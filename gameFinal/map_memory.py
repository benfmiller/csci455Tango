import random

Direction = {"Front": "North", "Left": "West", "Right": "East", "Behind": "South"}

# ----------------------------------
# Level 2 Memory
# -----------------------------------
class Map:
    full_map = [
        [1, "x", 2, "x", 3],
        [" ", " ", "x", " ", "x"],
        [6, "x", 7, " ", 8],
        ["x", " ", "x", " ", " "],
        [11, " ", 12, "x", 13],
    ]

    position: list[int]
    state: str  # in fight, moving, just started, all done
    # 9 nodes

    def __init__(self) -> None:
        print("Initializing Map")
        possible_corners = [[0, 0], [0, 4], [4, 0], [4, 4]]
        starting_corner = random.randint(0, 3)
        end_corner = random.randint(0, 2)
        self.position = possible_corners.pop(starting_corner)

        # TODO: create map structure
        # TODO: Random start position in corner
        # TODO: Random ending in different corner

        # Node types
        # Start
        # End
        # Recharging Station
        # Four weak bad guys
        # Two hard bad guys. (need to have all hit points to beat)

    def get_input_options(self):
        ...

    def perform_action(self):
        ...

    def turn(self):
        print(Direction)
        print(Direction["Up"])

        # if robot.turnRight():
        #     Direction["Front"] = "East"
        #     Direction["Left"] = "North"
        #     Direction["Right"] = "South"
        #     Direction["Behind"] = "West"

        # if robot.turnLeft():
        #     Direction["Front"] = "West"
        #     Direction["Left"] = "South"
        #     Direction["Right"] = "North"
        #     Direction["Behind"] = "East"

        # if robot.moveForward():
        #     Direction["Front"] = "North"
        #     Direction["Left"] = "West"
        #     Direction["Right"] = "East"
        #     Direction["Behind"] = "South"

        # if robot.moveBackward():
        #     Direction["Front"] = "South"
        #     Direction["Left"] = "East"
        #     Direction["Right"] = "West"
        #     Direction["Behind"] = "North"

    def print_map(self):
        print(" ")
        print("Level 2 Map")
        for x in self.full_map:
            for y in x:
                print(y, end=" ")
            print()


class Node:
    def __init__(self) -> None:
        pass


class EndNode(Node):
    def __init__(self) -> None:
        super().__init__()
        self.unlocked = False


class Enemy:
    def __init__(self) -> None:
        print("Initialized a Base enemy")


class EasyEnemy(Enemy):
    def __init__(self) -> None:
        print("Initialized an easy enemy")


class StrongEnemy(Enemy):
    def __init__(self) -> None:
        print("Initialized a strong enemy")
