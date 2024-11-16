# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Collect all necessary data files
datas = []
datas += collect_data_files('librosa')
datas += collect_data_files('matchering')

# Add our local modules
datas += [
    ('ui', 'ui'),
    ('core', 'core'),
    ('config', 'config')
]

# Add any additional resources your app needs
binaries = []
if sys.platform == 'darwin':  # macOS specific
    binaries += collect_dynamic_libs('librosa')
    binaries += collect_dynamic_libs('soundfile')

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath(os.getcwd())],  # Add the current directory to path
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'librosa',
        'librosa.util',
        'librosa.feature',
        'librosa.effects',
        'librosa.core.spectrum',
        'librosa.core.pitch',
        'librosa.core.audio',
        'librosa.core',
        'librosa.display',
        'matchering',
        'numpy',
        'scipy',
        'scipy.signal',
        'scipy.fft',
        'scipy.fftpack',
        'soundfile',
        'mutagen',
        'PyQt5',
        'PyQt5.QtMultimedia',
        'PyQt5.QtMultimediaWidgets',
        'sklearn.preprocessing',
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
        'resampy',
        'ui',
        'ui.main_window',
        'ui.dialogs',
        'ui.widgets',
        'core',
        'core.analyzer',
        'core.mastering',
        'config'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MAST',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.icns'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MAST'
)

app = BUNDLE(
    coll,
    name='MAST.app',
    icon='app_icon.icns',
    bundle_identifier='com.jk.mast',
    info_plist={
        'CFBundleName': 'MAST',
        'CFBundleDisplayName': 'MAST',
        'CFBundleExecutable': 'MAST',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.jk.mast',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'NSRequiresAquaSystemAppearance': False,
        'LSApplicationCategoryType': 'public.app-category.music',
        'CFBundleDocumentTypes': [],
        'NSMicrophoneUsageDescription': 'MAST does not use the microphone.',
    }
)