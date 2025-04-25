from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from twilio.rest import Client
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Get Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone = os.getenv('TWILIO_PHONE')
whatsapp_phone = os.getenv('WHATSAPP_PHONE')

# Debug: Print environment variables (remove in production)
print("Environment Variables Status:")
print(f"TWILIO_ACCOUNT_SID: {'Set' if account_sid else 'Not Set'}")
print(f"TWILIO_AUTH_TOKEN: {'Set' if auth_token else 'Not Set'}")
print(f"TWILIO_PHONE: {'Set' if twilio_phone else 'Not Set'}")
print(f"WHATSAPP_PHONE: {'Set' if whatsapp_phone else 'Not Set'}")

# Initialize Twilio client
try:
    if all([account_sid, auth_token]):
        client = Client(account_sid, auth_token)
        print("Twilio client initialized successfully")
    else:
        client = None
        print("Twilio client not initialized - missing credentials")
except Exception as e:
    print(f"Error initializing Twilio client: {str(e)}")
    client = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/certificates')
def certificates():
    return render_template('certificates.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/certificates/<filename>')
def view_certificate(filename):
    return send_from_directory('my_certificates', filename)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        if not client:
            print("Error: Twilio client not initialized")
            return jsonify({
                'success': False,
                'message': 'WhatsApp messaging is not configured'
            }), 503

        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        subject = data.get('subject')
        message = data.get('message')
        
        print(f"Received message request from: {name} ({email})")
        
        # Format the message
        formatted_message = f"This is a contact wish from Swarnava Portfolio\n\n" \
                          f"Name: {name}\n" \
                          f"Email: {email}\n" \
                          f"Phone: {phone}\n" \
                          f"Subject: {subject}\n" \
                          f"Message: {message}"
        
        print(f"Attempting to send message to: {whatsapp_phone}")
        print(f"From: {twilio_phone}")
        
        # Send WhatsApp message using Twilio
        message = client.messages.create(
            from_=twilio_phone,
            body=formatted_message,
            to=whatsapp_phone
        )
        
        print(f"Message sent successfully. SID: {message.sid}")
        return jsonify({'success': True, 'message': 'Your message has been sent'})
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 