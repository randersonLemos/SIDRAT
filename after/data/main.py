

tfm = TardisFilesManager(['RES_SPHERE', 'RES_RASTRIGIN', 'RES_ROSENBROCK'], '/media/beldroega/DATA/SIDRAT/tardis')

tfm.clean(r'it_(\d+)')

tdm = TardisDataManager(tfm.files('.*it_ultima.csv'))
#tdm = TardisDataManager(tfm.files(r'IDLHC_NSI50_NSP10_NNBC_NCT10_ECC10.*it_ultima.csv'))

tdm.save('./DATA')
