# Análise de Algoritmos - FazAlgo
Repositório contém o código do algoritmo denominado FazAlgo que será utilizada no seminário de apresentação da disciplina de Análise de algoritmo. 

O objetivo principal é demonstrar a análise de complexidade em termos de custo computacional, considerando diferentes tamanhos de entrada

## Algoritmo
```
void FazAlgo (int n) {
    int i, j, k;
    FOR (i= 1; i<n - 1; i++) {
        FOR (j= i + 1; j<= n; j++) {
            FOR (k = 1; k<=j;k++) {
                Algum comando de custo O(1)
            } 
        } 
    }
}
```

## Extração de custo e complexidade
```
FOR (i= 1; i<n - 1; i++)
```
O laço externo começa em i = 1 e vai até i < n - 1, o que significa que ele itera `n - 2` vezes.

```
FOR (j= i + 1; j<= n; j++)
```

O laço médio depende do valor de i. Ele começa em j = i + 1 e vai até `j = n`.

```
FOR (k = 1; k<=j;k++)
```

E por ultimo o laço interno começa em k = 1 e vai até k = j, fazendo j iterações para um valor fixo de `j`. Portanto, o custo total é a soma das operações realizadas por todos os laços:
$$
C(n) = \sum_{i=1}^{n-2} \sum_{j=i+1}^{n} \sum_{k=1}^{j} O(1)
$$

**Laço mais interno (em k):**

$$
\sum_{k=1}^{j} 1 = j
$$

O número de operações dentro do laço mais interno é simplesmente \( j \).

**Laço do meio (em j):**

$$
\sum_{j=i+1}^{n} j
$$

Essa soma é uma soma de inteiros consecutivos. Podemos usar a fórmula para a soma dos primeiros mm inteiros. Portanto:

$$
\sum_{j=i+1}^{n} j = \frac{n(n+1)}{2} - \frac{i(i+1)}{2}
$$

**Laço externo (em i):**

$$
C(n) = \sum_{i=1}^{n-2} \left(\frac{n(n+1)}{2} - \frac{i(i+1)}{2}\right)
$$

### Simplificação para a Complexidade

Podemos simplificar o termo dominante para encontrar a função exata de custo:

$$
C(n) = \sum_{i=1}^{n-2} \frac{n(n+1)}{2} - \sum_{i=1}^{n-2} \frac{i(i+1)}{2}
$$

O primeiro termo, somado para \( i=1 \) até \( n-2 \), é:

$$
\sum_{i=1}^{n-2} \frac{n(n+1)}{2} = \frac{(n-2) \cdot n(n+1)}{2} = \frac{n(n+1)(n-2)}{2}
$$

O segundo termo é uma soma de quadrados que pode ser aproximada por:

$$
\sum_{i=1}^{n-2} \frac{i(i+1)}{2} \approx \frac{1}{2} \sum_{i=1}^{n-2} \left(i^2 + i\right)
$$

Usando somas conhecidas, temos:

$$
\sum_{i=1}^{n-2} i^2 \approx \frac{(n-2)(n-1)(2n-3)}{6}
$$

E

$$
\sum_{i=1}^{n-2} i \approx \frac{(n-2)(n-1)}{2}
$$

Juntando todos esses termos, a função de custo exata se aproxima de:

$$
C(n) \approx \frac{n(n+1)(n-2)}{2} - \frac{1}{2} \left(\frac{(n-2)(n-1)(2n-3)}{6} + \frac{(n-2)(n-1)}{2}\right)
$$

Multiplicando e combinando os termos cúbicos e quadráticos, chegamos à fórmula final simplificada:

$$
C(n) = \frac{1}{3}n^3 - \frac{4}{3}n
$$

Por simplicidade, sabendo que C(n) tem um comportamento cúbico, podemos definir a complexidade como sendo:
$$
O(n^3)
$$

## To Do List

- [X] ~~Função de custo e complexidade~~
- [X] ~~Código em C do algoritmo proposto~~
- [X] ~~Experimentação com a execução do algoritmo com diferentes entradas e coleta de tempo de execução~~
- [ ] Gráfico de linha com o tempo de execução em relação a cada entrada e análise da tendência de comportamente  assintótico
- [ ] Apresentar um algoritmo que seja mais eficiente, em termos de complexidade, do que o algoritmo análisado