# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['/Users/jk/src/mast'],
    binaries=[
        ('/Users/jk/opt/anaconda3/envs/mast/lib/libopenblas.dylib', '.'),
        ('/Users/jk/opt/anaconda3/envs/mast/lib/libfftw3f.dylib', '.'),
        ('/Users/jk/opt/anaconda3/envs/mast/lib/libpython3.11.dylib', '.'),
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
