# Portfolio Website

A Flask-based portfolio website with WhatsApp integration for contact form submissions.

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Twilio credentials in `.env`
   - Never commit `.env` to version control

5. Run the application:
   ```bash
   python app.py
   ```

## Environment Variables

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE`: Your Twilio WhatsApp number
- `WHATSAPP_PHONE`: Your WhatsApp number for receiving messages

## Security Note

Never commit your `.env` file or expose your Twilio credentials. Keep them secure and use environment variables in production. 