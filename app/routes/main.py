from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

main_bp = Blueprint('main', __name__)

# Initialize Gemini client
def get_gemini_client():
    """Initialize and return Gemini client."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return genai.Client(api_key=api_key)

def get_policy_dates():
    """Helper function to get consistent policy dates across all policy pages."""
    date_updated = datetime(2025, 5, 29)   # Date format: (YYYY, MM, DD)
    date_effective = date_updated + timedelta(days=14)  # 14 days after update
    return date_updated, date_effective

@main_bp.route('/')
def home():
    """Home page route."""
    return render_template('home.html')

@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

# Policy Pages
@main_bp.route('/privacy-policy')
def privacy_policy():
    """Privacy Policy page route."""
    date_updated, date_effective = get_policy_dates()
    return render_template('policy-pages/privacy-policy.html', 
                         date_updated=date_updated, 
                         date_effective=date_effective)

@main_bp.route('/terms-of-service')
def terms_of_service():
    """Terms of Service page route."""
    date_updated, date_effective = get_policy_dates()
    return render_template('policy-pages/terms-of-service.html',
                         date_updated=date_updated,
                         date_effective=date_effective)

@main_bp.route('/cookie-policy')
def cookie_policy():
    """Cookie Policy page route."""
    date_updated, date_effective = get_policy_dates()
    return render_template('policy-pages/cookie-policy.html',
                         date_updated=date_updated,
                         date_effective=date_effective)

@main_bp.route('/mental-health-chatbot')
def mental_health_chatbot():
    """Mental Health Chatbot page route."""
    return render_template('mental-health-chatbot.html')

@main_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI responses."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize Gemini client
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
            
        client = genai.Client(api_key=api_key)
        
        # Create mental health focused prompt
        system_prompt = """You are a compassionate mental health support chatbot named 'MindfulBot'. Provide helpful, empathetic responses while being clear that you are not a replacement for professional mental health care. Always encourage users to seek professional help when appropriate. Keep responses supportive, non-judgmental, and under 200 words. Focus on active listening, validation, and gentle guidance."""
        
        full_prompt = f"{system_prompt}\n\nUser message: {user_message}\n\nPlease respond with empathy and support:"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[full_prompt]
        )
        
        # Extract text from response
        bot_response = response.text if hasattr(response, 'text') else str(response)
        
        return jsonify({'response': bot_response})
        
    except ValueError as ve:
        return jsonify({'error': f'Configuration error: {str(ve)}'}), 500
    except Exception as e:
        # Log the actual error for debugging
        print(f"Chat error: {str(e)}")
        return jsonify({'error': 'I apologize, but I encountered a technical issue. Please try again in a moment.'}), 500
