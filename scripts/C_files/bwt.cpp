#include <string.h>
#include <stdio.h>
#include <stdlib.h>

const char DOLLAR = '$'; // Delimiter character used in the BWT

// Function to compare two strings for qsort
int compareStrings(const void *a, const void *b)
{
    char *aa = *(char **)a;
    char *bb = *(char **)b;
    return strcmp(aa, bb);
}

// Function to perform the Burrows-Wheeler Transform
int bwt(const char *s, char r[])
{
    int i, len = strlen(s) + 1; // Length of the input string plus the dollar sign
    char *ss, *str;
    char **table;

    // Check if the input string contains a dollar sign
    if (strchr(s, DOLLAR))
    {
        return 1; // Return an error if it does
    }

    printf("Original string: %s\n", s);

    // Allocate memory for the string with the dollar sign appended
    ss = calloc(len + 1, sizeof(char));
    sprintf(ss, "%s%c", s, DOLLAR); // Append the dollar sign to the string
    printf("String with dollar sign: %s\n", ss);

    // Allocate memory for the table of rotations
    table = malloc(len * sizeof(const char *));
    for (i = 0; i < len; ++i)
    {
        str = calloc(len + 1, sizeof(char)); // Allocate memory for each rotation
        strcpy(str, ss + i); // Copy the rotated part of the string
        if (i > 0)
        {
            strncat(str, ss, i); // Append the beginning part of the string to complete the rotation
        }
        table[i] = str; // Store the rotation in the table
        printf("Rotation %d: %s\n", i, str);
    }

    // Sort the rotations lexicographically
    qsort(table, len, sizeof(const char *), compareStrings);
    printf("Sorted rotations:\n");
    for (i = 0; i < len; ++i)
    {
        printf("%s\n", table[i]);
    }

    // Construct the BWT result from the last column of the sorted rotations
    for (i = 0; i < len; ++i)
    {
        r[i] = table[i][len - 1];
        free(table[i]); // Free the memory for each rotation
    }
    free(table); // Free the table memory
    free(ss); // Free the ss string memory
    return 0;
}

// Function to perform the inverse Burrows-Wheeler Transform
void ibwt(const char *r, char s[])
{
    int i, j, len = strlen(r); // Length of the encoded string
    char **table = malloc(len * sizeof(const char *)); // Allocate memory for the table
    for (i = 0; i < len; ++i)
    {
        table[i] = calloc(len + 1, sizeof(char)); // Allocate memory for each row in the table
    }

    printf("Encoded string: %s\n", r);

    // Create rotations from the encoded string
    for (i = 0; i < len; ++i)
    {
        for (j = 0; j < len; ++j)
        {
            memmove(table[j] + 1, table[j], len); // Shift existing characters right
            table[j][0] = r[j]; // Prepend the character from the encoded string
        }
        // Print the entire table after creating a rotation
        for (int k = 0; k < len; ++k)
        {
            printf("%s\n", table[k]);
        }
        // Sort the table lexicographically after each rotation
        qsort(table, len, sizeof(const char *), compareStrings);
    }

    // Find the row that ends with the dollar sign to get the original string
    for (i = 0; i < len; ++i)
    {
        if (table[i][len - 1] == DOLLAR)
        {
            strncpy(s, table[i], len - 1); // Copy the original string without the dollar sign
            break;
        }
    }

    // Free the allocated memory for the table
    for (i = 0; i < len; ++i)
    {
        free(table[i]);
    }
    free(table);
}

int main()
{
    int i, res, len;
    char *s, *r;

    // Prompt the user for input
    printf("Enter a word: ");
    s = calloc(100, sizeof(char)); // Allocate enough space for user input
    fgets(s, 100, stdin); // Read user input with fgets to handle spaces

    // Remove trailing newline character (if present)
    len = strlen(s);
    if (s[len - 1] == '\n')
    {
        s[len - 1] = '\0';
    }

    r = calloc(len + 2, sizeof(char)); // Allocate space for the BWT result

    printf("Original word: %s\n", s);
    printf(" --> ");

    // Perform the Burrows-Wheeler Transform
    res = bwt(s, r);
    if (res == 1)
    {
        printf("ERROR: String can't contain dollar sign ($)\n");
    }
    else
    {
        printf("%s\n", r);
    }

    // Allocate new memory for the decoded string
    s = calloc(len + 1, sizeof(char)); 
    // Perform the inverse Burrows-Wheeler Transform
    ibwt(r, s);
    printf(" --> %s\n", s);

    // Free allocated memory
    free(s);
    free(r);
    return 0;
}