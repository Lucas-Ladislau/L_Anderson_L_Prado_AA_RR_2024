#include <stdio.h>
#include <time.h>
#include <stdlib.h> 

void FazAlgo(int n) {
    int i, j, k;
    int contador = 0; 

    for (i = 1; i < n - 1; i++) {
        for (j = i + 1; j <= n; j++) {
            for (k = 1; k <= j; k++) {
                contador++; 
            }
        }
    }

    // printf("%d\n", contador);
}

int main(int argc, char *argv[]) {
    clock_t inicio, fim;
    double tempo_decorrido;
    if (argc != 2) {
        printf("Usage: %s <n>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    
    inicio = clock();

    FazAlgo(n);

    fim = clock();

    tempo_decorrido = (double)(fim - inicio) / CLOCKS_PER_SEC;

    printf("%.10f\n", tempo_decorrido);

    return 0;
}
