*******************************************************************************
** cria yml do conda
1 - executar o comando:
	+ windows -> conda env export > M:\Produtos\TARDIS\docs\Ambiente\Anaconda\python_3.7.7_environment_win.yml
	+ linux   -> conda env export > /mnt/TEC/Produtos/TARDIS/docs/Ambiente/Anaconda/python_3.7.7_environment_linux.yml

*******************************************************************************
** criar novo ambiente conda
1 - lembra de alterar no arquivo .yml o name e prefix para o caminho destinho
2 - executar o comando:
	+ windows -> conda env create -f M:\Produtos\TARDIS\docs\Ambiente\Anaconda\python_3.7.7_environment_win.yml -p S:\MS_RJN\5.fonte\.interpretador\conda_windows\python_3.7.7
	
	+ linux -> conda create -f /mnt/TEC/Produtos/TARDIS/docs/Ambiente/Anaconda/python_3.7.7_environment.yml -p /mnt/ALU/MS_RJN/5.fonte/.interpretador/conda_linux/python_3.7.7

*******************************************************************************
** criar arquivo de lib do pip
1 - executar o comando:
	+ windows -> pip freeze > M:\Produtos\TARDIS\docs\Ambiente\Anaconda\python_3.7.7_requirement_win.txt
	+ linux   -> pip freeze > /mnt/TEC/Produtos/TARDIS/docs/Ambiente/Anaconda/python_3.7.7_requirement_linux.txt

*******************************************************************************
** instalar das libs do pip
1 - executar o comando:
	+ windows -> pip install -r M:\Produtos\TARDIS\docs\Ambiente\Anaconda\python_3.7.7_requirement_win.txt
	+ linux   -> pip install -r /mnt/TEC/Produtos/TARDIS/docs/Ambiente/Anaconda/python_3.7.7_requirement_linux.txt
