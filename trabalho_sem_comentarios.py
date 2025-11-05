# o trabalho foi feito por: João Francisco Callegari (ra143496) e Beatriz Miranda da Silva (ra143912)
import math
import random
def eh_primo(n):
    if n < 2:
        return False 

    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if n % p == 0:
            return n == p

    h = n-1
    c = 0

    while h % 2 == 0:
        h //=2 
        c += 1

    for i in range(20):
        a = random.randint(2, min(n-2, 100000)) 
        
        x = pow(a, h, n)
        if x == 1:
            continue 

        if x == n-1:
            continue 

        encontrado = False
        for j in range(c): 
        
            if x == n-1:
                encontrado = True
                break
            x = pow(x, 2, n) 
            
        if not encontrado:
            return False
        
    return True

def pollards_rho(n, iteracao=0):
    if iteracao > 50:
        limite = min(int(math.sqrt(n)) + 1, 100000) 

        for i in range(2, limite):
            if n % i == 0:
                return i
        return n
    
    if n % 2 == 0:
        return 2

    x_0 = random.randint(2, n-2)
    c = random.randint(1, 10)
    
    def g(x):
        return (x**2 + c) % n

    T = x_0
    H = x_0
    contador = 0
    
    while contador < 100000:
        T = g(T)
        H = g(g(H))

        diferenca = abs(T-H) 
        d = math.gcd(diferenca, n)
        
        if d == n: 
            return pollards_rho(n, iteracao+1) 
        elif d > 1: 
            return d
        
        contador += 1

    return pollards_rho(n, iteracao+1)


def fatorizar(n):
    if n == 1:
        return[]

    if eh_primo(n):
        return[n] 

    fator = pollards_rho(n) 
    
    if fator == n:
        return[n]

    fatores_divisor = fatorizar(fator)
    fatores_quociente = fatorizar(n // fator)

    fatores = fatores_divisor + fatores_quociente
    fatores.sort()
    return fatores
    
def main():
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
        resultado_formatado = " ".join(map(str, fatores))

        print("Seus fatores primos são: %s" %resultado_formatado)
        
if __name__ == "__main__":
    main()