class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, data):
        new_node = Node(data)
        if self.head == None and self.tail == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def remove(self):
        if self.head is None:  # Kuyruk boşsa
            print("Kuyruk zaten boş!")
            return

        self.head = self.head.next

        if self.head is None:  # Kuyruk tamamen boşsa
            self.tail = None  # Kuyruğun sonunu da güncelle

    def Print(self):
        if self.head is None:
            print("Kuyruk boş.")
            return
        curr = self.head
        while curr != None:
            print(curr.data, end=' ')
            curr = curr.next
