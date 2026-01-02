import os
import google.generativeai as genai
import urllib.request
import json
import socket
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Property, PropertyTax, AIRequestLog, LocalInformation, OwnerInformation, FinancialInformation, AdditionalInformation, SupportingDocument

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

    # Build a Q object for searching
    # We want to match ANY of the significant words in the query against the fields
    # But to be safe and accurate, let's stick to the full phrase or significant chunks if possible.
    # For now, let's try to match the *entire* query string first, or key segments.
    # Actually, a simple 'icontains' on the whole string might be too restrictive if the user types a sentence.
    # Let's use the query_words approach: Find properties that match ANY of the significant words.
    
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
                
                owner_name = owner.oi_fullname if owner else "N/A"
                owner_bank = owner.oi_bankname if owner else "N/A"
                custody = owner.oi_custody_title if owner else "N/A"
                location = f"{loc.loc_barangay or ''}, {loc.loc_city or ''}, {loc.loc_province or ''}".strip(', ') if loc else "N/A"
                
                context_str += f"Property ID: {prop.property_id} | Title: {prop.title_no} | Lot: {prop.lot_no}\n"
                context_str += f"  - Owner: {owner_name} (Bank: {owner_bank})\n"
                context_str += f"  - Custody of Title: {custody}\n"
                context_str += f"  - Location: {location}\n"
                context_str += f"  - Status: {prop.get_title_status_display()} | Class: {prop.get_title_classification_display()}\n"
                context_str += f"  - Area: {prop.lot_area} sqm\n"
                
                if fin:
                    context_str += f"  - Financials: Mortgaged to {fin.fi_mortgage or 'None'} | Encumbrance: {fin.fi_encumbrance or 'None'} | Borrower: {fin.fi_borrower or 'None'}\n"
                
                if add_info and add_info.ai_remarks:
                    context_str += f"  - Remarks: {add_info.ai_remarks}\n"
                
                if docs.exists():
                    doc_names = ", ".join([os.path.basename(d.file.name) for d in docs])
                    context_str += f"  - Documents: {doc_names}\n"
                
                context_str += "  - Tax History:\n"
                for t in taxes: # List all taxes for matched properties
                    context_str += f"    * {t.tax_year} {t.tax_quarter}: {t.tax_amount} ({t.tax_status}) - Due: {t.tax_due_date} [{t.tax_remarks or ''}]\n"
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

    # Build the context string
    context_str = f"Current Date: {today}\n\n"
    context_str += "--- PROJECT SUMMARY ---\n"
    context_str += f"Total Properties: {total_properties}\n"
    context_str += f"Active Properties: {active_properties}\n\n"

    # 4. Full Property List (Summary)
    # Provides a high-level view of all properties so the AI knows what exists.
    # Capped at 50 to preserve token limit.
    all_props = Property.objects.all().order_by('property_id')[:50]
    
    context_str += "--- ALL PROPERTIES INDEX (ID | Title | Lot | Owner) ---\n"
    for p in all_props:
        owner_name = "N/A"
        # Access reverse relation safely
        owner = p.ownerinformation_set.first()
        if owner:
            owner_name = owner.oi_fullname
            
        context_str += f"ID: {p.property_id} | Title: {p.title_no} | Lot: {p.lot_no} | Owner: {owner_name}\n"
        
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
    
    # Try 'llama3' first, but we can't easily guess what the user has installed.
    # 'llama3' is a safe bet for a modern install.
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
            today = timezone.now().date()
            request_count = AIRequestLog.objects.filter(user=user, timestamp__date=today).count()
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
        "1. Present the data in a DETAILED, narrative format.\n"
        "2. Act as if you are a manager presenting to a client or non-technical stakeholder.\n"
        "3. Do NOT use technical jargon.\n"
        "4. Be thorough and explain the significance of the numbers.\n"
        "5. Structure the report logically (e.g., Executive Summary, Key Findings, Action Items).\n\n"
    )

    system_prompt = (
        "You are the RDRealty AI Assistant, a friendly and professional Real Estate Property Manager.\n"
        "Speak naturally and conversationally, like a human colleague. Avoid robotic, overly formal, or repetitive phrasing.\n"
        "Your goal is to help the user manage properties, identify due dates, and analyze financial data.\n"
        "You have READ-ONLY access to the project data below.\n\n"
        "--- FORMATTING RULES (CRITICAL) ---\n"
        "1. DO NOT use Markdown tables (e.g., | Header | Row |). Non-tech users find them hard to read on mobile or small screens.\n"
        "2. Instead, use clear, simple lists or paragraphs.\n"
        "   - Use bullet points (•) for lists.\n"
        "   - Use bold text (**Text**) for emphasis on keys/labels.\n"
        "   - Example: \n"
        "     **Property**: Title 123-456\n"
        "     **Owner**: Juan Cruz\n"
        "     **Status**: Active\n"
        "3. Keep the layout clean and spacious. Add blank lines between sections.\n\n"
        f"{report_instruction}"
        "--- IMAGE ANALYSIS INSTRUCTIONS ---\n"
        "If the user uploads an image, you must:\n"
        "1. EXTRACT all visible text, dates, amounts, and names from the image.\n"
        "2. COMPARE this information with the Project Data below.\n"
        "3. USE the image content as the primary source of truth for the specific question if it contains new info (e.g., a new receipt).\n"
        "4. EXPLAIN what you see in the image clearly to the user.\n\n"
        "--- GENERAL RULES ---\n"
        "1. Do NOT invent data. Base your answers strictly on the context provided or the image uploaded.\n"
        "2. If the answer is not in the data, simply say you don't have that information.\n"
        "3. Be concise but warm.\n\n"
        f"{suggestion_instruction}"
        f"--- DATA CONTEXT ---\n{project_data}\n"
        "--------------------\n"
    )

    # 3. Try Gemini (Online)
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            
            chat_content = []
            chat_content.append(system_prompt)
            chat_content.append(f"User: {user_message}")
            
            if image_file:
                from PIL import Image
                image = Image.open(image_file)
                chat_content.append(image)
                chat_content.append("\n[System: The user has uploaded an image. Please transcribe and analyze it carefully to answer the question.]")
            
            response = model.generate_content(chat_content)
            return response.text
        except Exception as e:
            print(f"Gemini Error (Switching to Offline Mode): {e}")
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
        return "Error: Could not connect to Google AI (Cloud) or Ollama (Local). Please check your internet or start your local AI server."
