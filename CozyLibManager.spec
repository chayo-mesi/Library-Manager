# -*- mode: python ; coding: utf-8 -*-
# Updated PyInstaller spec file for CozyLibraryManager
#
# This assumes the following directory structure:
# repo/
# ├── messy_cozy_lib.py
# ├── library_data.py
# ├── requirements.txt
# ├── CozyLibManager.spec (this file)
# └── ASSETS/
#     ├── fonts/
#     ├── *.png images
#     └── ...

from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['messy_cozy_lib.py'],  # Entry point - assumes same directory as this spec
    pathex=[],
    binaries=[],
    datas=[('ASSETS', 'ASSETS')],  # Bundle ASSETS folder
    hiddenimports=[
        'tkinter',  # Explicitly include tkinter for some PyInstaller versions
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'IPython',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # Include binaries in exe (onedir mode)
    a.datas,     # Include data files
    [],
    name='CozyLibraryManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Set to 'ASSETS/icon.ico' if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CozyLibraryManager',
)
