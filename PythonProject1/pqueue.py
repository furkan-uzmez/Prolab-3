class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, value, priority):
        self.queue.append((priority, value))
        self.queue.sort(key=lambda x: x[0])
    def pop(self):
        if not self.queue:
            raise IndexError("Kuyruk boş")
        return self.queue.pop(0)
    def is_empty(self):
        return len(self.queue) == 0
    def toString(self):
        string = ""
        for priority, value in self.queue:
            string += str(value) + ": " + str(priority) + "\n"
        return string