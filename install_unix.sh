#!/bin/bash

echo "Integrity Assistant 1.0.2 - Unix Installer"
echo "=========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH. Please install Python 3.8 or higher."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Detected Python version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating default configuration file..."
    cp .env.template .env
fi

# Create desktop shortcut (varies by platform)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Creating macOS application launcher..."
    DESKTOP_DIR="$HOME/Desktop"
    APP_SCRIPT="$DESKTOP_DIR/IntegrityAssistant.command"
    
    echo "#!/bin/bash" > "$APP_SCRIPT"
    echo "cd $(pwd)" >> "$APP_SCRIPT"
    echo "source .venv/bin/activate" >> "$APP_SCRIPT"
    echo "python3 main.py" >> "$APP_SCRIPT"
    
    chmod +x "$APP_SCRIPT"
    
    echo "Created launcher at: $APP_SCRIPT"
else
    # Linux
    echo "Creating Linux desktop shortcut..."
    DESKTOP_DIR="$HOME/Desktop"
    SHORTCUT="$DESKTOP_DIR/IntegrityAssistant.desktop"
    
    echo "[Desktop Entry]" > "$SHORTCUT"
    echo "Type=Application" >> "$SHORTCUT"
    echo "Name=Integrity Assistant" >> "$SHORTCUT"
    echo "Exec=$(pwd)/.venv/bin/python3 $(pwd)/main.py" >> "$SHORTCUT"
    echo "Terminal=false" >> "$SHORTCUT"
    echo "Categories=Utility;" >> "$SHORTCUT"
    
    chmod +x "$SHORTCUT"
    
    echo "Created shortcut at: $SHORTCUT"
fi

echo
echo "Installation complete!"
echo
echo "You can now:"
echo "1. Run Integrity Assistant from the desktop shortcut"
echo "2. Run manually with: python3 $(pwd)/main.py"
echo
echo "Note: You'll need to create an account on the Integrity website"
echo "and log in when you first launch the application."
echo 