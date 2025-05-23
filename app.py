from flask import Flask, render_template, send_from_directory, request, jsonify, send_file
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

# Set the path for certificates directory
CERTIFICATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Certificate_jpg')

# Debug: Print environment variables and paths
print("\n=== Application Debug Information ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Application root path: {os.path.dirname(os.path.abspath(__file__))}")
print(f"Certificates Directory: {CERTIFICATES_DIR}")
print(f"Directory exists: {os.path.exists(CERTIFICATES_DIR)}")
if os.path.exists(CERTIFICATES_DIR):
    print(f"Files in certificates directory: {os.listdir(CERTIFICATES_DIR)}")
print("===================================\n")

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
    try:
        print("\n=== Loading Certificates ===")
        print(f"Checking directory: {CERTIFICATES_DIR}")
        
        if not os.path.exists(CERTIFICATES_DIR):
            print(f"Error: Directory {CERTIFICATES_DIR} does not exist")
            return render_template('certificates.html', certificates=[])
            
        cert_files = [f for f in os.listdir(CERTIFICATES_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
        print(f"Found {len(cert_files)} certificates:")
        for cert in cert_files:
            print(f"- {cert}")
            
        if not cert_files:
            print("No certificate files found!")
            return render_template('certificates.html', certificates=[])
            
        print("Rendering template with certificates")
        return render_template('certificates.html', certificates=cert_files)
    except Exception as e:
        print(f"Error in certificates route: {str(e)}")
        return render_template('certificates.html', certificates=[])

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/certificates/<filename>')
def view_certificate(filename):
    try:
        print(f"\n=== Serving Certificate: {filename} ===")
        file_path = os.path.join(CERTIFICATES_DIR, filename)
        print(f"Full path: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return "Certificate not found", 404
            
        print("Sending file...")
        return send_file(file_path, mimetype='image/jpeg')
    except Exception as e:
        print(f"Error serving certificate: {str(e)}")
        return str(e), 500

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True) 