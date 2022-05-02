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
        self.position = possible_corners.pop(starting_corner)
        node_num = self.full_map[self.position[0]][self.position[1]]
        self.full_map[self.position[0]][self.position[1]] = StartNode()
        self.full_map[self.position[0]][self.position[1]].set_number(node_num)

        end_corner = random.randint(0, 2)
        end_position = possible_corners.pop(end_corner)
        node_num = self.full_map[end_position[0]][end_position[1]]
        self.full_map[end_position[0]][end_position[1]] = EndNode()
        self.full_map[end_position[0]][end_position[1]].set_number(node_num)

        remaining_node_list = [
            EasyEnemy(),
            EasyEnemy(),
            EasyEnemy(),
            EasyEnemy(),
            StrongEnemy(has_key=False),
            StrongEnemy(has_key=True),
            RechargingNode(),
        ]
        unset_gen = self.iterate_nonset()
        for i in range(len(remaining_node_list) - 1, -1, -1):
            next_node = remaining_node_list.pop(random.randint(0, i))
            next_node_position = unset_gen.__next__()
            node_num = self.full_map[next_node_position[0]][next_node_position[1]]
            self.full_map[next_node_position[0]][next_node_position[1]] = next_node
            next_node.set_number(node_num)
            print(i)

        print("initialized randomized map")
        self.print_map()

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

    def iterate_nonset(self):
        for x in range(len(self.full_map)):
            for y in range(len(self.full_map[1])):
                if isinstance(self.full_map[x][y], int):
                    yield [x, y]

    def print_map(self):
        print(" ")
        print("Level 2 Map")
        for x in self.full_map:
            for y in x:
                print(y, end=" ")
            print()


class Node:
    number: int = 0

    def __init__(self) -> None:
        pass

    def set_number(self, num):
        self.number = num


class EndNode(Node):
    def __init__(self) -> None:
        super().__init__()
        self.unlocked = False


class StartNode(Node):
    def __init__(self) -> None:
        super().__init__()


class RechargingNode(Node):
    def __init__(self) -> None:
        super().__init__()


class Enemy(Node):
    def __init__(self) -> None:
        pass


class EasyEnemy(Enemy):
    def __init__(self) -> None:
        pass


class StrongEnemy(Enemy):
    def __init__(self, has_key=False) -> None:
        self.has_key = has_key
