class ArrayList:
    """
    ArrayList - динамичен списък.
    Използва се за всички паркирани автомобили.
    """

    def __init__(self):
        self.data = []
        self.size = 0

    def add(self, item):
        self.data.append(item)
        self.size += 1

    def remove(self, item):
        if item in self.data:
            self.data.remove(item)
            self.size -= 1
            return True

        return False

    def get(self, index):
        if 0 <= index < self.size:
            return self.data[index]

        return None

    def contains_plate(self, plate):
        for car in self.data:
            if car.plate == plate:
                return True

        return False

    def find_by_plate(self, plate):
        for car in self.data:
            if car.plate == plate:
                return car

        return None

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.data)