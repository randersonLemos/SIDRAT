print("Dentro da interface de comunicacao entre Tardir e WAHOO")
--load_file = '/mnt/ALU/MS_RJN/5.fonte/tardis_wahoo/src/avaliacao/wahoo/?.lua;'
--package.path = [[/mnt/ALU/MS_RJN/5.fonte/tardis_wahoo/src/avaliacao/wahoo/?.lua;]]..package.path

variaveis = {}

add_variavel = function(nome, valor)
    print("Variavel [" .. nome .. "] recebo valor [" .. valor .. "]")
    variaveis[nome] = valor
    return true
end

executa_wahoo = function(id, load_file, file_lua)

    print("Executando interface...")
    print('caminho arquivo carregar =>' .. load_file)
    print('caminho wahoo =>' .. file_lua)

    package.path = package.path .. ";" .. load_file .. ";"
    local wahoo = require(file_lua)

    tamanho_variaveis = 0
    for k, v in pairs(variaveis) do
        tamanho_variaveis = tamanho_variaveis +1
    end
    if tamanho_variaveis < 1 then
        print('Não tem variaveis salvas')
        return nil
    end

    print('Chamando getResult' )
    of = getResult(variaveis, id)

    print('Retorno OF = ' .. of )

    print('Fim da execução')

    clean()
    return of
end

clean = function()
    variavies = {}
end
