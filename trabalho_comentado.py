# vamos definir a estrutura e o funcionamento do código em sequência:
# 1) receber o input do usuário com qualquer número inteiro;
# 2) após receber o número, passaremos ele pelo teste de Miller-Rabin, para verificação de primos,
# e caso o número seja primo, não rodaremos o algoritimo de Pollard's Rho, já que primmos não são fatoráveis;
# 3) após a verificação, caso não seja primo, passaremos pelo algorítimo de Pollard's Rho, e então ele será fatorado, e depois printado na forma fatorada;
# o código será separado em funções: 
# "eh_primo" -> verifica se é primo;
# "pollards_rho" -> executa o algorítimo;
# "fatorizar" -> irá fatorar recursivamente utilizando o algorítimo;
# "main" -> função main;


import math # precisaremos de funções para MDC;
import random # precisamos para gerar números aleatórios, especialmente para Miller-Rabin

def eh_primo(n):
    # definida a função de verificação de primos por Miller-Rabin;
    
    if n < 2:
        return False # não existem primos menores que 2, ora pois
    
    # durante o estudo do código, me deram a ideia de primeiro verificar se n é primo por um pequeno teste de divisibilidade, por uma lista de primos entre 2-23
    # dessa forma, poupamos trabalho caso o usuário coloque algum dos 9 primeiros primos

    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if n % p == 0:
            return n == p
    
    # ou seja, faremos o teste: se o resto da divisão de n por p resultar em 0 temos que p divide n;
    # caso n == p, o retorno será TRUE, dessa forma, n automaticamente será primo;
    # caso n != p, por exemplo, n = 26 e p = 2, 26/2 = 13, significa que n é multiplo de p, porém, 26 != 2, então return será falso;
    # pensemos de forma exemplificada: n = 13
    # o código irá rodar p e dividir n para cada valor: 13 % 2 não tem resto 0, return FALSE
    # 13 % 3 não tem resto 0, return FALSE
    # e assim por diante, até que eventualmente, p = 13, e 13 % 13 == 0, return TRUE; dessa forma, 13 é primo

    # agora, Miller-Rabin, mas primeiro, uma pequena explicação do que isso significa:
    # o teste de Miller-Rabin verifica, de forma probabilística, se um número f(n) é primo ou composto, utilizando o pequeno teorema de Fermat;
    # a principal notação utilizada é: a = b (mod n), que significa que dividir a por n retorna um resto b, exemplo:
    # 52 = 2 (mod 10), por que 52/10 tem quociente 5 e resto 2; lembrando que a = 0 (mod n) significa que a/n não tem resto, ou seja, n é divisor de a;

    # escolheremos um número aleatório "a" entre 1 e o antecessor de n; o pequeno teorema de Fermat diz basicamente: a^{n-1} = 1 (mod n) se n for primo;
    # de forma aritimética, a^{n-1}-1 = 0 (mod n), ou seja, (a^{n-1}-1)/n terá resto 0.
    # se n for primo, (ex, n=7), então n-1 sempre será PAR
    # por conta do expoente par, pensemos no quadrado da soma pela diferença: x^2-y^2 = (x+y)(x-y)
    # dessa forma, aplicando para (a^{n-1}-1), temos basicamente:
    # (a^{(n-1)/2} - 1)(a^{(n-1)/2} + 1) = 0 (mod n)
    # já que (a^{(n-1)/2})^2 é uma potência de potência, então o 2 que está dividindo é simplificado pelo expoente, retornando para a expressão original;
    # note que podemos tomar (a^{(n-1)/2} - 1) e fatorar novamente como quadrado da soma pela diferença, seguindo o padrão de aumentar a potência do denominador 2 conforme fatoramos (já que sempre que ocorre uma fatoração, é necessário dividir o expoente por 2 novamente)
    # temos então (a^{(n-1)/4} - 1) * (a^{(n-1)/4} + 1) * (a^{n-1}/2 + 1) = 0 (mod n)
    # a implicação matemática dessa fatoração nos diz que (n-1)/2 é par, e caso não seja mais possível fatorar, (n-1)/2 será ímpar;
    # é importante citar que isso vale para qualquer (n-1)/k tal que k seja uma potência de 2; o nosso objetivo é montar um algorítimo que fatore recursivamente até (n-1)/k ser ímpar
    # utilizaremos o lema de Euclides, que é basicamente o teorema fundamental da aritimética com propriedades de primos: dado p>1 será primo se, e somente se, p % ab == 0, então p divide a ou p divide b;
    # para o nosso caso, se n for primo, e o expoente (n-1)/k for ímpar, então n dividirá ao menos um dos termos expandidos, satisfazendo (a^{n-1}/k - 1)(a^{n-1}/k + 1)...(a^{n-1}/2 + 1) = 0 (mod n)
    # por exemplo: 6 * 2 = 12 -> 4 pode dividir 12, mas não pode dividir 6 nem 2; como 4 não é primo, ele não consegue dividir nenhum dos termos da esquerda
    # dessa forma, conseguimos provar que n é primo, caso contrário, n é um número composto e passará para a etapa de Pollard's Rho.

    # de forma resumida: temos o valor de n; tomaremos um valor aleatório de a entre 1 e n-1, seguiremos os passos de fatoração e verificaremos a divisibilidade, se n dividir algum dos termos da fatoração, então n provavelmente é primo;
    # porém, a probabilidade está ao nosso lado: conforme testamos valores diferentes de "a", a probabilidade de acertarmos aumenta exponencialmente, na forma 2^{-2 * a}, ou seja, se testarmos por exemplo, 30 valores possíveis de a, a chance do código errar é de 2^{-2 * 30} = 2^{-60}, uma chance absurdamente baixa.
    # dessa forma, basta testar para vários valores de a, e teremos garantia de que o código funcionará. 

    h = n-1 # definido o expoente par, caso n seja primo
    c = 0 # definido o contador

    # executa o loop enquanto h for par
    while h % 2 == 0:
        h //=2 # divide h por 2, garantindo que a saída será inteira
        c += 1 # conta quantas vezes dividimos por 2

    for i in range(20): # realizaremos 20 iterações, que já suficientes para fugir de problemas probabilísticos envolvendo a função
        
        a = random.randint(2, min(n-2, 100000)) # base aleatória entre 2 e n-2 (depois de testar o algoritimo de Pollard's Rho, percebi que 1, n-1 é um intervalo com extremos triviais)
        # outra adição importante foi a função min() para retornar o menor valor entre esse intervalo n-2 e 100000, pra não dar biziu na recursão
        
        x = pow(a, h, n) # calcula a^{n-1} (mod n) [eleva "a" a "h" e obtem o resto da divisão por n]

        # primeira verificação: a^{n-1} = 1 (mod n)
        if x == 1:
            continue 
            # x vai corresponder à a^{n-1}-1 = 0 (mod n) -> o primeiro termo da sequência recursiva
            # ou seja, se n divide a^{n-1}-1, satisfazendo portanto, a propriedade dita, logo, passa no teste

        # segunda verificação: a^{n-1} = -1 (mod n)
        if x == n-1:
            continue 
            # x vai corresponder à a^{n-1}+1 = 0 (mod n) -> o segundo termo da sequência recursiva
            # idem à verificação 1, se dividir a^{n-1}, a propriedade é válida.

        # terceira verificação: recursão de potências
        encontrado = False
        for j in range(c): 
        
            if x == n-1:
                encontrado = True
                break
            x = pow(x, 2, n) 
            # eleva os termos x, ao quadrado, quantas vezes for necessário, satisfazendo x^2 (mod n) -> basicamente segue a sequência recursiva até encontrar um valor ímpar
            
        # vamos basicamente verificar as divisões das potências criadas recursivamente, quando for divisível (assim como na verificação 2), será primo, caso contrário:
        if not encontrado:
            return False # ou seja, n é um número composto e passará para o algorítimo de Pollard's Rho.


