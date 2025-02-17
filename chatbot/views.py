from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import TransactionQuery

def chatbot_ui(request):
    """ Renders the chatbot UI """
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
    
    return render(request, 'chatbot/chatbot_ui.html', {'chat_history': request.session['chat_history']})


def handle_chat(request):
    """ Handles chat interactions dynamically using HTMX """
    
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat_history = request.session['chat_history']
    chat_state = request.session.get('chat_state', 'start')

    user_input = request.POST.get('user_input')
    
    if user_input:  
        chat_history.append({'user': user_input})

    if chat_state == 'start':
        bot_response = "Welcome! How can I help you today?"
        options = ["Check Transaction Status", "Report an Issue", "Contact Support"]
        request.session['chat_state'] = 'awaiting_selection'
    
    elif chat_state == 'awaiting_selection':
        if user_input == "Check Transaction Status":
            request.session['chat_state'] = 'transaction_status'
            bot_response = "Please enter your Transaction ID:"
            options = []
        
        elif user_input == "Report an Issue":
            request.session['chat_state'] = 'report_issue'
            bot_response = "Please describe the issue you're facing:"
            options = []
        
        elif user_input == "Contact Support":
            request.session['chat_state'] = 'contact_support'
            bot_response = "Please provide your contact details:"
            options = []
        
        else:
            bot_response = "Please select a valid option:"
            options = ["Check Transaction Status", "Report an Issue", "Contact Support"]

    elif chat_state == 'transaction_status':
        try:
            transaction = TransactionQuery.objects.get(transaction_id=user_input)
            bot_response = f"Transaction status: {transaction.status}. What else can I help you with?"
        except TransactionQuery.DoesNotExist:
            bot_response = "Transaction not found. Please try again."
        options = ["Check Another Transaction", "Main Menu"]
        request.session['chat_state'] = 'awaiting_selection'

    elif chat_state == 'report_issue':
        bot_response = "Thank you for reporting the issue. Our team will review it soon. What else can I assist you with?"
        options = ["Main Menu"]
        request.session['chat_state'] = 'awaiting_selection'

    elif chat_state == 'contact_support':
        bot_response = "Thank you! Our support team will contact you soon. Anything else?"
        options = ["Main Menu"]
        request.session['chat_state'] = 'awaiting_selection'

    chat_history.append({'bot': bot_response, 'options': options})
    request.session['chat_history'] = chat_history
    request.session.modified = True

    # Render only the new messages dynamically
    new_message_html = render_to_string('chatbot/partials/chat_messages.html', {'chat_history': chat_history[-1:]})
    
    return JsonResponse({'html': new_message_html})

from django.http import HttpResponse

def reset_session(request):
    """ Clears session data and regenerates session ID """
    request.session.flush()  # Clears all session data
    return HttpResponse("Session has been reset")