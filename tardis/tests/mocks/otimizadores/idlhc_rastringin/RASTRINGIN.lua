getResult =  function(variaveis, id)
	print('Otimizando funcao RASTRINGIN')

    n = 0
    soma = 0
    A = 10
    of = 0
    for k, v in pairs(variaveis) do
        n = n + 1

        if type(v) == "string" then
            if v == "I" then
                x = 0
            else
                x = 1
            end
        else
            x = v * 0.425
        end
        if x > 5.12 then
            x = 5.12
        end
        print('variavel     => [' .. k .. "]   valor => [" .. v .. ']   norm => [' .. x .. ']')

        pi = math.pi
        cos = math.cos( 2 * pi * x)
        interno = (x * x - A * cos)
        --print('interno      =>' .. interno)

        soma = soma + interno
    end

    m_of = A * n + ( -1 * A * 1 ) * n
    of = -1 * ( A * n + soma )
    print('of           =>' .. of .. ' MAX => [' .. m_of .. ']')

    return of
end