def pollards_rho(n, iteracao=0):
    # definida a função do algorítimo;

    # antes de tudo, é melhor explicar que para evitar recursões infinitas, definiremos um número máximo de tentativas, adicionando "1" ao valor de "iteracao" sempre que o teste falhar

    # primeiramente, definiremos o algorítimo de Pollard's Rho: recebido um valor "n" não primo, podemos fatorar ele em fatores primos (ex: 18 = 3 * 3 * 2);
    # para isso, tomaremos um polinômio g(x)=x^2+c (mod n) tal que c é uma constante escolhida aleatoriamente;
    # tomaremos um valor inicial qualquer, por exemplo x_0 = 1;
    # a partir disso, criaremos uma sequência denotada como x_i = g(x_i-c) -> o iésimo valor de i será o valor de seu antecessor aplicado em x^2+c (mod n);
    # a sequência será: {1, g(1), g(g(1)), g(g(g(1))), ...}
    # ou seja, x_i é g^i (x_0)
    # lembrando que (mod n) pega o resto da divisão de x^2+1 por n, então eventualmente os valores começarão a se repetir, em forma de diagrama, a letra grega "rho" semelhante ao nosso "p"
    
    # agora, iremos definir dois numeros que vão variar conforme o algorítimo roda;
    # T (tartaruga), que começará em x_0
    # H (hare, lebre em inglês) que também começará em x_0;
    # a grande diferença está no caminhar: T será iterado 1x a cada valor, tomando a forma T -> g(T) -> g(g(T)) -> ...
    # já H será iterado duas vezes a cada valor, ou seja: H -> g(g(H)) _> g(g(g(g(H)))) -> ...

    # a próxima etapa é criar um método para checar o MDC (máximo de divisor comum) entre (|T-H|, n); -> é necessário aplicar || pois é possível que T-H seja negativo
    # agora, verificaremos se o MDC(T-H, n) > 1;
    # uma das possibilidades é T=H, ou seja, MDC(0, 1) = n e óbviamente n>1
    # agora, na outra possibilidade, chamarei um valor d tal que d=MDC(T-H, n) que não entre na primeira possibilidade;
    # dessa forma, d é um fator de n, mas não é 1 e nem n;

    # eventualmente, os valores que definimos como tartaruga e lebre entrarão no ciclo da sequência, e eventualmente a lebre passará a tartaruga e ambas pararão no mesmo lugar do ciclo;
    # se a tartaruga e a lebre não se encontrarem em primeiro lugar, então, o algorítimo roda;
    # caso a lebre e a tartaruga se encontrem, implicará que T = H (mod n), ou seja, (T-H) é um múltiplo de n, então o MDC(T-H, n) será o próprio n, o que não retorna um fator próprio;
    # em resumo, é muito improvável cairmos em um caso de "colisão" e caso isso ocorra, basta trocar o valor de c ou x_0 -> faremos isso de forma recursiva dentro do programa;

    # agora, após tomar um valor considerado interessante de d, tomaremos a mesma sequência inicial, mas faremos ela da forma x^2+c (mod d), ou seja, queremos o resto da divisão por esse novo valor d;
    # isso cria uma nova sequência semelhante à primeira, mas dessa vez, com um número de elementos menor que d;
    # novamente, caso T = H (mod d), a lebre e a tartaruga se encontraram, e o valor gerado não é um fator próprio;
    # porém, é fácil notar que d < n é sempre válido caso fujamos da primeira condição T = H (mod n), portanto, o ciclo gerado por T = H (mod d) é considerávelmente menor que o primeiro;
    # com exemplos concretos: n = 15, sabemos que d=3 é válido como fator de 15;
    # tomando c=1, temos x^2+1 -> a sequência gerada será: {x_0=1; x_1 = (1)^2+1 (mod 15) = 2; x_2 = (2)^2+1 (mod 15) = 5; x_3 = (5)^2+1 (mod 15) = 26 (mod 15) = 11; x_4 = (11)^2+1 (mod 15) = 122 (mod 15) = 2; 5; 11; ...}
    # perceba o ciclo a partir de x_4;
    # a sequência gerada então é {1, 2, 5, 11, 2, 5, 11, 2, 5, 11, ...}
    # substituindo para ver como a lebre a tartaruga caminham:
    # T_1 = g(1) = 2;
    # H_1 = g(g(1)) = 5;
    # MDC(|5-2|, 15) = 3; como 3<15, o algorítimo funcionou, portanto, d=3;
    # perceba que, agora na sequência com (mod d) ao invés de (mod n), temos:
    # MDC(|5-2|, 3) = MDC(3, 3) -> de fato, 5 = 2 mod (mod 3), porém, a colisão ocorreu antes, quando ainda estávamos em n, não em d, portanto, podemos dar sequência com o código

    # em resumo, criaremos uma sequencia com valores arbitrários para um polinômio, analisaremos o comportamento de duas variáveis que correm pela sequência formada pelo polinômio, e com base no seu comportamento, conseguiremos os divisores subsequentes do número em questão.
 
    
    if iteracao > 50: # basicamente, se atingirmos 50 tentativas, ao invés de fatorar com pollard's rho, tentaremos com força bruta
        limite = min(int(math.sqrt(n)) + 1, 100000) 
        # primeiro, calculamos a parte inteira de sqrt(n) e somamos 1, para garantir que todos os fatores estejam inclusos (ex: int(math.sqrt(15)) = 3, 3+1=4, garantindo que os fatores até 3 estejam inclusos)
        # a função min garante que o limite não se exceda para rodar a força bruta, garantindo que o script não caia em um loop infinito

        for i in range(2, limite): # o loop irá de 2 (o menor primo) até limite-1
            if n % i == 0:
                return i
        return n

        # a propriedade que rege esse loop de força bruta é a seguinte:
        # se n for composto e maior que 1, é possível escrever n=ab com a<=b ou vice-versa;
        # então, pelo menos um dos fatores deve ser <= sqrt(n), já que caso a ou b fossem >= sqrt(n), teríamos que ab >= sqrt(n) * sqrt(n), ou seja, ab >= n, o que não faz sentido, já que inicialmente supomos que a e b fossem fatores de n
        # dessa forma, testaremos divisores de 2 até sqrt(n), e caso n seja composto, haverá ao menos 1 fator para ser encontrado;
    
    if n % 2 == 0:
        return 2 # n % 2 => par, então 2 é um fator de n;

    x_0 = random.randint(2, n-2) # idem ao Miller-Rabin, (1, n-1) tem extremos triviais;

    c = random.randint(1, 10) # definido valor c entre 1 e 10
    def g(x):
        # definido o polinômio g(x)
        return (x**2 + c) % n

    
    # inicilizando a tartaruga e a lebre em valores de x_0:
    T = x_0
    H = x_0

    contador = 0
    while contador < 100000: # loop para executar o ciclo
        T = g(T)
        H = g(g(H))

        diferenca = abs(T-H) # faz o módulo de T-H
        d = math.gcd(diferenca, n) # gcd é o equivalente de MDC no python (e agora fiquei curioso sobre como faríamos isso em C, provavelmente teria de haver outra função só pro MDC)

        if d == n: # os valores colidiram;
            return pollards_rho(n, iteracao+1) # retorna desde ao começo e incrementa 1 para o limite de tentativas;
        elif d > 1: # o fator próprio
            return d


