import os
import google.generativeai as genai
import urllib.request
import json
import socket
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Property, PropertyTax, AIRequestLog, LocalInformation, OwnerInformation, FinancialInformation, AdditionalInformation, SupportingDocument, TitleMovementRequest

def get_specific_property_context(user_message):
    """
    Scans the user message for keywords to find relevant properties.
    Searches across Title, Lot, Owner, Location, and Financial info.
    """
    context_str = ""
    if not user_message:
        return context_str
        
    query = user_message.lower()
    
    # Filter stopwords to avoid matching everything on "the", "is", "a", etc.
    stopwords = ['the', 'is', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
    query_words = [w for w in query.split() if w not in stopwords and len(w) > 2]
    
    if not query_words:
        return ""
    
    q_objects = Q()
    for word in query_words:
        # Property Table
        q_objects |= Q(title_no__icontains=word)
        q_objects |= Q(lot_no__icontains=word)
        q_objects |= Q(title_description__icontains=word)
        q_objects |= Q(title_classification__icontains=word)
        q_objects |= Q(title_status__icontains=word)
        
        # Owner Information Table
        q_objects |= Q(ownerinformation__oi_fullname__icontains=word)
        q_objects |= Q(ownerinformation__oi_custody_title__icontains=word)
        q_objects |= Q(ownerinformation__oi_bankname__icontains=word)
        
        # Local Information Table
        q_objects |= Q(localinformation__loc_province__icontains=word)
        q_objects |= Q(localinformation__loc_city__icontains=word)
        q_objects |= Q(localinformation__loc_barangay__icontains=word)
        q_objects |= Q(localinformation__loc_specific__icontains=word)
        
        # Financial Information Table
        q_objects |= Q(financialinformation__fi_borrower__icontains=word)
        q_objects |= Q(financialinformation__fi_mortgage__icontains=word)
        q_objects |= Q(financialinformation__fi_encumbrance__icontains=word)
        
        # Additional Information Table
        q_objects |= Q(additionalinformation__ai_remarks__icontains=word)
        
        # Supporting Documents Table (File Names)
        q_objects |= Q(supportingdocument__file__icontains=word)
        
        # Property Tax Table
        q_objects |= Q(propertytax__tax_remarks__icontains=word)
        q_objects |= Q(propertytax__tax_status__icontains=word)
        
        # Title Movement Table
        q_objects |= Q(title_movements__tm_transmittal_no__icontains=word)
        q_objects |= Q(title_movements__tm_purpose__icontains=word)
        q_objects |= Q(title_movements__tm_received_by__icontains=word)
        q_objects |= Q(title_movements__status__icontains=word)
    
    # Execute Query
    matching_props = Property.objects.filter(q_objects).distinct()[:15] # Limit to 15 to manage context size

    if matching_props.exists():
        context_str += "\n--- RELEVANT PROPERTY DETAILS (Matched from Query) ---\n"
        for prop in matching_props:
            try:
                # Fetch related data efficiently
                owner = prop.ownerinformation_set.first()
                loc = prop.localinformation_set.first()
                fin = prop.financialinformation_set.first()
                add_info = prop.additionalinformation_set.first()
                docs = prop.supportingdocument_set.all()
                taxes = prop.propertytax_set.all().order_by('-tax_year', '-tax_quarter')
                title_movements = prop.title_movements.all().order_by('-created_at')
                
                owner_name = owner.oi_fullname if owner else "N/A"
                owner_bank = owner.oi_bankname if owner else "N/A"
                custody = owner.oi_custody_title if owner else "N/A"
                location = f"{loc.loc_barangay or ''}, {loc.loc_city or ''}, {loc.loc_province or ''}".strip(', ') if loc else "N/A"
                
                context_str += f"**Property**: {prop.title_no} | **Lot**: {prop.lot_no}\n"
                context_str += f"  - **Owner**: {owner_name} (Bank: {owner_bank})\n"
                context_str += f"  - **Custody of Title**: {custody}\n"
                context_str += f"  - **Location**: {location}\n"
                context_str += f"  - **Status**: {prop.get_title_status_display()} | **Class**: {prop.get_title_classification_display()}\n"
                context_str += f"  - **Area**: {prop.lot_area} sqm\n"
                context_str += f"  - **Date Added**: {prop.date_added.date() if prop.date_added else 'N/A'}\n"
                
                if fin:
                    context_str += f"  - **Financials**: Mortgaged to {fin.fi_mortgage or 'None'} | Encumbrance: {fin.fi_encumbrance or 'None'} | Borrower: {fin.fi_borrower or 'None'}\n"
                
                if add_info and add_info.ai_remarks:
                    context_str += f"  - **Remarks**: {add_info.ai_remarks}\n"
                
                if docs.exists():
                    doc_names = ", ".join([os.path.basename(d.file.name) for d in docs])
                    context_str += f"  - **Documents**: {doc_names}\n"
                
                context_str += "  - **Tax History**:\n"
                for t in taxes: # List all taxes for matched properties
                    created_by = f" by {t.created_by.get_full_name()}" if t.created_by else ""
                    context_str += f"    * {t.tax_year} {t.tax_quarter}: {t.tax_amount} ({t.tax_status}) - Due: {t.tax_due_date} [{t.tax_remarks or ''}]\n"
                    context_str += f"      Created: {t.created_at.date()}{created_by}\n"
                
                context_str += "  - **Title Movements**:\n"
                for movement in title_movements:
                    released_by = f" by {movement.tm_released_by.get_full_name()}" if movement.tm_released_by else ""
                    approved_by = f" by {movement.tm_approved_by.get_full_name()}" if movement.tm_approved_by else ""
                    context_str += f"    * {movement.tm_transmittal_no}: {movement.tm_purpose} - Status: {movement.status}\n"
                    context_str += f"      Received by: {movement.tm_received_by}, Created: {movement.created_at.date()}\n"
                    context_str += f"      Released{released_by}, Approved{approved_by}\n"
                
                context_str += "--------------------------------------------------\n"
            except Exception as e:
                continue
                
    return context_str

def get_project_context(user_message=""):
    """
    Fetches a summary of the project data (ReadOnly) to feed into the AI.
    Focuses on critical information like overdue taxes and property status.
    """
    today = timezone.now().date()
    next_30_days = today + timedelta(days=30)

    # 1. Fetch Overdue Taxes
    overdue_taxes = PropertyTax.objects.filter(
        tax_status__in=['Overdue', 'Due', 'Pending'],
        tax_due_date__lt=today
    ).select_related('property')

    # 2. Fetch Upcoming Taxes (Next 30 Days)
    upcoming_taxes = PropertyTax.objects.filter(
        tax_status__in=['Pending', 'Due'],
        tax_due_date__range=[today, next_30_days]
    ).select_related('property')

    # 3. Property Summary
    total_properties = Property.objects.count()
    active_properties = Property.objects.filter(title_status='ACT').count()
    
    # 4. Title Movement Summary
    total_title_movements = TitleMovementRequest.objects.count()
    recent_title_movements = TitleMovementRequest.objects.filter(created_at__gte=today - timedelta(days=30)).count()
    
    # 5. Property Tax Summary
    total_tax_records = PropertyTax.objects.count()
    paid_taxes = PropertyTax.objects.filter(tax_status='Paid').count()
    overdue_tax_count = overdue_taxes.count()

    # Build the context string
    context_str = f"Current Date: {today}\n\n"
    context_str += "--- PROJECT SUMMARY ---\n"
    context_str += f"Total Properties: {total_properties}\n"
    context_str += f"Active Properties: {active_properties}\n"
    context_str += f"Total Title Movements: {total_title_movements}\n"
    context_str += f"Recent Title Movements (30 days): {recent_title_movements}\n"
    context_str += f"Total Tax Records: {total_tax_records}\n"
    context_str += f"Paid Taxes: {paid_taxes}\n"
    context_str += f"Overdue Taxes: {overdue_tax_count}\n\n"

    # 4. Full Property List (Summary)
    all_props = Property.objects.all().order_by('property_id')[:50]
    
    context_str += "--- ALL PROPERTIES INDEX (Title | Lot | Owner | Status) ---\n"
    for p in all_props:
        owner_name = "N/A"
        # Access reverse relation safely
        owner = p.ownerinformation_set.first()
        if owner:
            owner_name = owner.oi_fullname
            
        context_str += f"Title: {p.title_no} | Lot: {p.lot_no} | Owner: {owner_name} | Status: {p.get_title_status_display()}\n"
        
    if total_properties > 50:
        context_str += f"... [Truncated] and {total_properties - 50} more properties available. Ask specifically to find them.\n"
    
    context_str += "\n--- OVERDUE TAXES (Action Required) ---\n"
    if overdue_taxes.exists():
        for tax in overdue_taxes:
            context_str += (f"- Property: {tax.property.title_no} ({tax.property.lot_no})\n"
                            f"  Amount: {tax.tax_amount}\n"
                            f"  Due Date: {tax.tax_due_date} (Overdue)\n"
                            f"  Status: {tax.tax_status}\n")
    else:
        context_str += "No overdue taxes found.\n"
    
    context_str += "\n--- UPCOMING TAXES (Next 30 Days) ---\n"
    if upcoming_taxes.exists():
        for tax in upcoming_taxes:
            context_str += (f"- Property: {tax.property.title_no} ({tax.property.lot_no})\n"
                            f"  Amount: {tax.tax_amount}\n"
                            f"  Due Date: {tax.tax_due_date}\n")
    else:
        context_str += "No taxes due in the next 30 days.\n"

    # Add specific property context if identified in user message
    context_str += get_specific_property_context(user_message)

    return context_str

def query_local_llm(system_prompt, user_message):
    """
    Fallback to local LLM (Ollama) when offline.
    Assumes Ollama is running on localhost:11434.
    """
    url = "http://localhost:11434/api/generate"
    
    # Construct a single text prompt
    full_prompt = f"{system_prompt}\n\nUser Question: {user_message}\nAnswer:"
    
    payload = {
        "model": "llama3", 
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        # 30 second timeout
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('response', 'Error: No response from local model.')
    except Exception as e:
        # Return None to indicate failure/not running
        return None

def get_ai_response(user_message, image_file=None, user=None):
    """
    Generates a response using Gemini, incorporating project data context.
    Handles both text-only and multimodal (image) inputs.
    Falls back to Local LLM (Ollama) if offline.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")

    # 1. Log Request & Determine Context
    try:
        if user:
            AIRequestLog.objects.create(user=user, request_type='chat')
        else:
            AIRequestLog.objects.create(user=None, request_type='chat')
            
        is_first_question = False
        if user:
            # Use local date range to ensure "midnight" reset aligns with user's timezone and DB storage
            now = timezone.now()
            local_now = timezone.localtime(now)
            today_start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            request_count = AIRequestLog.objects.filter(user=user, timestamp__gte=today_start).count()
            if request_count <= 1:
                is_first_question = True
    except Exception as e:
        # Fallback if DB fails, though unlikely
        is_first_question = False
        print(f"DB Error: {e}")

    # 2. Build System Prompt
    project_data = get_project_context(user_message)
    
    suggestion_instruction = ""
    if is_first_question:
        suggestion_instruction = (
            "IMPORTANT: After answering the user's question, ALWAYS provide a section titled 'Suggestions / Next Steps'.\n"
            "In this section, propose 1-2 relevant actions the user can take based on the context (e.g., 'Check the due date for Property Y', 'Upload the receipt for the recent payment', 'Review the tax history').\n\n"
        )
    
    report_instruction = (
        "--- REPORT GENERATION ---\n"
        "If the user asks for a report (e.g., 'generate a report', 'summary', 'overview'), follow these steps:\n"
        "1. Present the data in a DETAILED, narrative format using bullet points (•) for easy reading\n"
        "2. Act as if you are a manager presenting to a client or non-technical stakeholder.\n"
        "3. Do NOT use technical jargon or markdown tables - use simple bullet points and clear language\n"
        "4. Be thorough and explain the significance of the numbers in plain English\n"
        "5. Structure the report logically with clear section headings and bullet points\n"
        "6. NEVER use markdown tables or complex formatting - use simple bullet points for all data\n\n"
    )

    system_prompt = (
        "You are the RDRealty AI Assistant, a friendly and professional Real Estate Property Manager.\n"
        "Speak naturally and conversationally, like a human colleague. Use warm, engaging language and avoid robotic or overly formal phrasing.\n"
        "Your goal is to help the user manage properties, identify due dates, analyze financial data, and provide valuable insights.\n"
        "You have READ-ONLY access to the project data below - you can view all information but cannot edit, update, or delete any records.\n\n"
        "--- RESPONSE STYLE GUIDE ---\n"
        "1. **Be Human**: Use natural language, contractions, and friendly tone like 'I'd be happy to help' or 'Let me check that for you'\n"
        "2. **Be Helpful**: Always provide context and explanations, not just raw data\n"
        "3. **Be Proactive**: Offer suggestions and next steps based on the data\n"
        "4. **Use Title Numbers**: Always refer to properties by their title numbers (e.g., 'Title 123-456'), never by internal property IDs\n"
        "5. **Format Clearly**: Use **bold** for labels, bullet points (•) for lists, and blank lines between sections\n"
        "6. **No Markdown Tables**: NEVER use markdown tables or complex formatting - use simple bullet points that are easy for non-technical users to understand\n"
        "7. **Use Philippine Currency**: ALWAYS use Philippine Peso (₱) symbol instead of Dollar ($) for all monetary amounts\n\n"
        f"{report_instruction}"
        "--- DOCUMENT & IMAGE ANALYSIS ---\n"
        "When users upload documents or images, you must:\n"
        "1. **Extract Everything**: Read all text, numbers, dates, names, and amounts visible in the image\n"
        "2. **Cross-Reference**: Compare extracted information with the project database below\n"
        "3. **Explain Clearly**: Describe what you see in simple terms and how it relates to existing records\n"
        "4. **Identify New Info**: If the document contains new information (receipts, updates, etc.), treat it as current truth\n"
        "5. **Provide Context**: Explain the significance of the document content to the user\n\n"
        "--- RECOMMENDATION ENGINE ---\n"
        "Always provide helpful suggestions based on the data:\n"
        "• **Overdue Items**: Highlight urgent actions needed for overdue taxes or pending movements\n"
        "• **Best Practices**: Suggest property management tips and next steps\n"
        "• **Data Gaps**: Point out missing information that would be valuable to collect\n"
        "• **Follow-up Actions**: Recommend specific tasks based on the current situation\n\n"
        "--- DATA INTEGRITY ---\n"
        "1. **Never Invent**: Only use information from the project data or uploaded documents\n"
        "2. **Be Honest**: Clearly state when information is missing or unavailable\n"
        "3. **Stay Current**: Use the most recent data available in the system\n\n"
        f"{suggestion_instruction}"
        f"--- PROJECT DATA CONTEXT ---\n{project_data}\n"
        "--------------------\n"
    )

    # 3. Try Gemini (Online)
    gemini_error = None
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            
            chat_content = []
            chat_content.append(system_prompt)
            chat_content.append(f"User: {user_message}")
            
            if image_file:
                from PIL import Image
                import mimetypes
                
                # Check if file is actually an image
                file_type = mimetypes.guess_type(image_file.name)[0]
                if file_type and file_type.startswith('image/'):
                    try:
                        image = Image.open(image_file)
                        chat_content.append(image)
                        chat_content.append("\n[System: The user has uploaded an image. Please transcribe and analyze it carefully to answer the question.]")
                    except Exception as img_error:
                        # If image processing fails, treat it as a document
                        gemini_error = f"Image processing failed: {img_error}. Treating as document reference."
                        chat_content.append(f"\n[System: The user uploaded a file named '{image_file.name}'. Please analyze this document and help the user understand its contents.]")
                else:
                    # Handle non-image files (PDFs, documents, etc.)
                    chat_content.append(f"\n[System: The user uploaded a document file: '{image_file.name}'. Please help analyze this document and provide insights based on its content.]")
            
            response = model.generate_content(chat_content)
            return response.text
        except Exception as e:
            gemini_error = str(e)
            print(f"Gemini Error (Switching to Offline Mode): {gemini_error}")
            # Fall through to local
            pass
            
    # 4. Fallback to Local LLM (Offline)
    local_response = query_local_llm(system_prompt, user_message)
    if local_response:
        return f"{local_response}\n\n(Note: Answered via Offline Mode)"
    
    # 5. Final Failure
    if not api_key:
        return "Error: No Internet Connection and 'Ollama' (Local AI) is not running.\nPlease install Ollama (https://ollama.com) and run 'ollama run llama3' to use offline mode."
    else:
        error_msg = "Error: Could not connect to Google AI (Cloud) or Ollama (Local)."
        if gemini_error:
            error_msg += f"\n\nGoogle AI Error: {gemini_error}"
        error_msg += "\n\nPlease check your internet, API key, or start your local AI server."
        return error_msg
