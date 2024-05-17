#include <stdio.h>

#define MAX_ANIMALS 10

int main() {
    // Array of animal names (parallel array)
    char names[MAX_ANIMALS][20] = {
        "Lion", "Elephant", "Tiger", "Zebra", "Giraffe",
        "Cheetah", "Gorilla", "Chimpanzee", "Rhinoceros", "Hippopotamus"
    };

    // Array of animal ages (parallel array)
    int ages[MAX_ANIMALS] = {5, 30, 8, 3, 10, 12, 15, 10, 5, 7};

    // Print animal information
    printf("Animal Information:\n");
    for (int i = 0; i < MAX_ANIMALS; i++) {
        printf("Name: %s\tAge: %d\n", names[i], ages[i]);
    }

    return 0;
}