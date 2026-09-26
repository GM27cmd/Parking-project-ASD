class Queue:
    """
    Queue - FIFO.
    Използва се за автомобилите, които чакат за свободно място.
    """

    def __init__(self):
        self.items = []
        self.front_index = 0

    def enqueue(self, item):
        self.items.append(item)

    def enqueue_front(self, item):
        """
        Връща елемент в началото на Queue.
        Използва се при Undo.
        """
        self.items.insert(self.front_index, item)

    def dequeue(self):
        if self.is_empty():
            return None

        item = self.items[self.front_index]
        self.front_index += 1

        if self.front_index >= len(self.items):
            self.items = []
            self.front_index = 0

        return item

    def remove(self, item):
        """
        Премахва конкретен елемент от Queue.
        """

        active_items = self.items[self.front_index:]

        for index, current_item in enumerate(active_items):
            if current_item is item:
                del self.items[self.front_index + index]

                if self.front_index >= len(self.items):
                    self.items = []
                    self.front_index = 0

                return True

        return False

    def is_empty(self):
        return self.front_index >= len(self.items)

    def __len__(self):
        return len(self.items) - self.front_index

    def __iter__(self):
        return iter(self.items[self.front_index:])