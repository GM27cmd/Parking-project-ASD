from car import Car
from array_list import ArrayList
from stack import Stack
from queue import Queue
from parking_lot import ParkingLot


class ParkingManager:

    def __init__(self, rows, cols):
        self.parking = ParkingLot(rows, cols)

        # ArrayList
        self.cars = ArrayList()

        # Queue
        self.waiting_queue = Queue()

        # Stack
        self.history = Stack()

    # =====================================================
    # ADD CAR
    # =====================================================

    def add_car(self, plate, brand, model):

        if self.cars.contains_plate(plate):
            print("Автомобилът вече е паркиран.")
            return

        for waiting_car in self.waiting_queue:
            if waiting_car.plate == plate:
                print("Този автомобил вече чака.")
                return

        car = Car(plate, brand, model)

        free_spot = self.parking.find_free_spot()

        # -------------------------------------------------
        # НЯМА СВОБОДНО МЯСТО
        # -------------------------------------------------

        if free_spot is None:

            self.waiting_queue.enqueue(car)

            self.history.push({
                "type": "queue_add",
                "car": car
            })

            print("\nНяма свободни места.")
            print("Автомобилът е добавен в Queue.")

            return

        # -------------------------------------------------
        # ИМА СВОБОДНО МЯСТО
        # -------------------------------------------------

        row, col = free_spot

        self.parking.occupy(row, col)

        car.row = row
        car.col = col

        self.cars.add(car)

        self.history.push({
            "type": "add_car",
            "car": car
        })

        print(
            f"\nАвтомобилът {plate} е паркиран "
            f"на място [{row + 1}][{col + 1}]."
        )

    # =====================================================
    # REMOVE CAR
    # =====================================================

    def remove_car(self, plate):

        car = self.cars.find_by_plate(plate)

        if car is None:
            print("Автомобилът не е намерен.")
            return

        row = car.row
        col = car.col

        removed_car = car
        promoted_car = None

        # Освобождаваме мястото
        self.parking.free(row, col)
        self.cars.remove(car)

        # -------------------------------------------------
        # АКО ИМА ЧАКАЩ АВТОМОБИЛ
        # -------------------------------------------------

        if not self.waiting_queue.is_empty():

            next_car = self.waiting_queue.dequeue()

            next_car.row = row
            next_car.col = col

            self.parking.occupy(row, col)
            self.cars.add(next_car)

            promoted_car = next_car

            print(
                f"\nАвтомобилът {plate} е премахнат."
            )

            print(
                f"Чакащият автомобил {next_car.plate} "
                f"е паркиран на място "
                f"[{row + 1}][{col + 1}]."
            )

        else:
            print(
                f"\nАвтомобилът {plate} е премахнат."
            )

        # -------------------------------------------------
        # ЕДНО ПОТРЕБИТЕЛСКО ДЕЙСТВИЕ = ЕДИН STACK ЕЛЕМЕНТ
        # -------------------------------------------------

        self.history.push({
            "type": "remove_car",
            "removed_car": removed_car,
            "promoted_car": promoted_car,
            "row": row,
            "col": col
        })

    # =====================================================
    # SHOW CARS
    # =====================================================

    def show_cars(self):

        print("\n========== АВТОМОБИЛИ ==========")

        if len(self.cars) == 0:
            print("Няма паркирани автомобили.")
            return

        for index, car in enumerate(self.cars, start=1):
            print(f"{index}. {car}")

    # =====================================================
    # SHOW QUEUE
    # =====================================================

    def show_queue(self):

        print("\n========== WAITING QUEUE ==========")

        if self.waiting_queue.is_empty():
            print("Няма чакащи автомобили.")
            return

        for index, car in enumerate(self.waiting_queue, start=1):
            print(f"{index}. {car}")

    # =====================================================
    # SEARCH CAR
    # =====================================================

    def search_car(self, plate):

        car = self.cars.find_by_plate(plate)

        if car is not None:
            print("\nАвтомобилът е намерен:")
            print(car)
            return

        for waiting_car in self.waiting_queue:
            if waiting_car.plate == plate:
                print("\nАвтомобилът е в Queue и чака.")
                print(waiting_car)
                return

        print("Автомобилът не е намерен.")

    # =====================================================
    # UNDO
    # =====================================================

    def undo(self):

        action = self.history.pop()

        if action is None:
            print("\nНяма действия за Undo.")
            return

        action_type = action["type"]

        # -------------------------------------------------
        # UNDO ADD CAR
        # -------------------------------------------------

        if action_type == "add_car":

            car = action["car"]

            current_car = self.cars.find_by_plate(car.plate)

            if current_car is not None:

                self.parking.free(car.row, car.col)
                self.cars.remove(car)

                print(
                    f"\nUndo успешно:"
                    f"\nПаркирането на {car.plate} е отменено."
                    f"\nОсвободено място "
                    f"[{car.row + 1}][{car.col + 1}]."
                )

        # -------------------------------------------------
        # UNDO QUEUE ADD
        # -------------------------------------------------

        elif action_type == "queue_add":

            car = action["car"]

            if self.waiting_queue.remove(car):

                print(
                    f"\nUndo успешно:"
                    f"\nДобавянето на {car.plate} "
                    f"в Queue е отменено."
                )

        # -------------------------------------------------
        # UNDO REMOVE CAR
        # -------------------------------------------------

        elif action_type == "remove_car":

            removed_car = action["removed_car"]
            promoted_car = action["promoted_car"]
            row = action["row"]
            col = action["col"]

            # ---------------------------------------------
            # Връщаме автоматично преместения автомобил
            # обратно в Queue
            # ---------------------------------------------

            if promoted_car is not None:

                current_promoted = (
                    self.cars.find_by_plate(
                        promoted_car.plate
                    )
                )

                if current_promoted is not None:

                    self.cars.remove(promoted_car)

                    self.parking.free(
                        promoted_car.row,
                        promoted_car.col
                    )

                promoted_car.row = -1
                promoted_car.col = -1

                self.waiting_queue.enqueue_front(
                    promoted_car
                )

            # ---------------------------------------------
            # Връщаме премахнатия автомобил
            # ---------------------------------------------

            removed_car.row = row
            removed_car.col = col

            self.parking.occupy(row, col)
            self.cars.add(removed_car)

            print(
                f"\nUndo успешно:"
                f"\nПремахването на {removed_car.plate} "
                f"е отменено."
            )

            if promoted_car is not None:

                print(
                    f"Автомобилът {promoted_car.plate} "
                    f"е върнат обратно в Queue."
                )

    # =====================================================
    # SHOW HISTORY
    # =====================================================

    def show_history(self):

        print("\n========== HISTORY ==========")

        if self.history.is_empty():
            print("Няма действия в историята.")
            return

        total = len(self.history.items)

        for index, action in enumerate(
                reversed(self.history.items),
                start=1
        ):

            history_number = total - index + 1

            if action["type"] == "add_car":

                car = action["car"]

                print(
                    f"{history_number}. "
                    f"ADD CAR - {car.plate}"
                )

            elif action["type"] == "queue_add":

                car = action["car"]

                print(
                    f"{history_number}. "
                    f"ADD TO QUEUE - {car.plate}"
                )

            elif action["type"] == "remove_car":

                removed_car = action["removed_car"]
                promoted_car = action["promoted_car"]

                if promoted_car is not None:

                    print(
                        f"{history_number}. "
                        f"REMOVE - {removed_car.plate} "
                        f"(Queue -> {promoted_car.plate})"
                    )

                else:

                    print(
                        f"{history_number}. "
                        f"REMOVE - {removed_car.plate}"
                    )

        print(
            "\nПоследното действие е най-отгоре "
            "и ще бъде отменено от Undo."
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        total_places = (
            self.parking.rows *
            self.parking.cols
        )

        occupied_places = len(self.cars)
        free_places = total_places - occupied_places
        waiting_cars = len(self.waiting_queue)

        print("\n========== STATISTICS ==========")
        print(f"Общо места:        {total_places}")
        print(f"Заети места:       {occupied_places}")
        print(f"Свободни места:    {free_places}")
        print(f"Чакащи автомобили: {waiting_cars}")