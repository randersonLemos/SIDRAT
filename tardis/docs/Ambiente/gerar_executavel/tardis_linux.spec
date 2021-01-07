# -*- mode: python ; coding: utf-8 -*-

import re

block_cipher = None

folders_to_copy = ['/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/campo_namorado_numero_pocos/base',
                   '/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/campo_namorado_posicionamento/base',
                   '/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/funcoes_teste/base/clustering',
                   '/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/funcoes_teste/base/knapsack',
                   '/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/funcoes_teste/base/rastrigin',
                   '/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/funcoes_teste/base/rosenbrock',
                   '/mnt/ALU/MS_RJN/5.fonte/tardis/src/modulo/problemas_fechados/funcoes_teste/base/sphere']
added_files = []

for folder in folders_to_copy:
    added_files.append((folder, re.findall('(src.*)',folder)[0]))

a = Analysis(['/mnt/ALU/MS_RJN/5.fonte/tardis/src/main.py'],
             pathex=['/mnt/ALU/MS_RJN/5.fonte/tardis/'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=['/mnt/ALU/MS_RJN/5.fonte/tardis/src/docs/Ambiente/gerar_executavel/addhooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='tardis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tardis')
