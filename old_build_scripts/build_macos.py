import os
import subprocess
import shutil

def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Remove any .pyc files and __pycache__ directories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
        for file_name in files:
            if file_name.endswith('.pyc'):
                os.remove(os.path.join(root, file_name))

def build_app():
    """Build the macOS application"""
    print("Building MAST for macOS...")
    
    # Clean previous builds
    clean_build()
    
    # Run PyInstaller using the spec file
    subprocess.run([
        'pyinstaller',
        'MAST.spec',
        '--clean',
        '--noconfirm'
    ], check=True)
    
    print("Build complete!")
    
    # Verify the app bundle
    app_path = 'dist/MAST.app'
    if os.path.exists(app_path):
        print(f"\nApplication bundle created at: {app_path}")
    else:
        print("Error: Application bundle not created!")

if __name__ == "__main__":
    build_app()