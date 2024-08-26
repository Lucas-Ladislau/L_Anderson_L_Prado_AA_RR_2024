#include <stdio.h>
#include <time.h>
#include <stdlib.h> 

void FazAlgoOtimizado(int n) {
    long contador = 0;
    for (int i = 1; i < n - 1; i++) {
        for (int j = i + 1; j <= n; j++) {
            contador += j; 
        }
    }
    printf("%ld\n", contador);
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
    FazAlgoOtimizado(n);
    fim = clock();

    tempo_decorrido = (double)(fim - inicio) / CLOCKS_PER_SEC;

    printf("%.10f\n", tempo_decorrido);
    return 0;
}
