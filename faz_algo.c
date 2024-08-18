#include <stdio.h>

void FazAlgo(int n) {
    int i, j, k;
    for (i = 1; i < n - 1; i++) {
        for (j = i + 1; j <= n; j++) {
            for (k = 1; k <= j; k++) {
                printf("i = %d, j = %d, k = %d\n", i, j, k);
            }
        }
    }
}

int main() {
    int n = 5; 
    FazAlgo(n);
    return 0;
}
