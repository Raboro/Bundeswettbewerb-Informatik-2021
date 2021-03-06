class SolveSlidingParkingLot():
    
    def __init__(self, CARS_IN_PARKSLOTS: list[str], BLOCKING_CARS: dict[str: [int, int]]) -> None:
        self.CARS_IN_PARKSLOTS = CARS_IN_PARKSLOTS
        self.BLOCKING_CARS = BLOCKING_CARS
        self.BLOCKING_CARS_POSITIONS = [position for positions in self.BLOCKING_CARS.values() for position in positions]

        #  add car to the list if car in parkslot is blocked by one car
        self.CARS_NEED_MOVES = [car for car_position, car in enumerate(self.CARS_IN_PARKSLOTS)
                                    for blocked_positions in self.BLOCKING_CARS.values()
                                        if car_position in blocked_positions]

        self.result = []
        self.car_position = 0
        self.parkslot_border = [len(self.CARS_IN_PARKSLOTS), 0]
        

    def assign_moves_to_cars(self) -> None:
        """
        assign each car to moves, which are needed, that the car can move out of the slot
        e.g A: B 1 right => For car A, car B needs to be moves one time to the right
        """

        for car in self.CARS_IN_PARKSLOTS:
            if car not in self.CARS_NEED_MOVES:
                self.result.append(f"{car}:")
                continue

            self.car_position = [position for position, value in enumerate(self.CARS_IN_PARKSLOTS) if value == car][0]
                
            #  if only one move is needed, it contains the direction of the move ["left", "right"], else it´s "multiple"
            move_status = self.check_if_car_needs_one_or_multiple_moves()
                
            if move_status == "multiple":
                blocking_cars = self.multiple_moves()
                self.result.append(f"{car}: {blocking_cars}")
                continue

            blocking_car = self.one_move_get_blocking_car()
            self.result.append(f"{car}: {blocking_car} 1 {move_status}")
                

    def check_if_car_needs_one_or_multiple_moves(self) -> str:
        """
        return if the selected car, needs multiple car moves to come out; if not return the direction the blocking car needs to be moved
        """

        #  one slot right blocked && two slots right free && two slots right inside parkslot border
        if self.car_position + 1 in self.BLOCKING_CARS_POSITIONS and self.car_position + 2 not in self.BLOCKING_CARS_POSITIONS and self.car_position + 2 < self.parkslot_border[0]:
            return "right"
        
        #  one slot left blocked && two slots left free && two slots left inside parkslot border
        elif self.car_position - 1 in self.BLOCKING_CARS_POSITIONS and self.car_position - 2 not in self.BLOCKING_CARS_POSITIONS and self.car_position - 2 >= self.parkslot_border[1]:
            return "left"
        
        return "multiple"
    

    def one_move_get_blocking_car(self) -> str:
        """
        return for one move the blocking car, which needs to be moved 
        """

        return [car for car, current_blocking_car_position in self.BLOCKING_CARS.items() if self.car_position in current_blocking_car_position][0]      

    
    def multiple_moves(self) -> str:
        """
        return multiple moves and the cars, which needs to be moved
        """

        moves_needed_per_side, backup_moves_needed_per_side = self.get_moves_needed_per_side()
        range_of_blocking_cars_and_side = self.find_range_of_blocking_cars_and_side(moves_needed_per_side, backup_moves_needed_per_side)
        blocking_cars = self.get_multiple_cars_need_to_move(range_of_blocking_cars_and_side)
        return blocking_cars


    def get_moves_needed_per_side(self) -> list[int, int]:
        """
        return moves needed per side that the selected car can go out and backup, which is the same
        e.g if return [1, 2] => left side one or right side two spaces are needed
        """

        blocking_car_positions = [blocked_positions for blocked_positions in self.BLOCKING_CARS.values() if self.car_position in blocked_positions][0]
        return [[1, 2], [1, 2]] if self.car_position == blocking_car_positions[1] else [[2, 1], [2, 1]]


    def find_range_of_blocking_cars_and_side(self, moves_needed_per_side: list[int, int], backup_moves_needed_per_side: list[int, int]) -> list[int, str, int]:
        """
        return if the side, where the cars, which needs to be moved are (left or right) and return up to which position these cars are and the moves the directly blocking car needs to do
        e.g if return [1, "left", 1] => up to position 1 from the position of the current car on the left side, these cars and the directly blocking car needs to be moved, directly blocking car needs to move 1 field
        """

        position_changer = 0
        while True:
            #  car_position - position_changer is free space && inside parkslot border (left)
            if self.car_position - position_changer not in self.BLOCKING_CARS_POSITIONS and self.car_position - position_changer >= self.parkslot_border[1]:
                moves_needed_per_side[0] -= 1

            #  car_position + position_changer is free space && inside parkslot border (right)
            if self.car_position + position_changer not in self.BLOCKING_CARS_POSITIONS and self.car_position + position_changer < self.parkslot_border[0]:
                moves_needed_per_side[1] -= 1

            #  if one side got enough space and is the fastest one
            if moves_needed_per_side[0] == 0 or moves_needed_per_side[1] == 0:
                return [self.car_position - position_changer - 1, "left", backup_moves_needed_per_side[0]] if moves_needed_per_side[0] == 0 else [self.car_position + position_changer + 1, "right", backup_moves_needed_per_side[1]]

            position_changer += 1

        
    def get_multiple_cars_need_to_move(self, range_of_blocking_cars_and_side: list[int ,str, int]) -> str:
        """
        return the cars, which need to be moved
        e.g "E 1 left, F 2 left" => car E needs to move 1 left and car F needs to move 2 left
        """
        
        directly_blocking_car = [[car, positions] for car, positions in self.BLOCKING_CARS.items() 
                                                  for position in positions 
                                                        if position == self.car_position][0]

        if range_of_blocking_cars_and_side[1] == "left":
            #  add car to blocking_cars if their positions in the range_of_blocking_cars_and_side[0] && on the left side from the current car and their not the directly_blocking_car 
            blocking_cars = [car for car, positions in self.BLOCKING_CARS.items() 
                                 for position in positions 
                                    if position >= range_of_blocking_cars_and_side[0] and position < self.car_position and car != directly_blocking_car[0]]
        
        else: 
            #  add car to blocking_cars if their positions in the range_of_blocking_cars_and_side[0] && on the right side from the current car and their not the directly_blocking_car 
            blocking_cars = [car for car, positions in self.BLOCKING_CARS.items() 
                                 for position in positions 
                                    if position <= range_of_blocking_cars_and_side[0] and position > self.car_position and car != directly_blocking_car[0]]

        car_result = []
        cleaned_blocking_cars = list(dict.fromkeys(blocking_cars))  # remove double elements

        if range_of_blocking_cars_and_side[1] == "right":
            cleaned_blocking_cars = cleaned_blocking_cars[::-1]

        for blocking_car in cleaned_blocking_cars:
            if range_of_blocking_cars_and_side[1] == "right":
                #  if one right field of the blocking_car is free or two right fields are the parkslot border
                if [positions for car, positions in self.BLOCKING_CARS.items() if car == blocking_car][0][1] + 1 in self.BLOCKING_CARS_POSITIONS or [positions for car, positions in self.BLOCKING_CARS.items() if car == blocking_car][0][1] + 2 >= self.parkslot_border[0]:
                    car_result.append(f"{blocking_car} 1 {range_of_blocking_cars_and_side[1]}, ")
                    continue

                car_result.append(f"{blocking_car} 2 {range_of_blocking_cars_and_side[1]}, ")  # two right fields of the blocking_car are free

            else:
                #  if one left field of the blocking_car is free or two left fields is the parkslot border
                if [positions for car, positions in self.BLOCKING_CARS.items() if car == blocking_car][0][0] - 1 in self.BLOCKING_CARS_POSITIONS or [positions for car, positions in self.BLOCKING_CARS.items() if car == blocking_car][0][0] - 2 < self.parkslot_border[1]:
                    car_result.append(f"{blocking_car} 1 {range_of_blocking_cars_and_side[1]}, ")
                    continue

                car_result.append(f"{blocking_car} 2 {range_of_blocking_cars_and_side[1]}, ") # two left fields of the blocking_car are free

        car_result.append(f"{directly_blocking_car[0]} {range_of_blocking_cars_and_side[2]} {range_of_blocking_cars_and_side[1]}")
        return "".join(car_result)