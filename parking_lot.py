class ParkingLot:
    """
    Паркингът е представен като двумерен масив (матрица).

    0 = свободно
    1 = заето
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.matrix = [
            [0 for _ in range(cols)]
            for _ in range(rows)
        ]

    def find_free_spot(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row][col] == 0:
                    return row, col

        return None

    def occupy(self, row, col):
        self.matrix[row][col] = 1

    def free(self, row, col):
        self.matrix[row][col] = 0

    def is_full(self):
        return self.find_free_spot() is None

    def display(self):
        print("\n========== PARKING ==========")

        print("     ", end="")

        for col in range(self.cols):
            print(f"{col + 1:^5}", end="")

        print()

        for row in range(self.rows):
            print(f"{row + 1:^5}", end="")

            for col in range(self.cols):
                if self.matrix[row][col] == 0:
                    print("[   ]", end="")
                else:
                    print("[ X ]", end="")

            print()

        print("=============================")