def fatorizar(n):
    # definida a função de fatoração;

    if n == 1:
        return[]

    if eh_primo(n):
        return[n] # se n é primo, a gente só vai printar o valor de n

    # agora, vamos basicamente repetir o processo da função pollards_rho() para d até que não hajam mais fatores;

    fator = pollards_rho(n) # vai encontrar um fator usando pollards rho

    if fator == n:
        return[n]

    # fatora recursivamente o fator e o quociente
    fatores_divisor = fatorizar(fator)
    fatores_quociente = fatorizar(n // fator)

    fatores = fatores_divisor + fatores_quociente
    fatores.sort() # só pra questões de organização

    return fatores
    

def main():
    # definida a função principal;

    print("Bem-vindo ao programa de fatoração de primos!")
    print("O programa pode fatorar números na forma de produtos de números primos.")
    n = int(input("Insira um número positivo maior que 1: "))
    
    while n <= 1:
        print("Insira um valor válido! Tente novamente: ")
        n = int(input("Insira um número positivo maior que 1: "))

    if eh_primo(n):
        print("O número em questão já é primo, portanto, não pode ser fatorado.")
    else:
        print("O algorítimo irá rodar para encontrar seus fatores...")

        fatores = fatorizar(n)
        resultado_formatado = " ".join(map(str, fatores)) # a função map pega e converte todos os fatores em str (caracteres), o join junta todos em uma unica str e os separa por " ".

        print("Seus fatores primos são: %s" %resultado_formatado)

if __name__ == "__main__": # aparentemente a gente precisa disso aqui pra chamar a função main na hora que o código compilar, o padrão em python é que __name__ tem valor "__main__", entao esse if basicamente chama a função main sempre
    main()


# comentários finais:
# utilizei algumas fontes para fazer o trabalho, segue os links:
# https://www.youtube.com/watch?v=7lhlJTtCsiw
# https://www.youtube.com/watch?v=zmhUlVck3J0
# https://artofproblemsolving.com/wiki/index.php/Euclid's_Lemma
# https://mathworld.wolfram.com/FermatsLittleTheorem.html
# boa parte das explicações, analogias e conceitos utilizados foram extraídos daqui
# segue tb o link do github com o arquivo.py:
# https://github.com/MasterT0ad/Fatoracao-em-primos


# esse trabalho nos custou aproxidamente 11h de esforço mental
