#!/bin/bash

# Activate virtual environment if you're using one
# source venv/bin/activate

# Install build requirements
pip install -r build-requirements.txt

# Run build script
python build.py

# Sign the application (if you have an Apple Developer certificate)
# codesign --force --sign "Developer ID Application: Your Name" "dist/MAST.app"

# Create DMG (optional)
# create-dmg \
#   --volname "MAST Installer" \
#   --volicon "app_icon.icns" \
#   --window-pos 200 120 \
#   --window-size 800 400 \
#   --icon-size 100 \
#   --icon "MAST.app" 200 190 \
#   --hide-extension "MAST.app" \
#   --app-drop-link 600 185 \
#   "dist/MAST-Installer.dmg" \
#   "dist/MAST.app"
