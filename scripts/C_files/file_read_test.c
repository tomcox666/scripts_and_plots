//Method A
/*#include <stdio.h>
#include <stdlib.h>

// Function to read numeric data (int or float) from a file
int read_data_from_file(const char *filename, int *array, int max_size) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error opening file: %s\n", filename);
        return -1; // Indicate error
    }

    int count = 0;
    while (fscanf(fp, "%d", &array[count]) == 1 && count < max_size) {
        count++;
    }

    fclose(fp);
    return count; // Number of elements read
}

int main() {
    int data[100];
    int num_elements = read_data_from_file("file_read_data.txt", data, 100);

    if (num_elements == -1) {
        // Handle error (e.g., print an error message)
    } else {
        printf("Read %d elements:\n", num_elements);
        for (int i = 0; i < num_elements; i++) {
            printf("%d ", data[i]);
        }
        printf("\n");
    }

    return 0;
}*/

//Model B
#include <stdio.h>
#include <stdlib.h>

int read_data_from_file(const char *filename, int *array, int max_size) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        return -1; // Error opening file
    }

    int count = 0;
    int num;
    while (fscanf(fp, "%d", &num) == 1 && count < max_size) {
        array[count] = num;
        count++;
    }

    fclose(fp);
    return count; // Return the number of elements read
}

int main() {
    int data_array[100]; // Array to store data
    int count = read_data_from_file("file_read_data.txt", data_array, 100);

    if (count == -1) {
        printf("Error reading file.\n");
    } else {
        printf("Read %d values from the file:\n", count);
        for (int i = 0; i < count; i++) {
            printf("%d ", data_array[i]);
        }
        printf("\n");
    }

    return 0;
}