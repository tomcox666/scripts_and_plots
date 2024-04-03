//to run make sure to compile, gcc -o sorted_insert sorted_insert.c, then run, ./sorted_instert.c

#include <stdio.h>
#include <stdlib.h>  // Include <stdlib.h> for malloc

// Define the student struct
typedef struct Student {
    int rollno;
    struct Student* next;
} student;

// Declare the head pointer globally
student* head = NULL;

// Function to create a new node
student* createNode(int rollno) {
    student* newNode = (student*)malloc(sizeof(student));
    newNode->rollno = rollno;
    newNode->next = NULL;
    return newNode;
}

// Function to insert a new node into the linked list in sorted order
void sortedInsert(int rollno) {
    // Create a new node
    student* p = createNode(rollno);

    // If the list is empty or the new node should be inserted at the beginning
    if (head == NULL || head->rollno >= p->rollno) {
        p->next = head; // Set the next of the new node to the current head
        head = p;       // Update the head to point to the new node
    } else {
        // Find the correct position to insert the new node
        student* current = head;
        while (current->next != NULL && current->next->rollno < p->rollno) {
            current = current->next;
        }
        p->next = current->next; // Set the next of the new node to the next of the current node
        current->next = p;       // Update the next of the current node to point to the new node
    }
}

// Function to print the linked list
void printList() {
    printf("Linked list: ");
    student* temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->rollno);
        temp = temp->next;
    }
    printf("NULL\n");
}

int main() {
    // Test the sortedInsert function
    printf("Testing sortedInsert function...\n");

    // Inserting roll numbers
    sortedInsert(1);
    sortedInsert(2);
    sortedInsert(3);
    sortedInsert(5);

    // Print the updated linked list
    printList();

    // Inserting roll number 4
    printf("\nInserting roll number 4...\n");
    sortedInsert(4);

    // Print the updated linked list
    printList();

    return 0;
}
