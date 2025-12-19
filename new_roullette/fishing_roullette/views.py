import pandas as pd
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse

def index(request):
    """Main page view that renders the white box and initial state."""
    # We pull data from the session to show the current status
    context = {
        'roster_loaded': 'available_roster' in request.session and len(request.session['available_roster']) > 0,
        'roster_count': len(request.session.get('available_roster', [])),
        'past_winners': request.session.get('past_winners', [])
    }
    return render(request, 'index.html', context)

def upload_roster(request):
    """Handles the Excel file upload."""
    if request.method == 'POST' and request.FILES.get('roster'):
        try:
            file = request.FILES['roster']
            df = pd.read_excel(file)
            # Take the first column and clean it
            names = df.iloc[:, 0].dropna().astype(str).str.strip().unique().tolist()
            
            if names:
                request.session['available_roster'] = names
                request.session['past_winners'] = [] 
                request.session.modified = True
        except Exception as e:
            print(f"Upload Error: {e}")
            
    return redirect('index')

def get_winner(request):
    """The API endpoint for the 'Spin' button."""
    roster = request.session.get('available_roster', [])
    
    if not roster:
        return JsonResponse({'error': 'No names left!'}, status=400)
    
    winner = random.choice(roster)
    roster.remove(winner)
    
    past_winners = request.session.get('past_winners', [])
    past_winners.insert(0, winner)
    
    request.session['available_roster'] = roster
    request.session['past_winners'] = past_winners
    request.session.modified = True
    
    return JsonResponse({
        'winner': winner.upper(),
        'roster': roster if roster else [winner]
    })

def reset_roster(request):
    """Resets the game."""
    request.session.flush()
    return redirect('index')