import os
import subprocess
import platform
import shutil

def clean_build_directories():
    """Clean up build directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Clean spec file
    if os.path.exists('MAST.spec'):
        os.remove('MAST.spec')

def build_application():
    """Build the MAST application"""
    system = platform.system()
    
    # Clean previous builds
    clean_build_directories()
    
    print("Building MAST application...")
    
    if system == 'Darwin':  # macOS
        subprocess.run([
            'pyinstaller',
            '--name=MAST',
            '--windowed',
            '--onefile',
            '--icon=app_icon.icns',
            '--add-data=app_icon.icns:.',
            '--hidden-import=mutagen',
            '--hidden-import=librosa',
            '--hidden-import=matchering',
            '--hidden-import=PyQt5.QtMultimedia',
            'main.py'
        ])
    elif system == 'Windows':
        subprocess.run([
            'pyinstaller',
            '--name=MAST',
            '--windowed',
            '--onefile',
            '--icon=app_icon.ico',
            '--add-data=app_icon.ico;.',
            '--hidden-import=mutagen',
            '--hidden-import=librosa',
            '--hidden-import=matchering',
            '--hidden-import=PyQt5.QtMultimedia',
            'main.py'
        ])
    else:  # Linux
        subprocess.run([
            'pyinstaller',
            '--name=MAST',
            '--windowed',
            '--onefile',
            '--hidden-import=mutagen',
            '--hidden-import=librosa',
            '--hidden-import=matchering',
            '--hidden-import=PyQt5.QtMultimedia',
            'main.py'
        ])

    print("Build complete!")

if __name__ == "__main__":
    build_application()