#include <stdio.h>

int main() {
    int matrix1[2][2], matrix2[2][2], result[2][2];
    int i, j, k;

    printf("Matrix Multiplication\n");
    printf("----------------Matrix: 1----------------\n");

    // Input for Matrix 1
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("Enter elements : ");
            scanf("%d", &matrix1[i][j]);
        }
    }

    // Display Matrix 1
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%d ", matrix1[i][j]);
        }
        printf("\n");
    }

    printf("\n----------------Matrix: 2----------------\n");

    // Input for Matrix 2
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("Enter elements : ");
            scanf("%d", &matrix2[i][j]);
        }
    }

    // Display Matrix 2
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%d ", matrix2[i][j]);
        }
        printf("\n");
    }

    // Initialize result matrix to zero
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            result[i][j] = 0;
        }
    }

    // Matrix multiplication logic
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            for (k = 0; k < 2; k++) {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }

    printf("\n--------Result : Multiplication Matrix--------\n");

    // Display Result Matrix
    for (i = 0; i < 2; i++) {
        for (j = 0; j < 2; j++) {
            printf("%d\t", result[i][j]);
        }
        printf("\n");
    }

    return 0;
}

