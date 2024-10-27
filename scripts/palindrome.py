class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_sorted_lists(l1, l2):
    dummy = ListNode()  # Dummy node to simplify the merging process
    current = dummy

    # Compare nodes of both lists and add the smaller node to the merged list
    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # If any nodes remain in either list, append them to the merged list
    if l1:
        current.next = l1
    elif l2:
        current.next = l2

    return dummy.next  # Return the merged list starting from the first actual node

# Example usage:
# Creating two sample linked lists:
# List 1: 1 -> 2 -> 4
# List 2: 1 -> 3 -> 4
l1 = ListNode(1, ListNode(2, ListNode(4)))
l2 = ListNode(1, ListNode(3, ListNode(4)))

merged_list = merge_two_sorted_lists(l1, l2)

# Print the merged linked list
current = merged_list
while current:
    print(current.val, end=" -> " if current.next else "")
    current = current.next