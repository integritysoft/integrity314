# Integrity Assistant 1.0.2

An intelligent digital teammate that captures contextual digital activity and provides AI-driven responses using OpenAI.

## Features

- **Real-time Screen OCR**: Captures screen content at 2 FPS and extracts text
- **Keystroke Logging**: Securely logs keystrokes with privacy filters for sensitive content
- **Minimalist UI**: Sleek, non-intrusive chat overlay accessible via customizable shortcut
- **Secure Authentication**: Supabase-powered authentication with daily query limits
- **Contextual Responses**: Uses your recent screen content and keystrokes to provide relevant answers

## Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (required for text extraction)
  - Windows: [Download Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `apt-get install tesseract-ocr`

### Quick Installation

1. Download the ZIP file from the [Integrity website](https://integrity-web.vercel.app)
2. Extract the files using the password: `integrity2025`
3. Run the installer or executable for your platform

### Manual Installation (from source)

1. Clone the repository:
   ```
   git clone https://github.com/integrity-ai/integrity-assistant.git
   cd integrity-assistant
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Copy the template environment file and edit it:
   ```
   cp .env.template .env
   ```
   
4. Edit the `.env` file to add your Supabase credentials.

5. Run the application:
   ```
   python -m integrity_assistant
   ```

## Usage

1. **First Launch**: On first launch, you'll need to log in with your Supabase credentials.
2. **Create Account**: If you don't have an account, click "Create one" to sign up on the website.
3. **Chat Interface**: The minimalist chat overlay can be activated with Alt+Space (default shortcut).
4. **Asking Questions**: Simply type your questions in the chat interface, and the assistant will use your recent screen content and keystrokes as context for answers.

## Privacy & Security

- Images captured from your screen are immediately processed for text and then discarded
- Keystroke logging has built-in filters for sensitive content (passwords, credit card info, etc.)
- All data is transmitted securely via HTTPS/TLS
- Data is only stored temporarily in memory and not persisted to disk
- Authentication is handled securely through Supabase

## Troubleshooting

- **OCR Not Working**: Ensure Tesseract OCR is properly installed and the path is correctly set in `.env`
- **Authentication Issues**: Verify your Supabase credentials and check your internet connection
- **Rate Limiting**: Free accounts are limited to 100 queries per day

## License

© 2025 Integrity AI - All Rights Reserved 