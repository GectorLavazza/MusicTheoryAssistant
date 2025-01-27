# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\wolkp\\PycharmProjects\\MusicTheoryAssistant\\resources', 'resources'),
           ('C:\\Users\\wolkp\\PycharmProjects\\MusicTheoryAssistant\\test.txt', '.')],
    hiddenimports=['numba.core.types.old_scalars', 'numba.core.datamodel.old_models', 'numba.cpython.old_builtins',
    'numba.core.typing.old_builtins', 'numba.core.typing.old_cmathdecl', 'numba.core.typing.old_mathdecl',
    'numba.cpython.old_hashing', 'numba.cpython.old_numbers', 'numba.cpython.old_tupleobj',
    'numba.np.old_arraymath', 'numba.np.random.old_distributions',
    'numba.np.random.old_random_methods', 'numba.cpython.old_mathimpl',
    'numba.core.old_boxing'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MusicTheoryAssistant',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MusicTheoryAssistant',
)
