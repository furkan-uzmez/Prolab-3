class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, value, priority):
        self.queue.append((priority, value))
        for i in range(len(self.queue)):
            for j in range(0, len(self.queue) - i - 1):
                if self.queue[j][0] > self.queue[j + 1][0]:
                    # Swap işlemi
                    self.queue[j], self.queue[j + 1] = self.queue[j + 1], self.queue[j]

    def pop(self):
        if not self.queue:
            raise IndexError("Kuyruk boş")
        return self.queue.pop(0)[1]
    def is_empty(self):
        return len(self.queue) == 0
    def toString(self):
        string = ""
        for priority, value in self.queue:
            string += str(value) + ": " + str(priority) + "\n"
        return string