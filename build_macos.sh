
#!/bin/bash

# Ensure the script exits on the first error
set -e

# Define paths and environment variables
PROJECT_PATH="/Users/jk/src/mast"
CONDA_ENV="mast"
BUILD_DIR="${PROJECT_PATH}/dist"

# Activate conda environment
echo "Activating conda environment: ${CONDA_ENV}"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${CONDA_ENV}

# Move to the project directory
echo "Moving to project directory: ${PROJECT_PATH}"
cd ${PROJECT_PATH}

# Ensure dependencies are installed
echo "Installing dependencies from requirements.txt"
pip install -r requirements.txt

# Remove old build directory if it exists
echo "Cleaning up previous build..."
rm -rf ${BUILD_DIR}
rm -rf build
rm -rf __pycache__
rm -f MAST.spec

# Generate PyInstaller spec file
echo "Generating MAST.spec file..."
pyi-makespec --windowed --name MAST main.py

# Add hooks and hidden imports to the spec file
echo "Updating MAST.spec file..."
cat > MAST.spec <<EOF
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['${PROJECT_PATH}'],
    binaries=[
        ('${CONDA_PREFIX}/lib/libopenblas.dylib', '.'),
        ('${CONDA_PREFIX}/lib/libfftw3f.dylib', '.'),
        ('${CONDA_PREFIX}/lib/libpython3.11.dylib', '.'),
    ],
    datas=[],
    hiddenimports=[
        'librosa',
        'matchering',
        'PyQt5',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'numpy',
        'scipy',
        'matplotlib'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MAST',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
)

app = BUNDLE(
    exe,
    name='MAST.app',
    icon='app_icon.icns',
    bundle_identifier='se.originalminds.mast',
)
EOF

# Run PyInstaller to create macOS executable
echo "Building macOS executable with PyInstaller..."
pyinstaller MAST.spec

# Verify the app bundle
echo "Verifying built application..."
if [ -d "${BUILD_DIR}/MAST.app" ]; then
    echo "Build successful! MAST.app is located in ${BUILD_DIR}"
else
    echo "Build failed. Please check for errors in the build process."
    exit 1
fi

echo "Build process completed."
