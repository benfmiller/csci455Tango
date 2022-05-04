import random


class Node:
    name = "base node"
    number: int = 0

    def __init__(self) -> None:
        pass

    def set_number(self, num):
        self.number = num

    def __str__(self) -> str:
        return str(self.number)


class EndNode(Node):
    name = "End Node"

    def __init__(self) -> None:
        super().__init__()
        self.unlocked = False


class StartNode(Node):
    name = "Start Node"

    def __init__(self) -> None:
        super().__init__()


class RechargingNode(Node):
    name = "Recharging Node"

    def __init__(self) -> None:
        super().__init__()


class Enemy(Node):
    name = "Base Enemy Node"
    damage_multiplier: float

    def __init__(self) -> None:
        super().__init__()
        self.health = 50


class EasyEnemy(Enemy):
    name = "Easy Enemy"

    def __init__(self) -> None:
        super().__init__()
        self.damage_multiplier = 1


class StrongEnemy(Enemy):
    name = "Strong Enemy"

    def __init__(self, has_key=False) -> None:
        super().__init__()
        self.has_key = has_key
        self.damage_multiplier = 2


class Map:
    direction_map = {
        "front": "north",
        "left": "west",
        "right": "east",
        "behind": "south",
    }
    direction: str
    position: list[int]
    current_node: Node

    def __init__(self) -> None:
        print("Initializing Map")
        self.full_map = [
            [1, "x", 2, "x", 3],
            [" ", " ", "x", " ", "x"],
            [4, "x", 5, " ", 6],
            ["x", " ", "x", " ", " "],
            [7, " ", 8, "x", 9],
        ]
        possible_corners = [[0, 0], [0, 4], [4, 0], [4, 4]]
        starting_corner = random.randint(0, 3)
        self.position = possible_corners.pop(starting_corner)
        node_num = self.full_map[self.position[0]][self.position[1]]
        self.current_node = StartNode()
        self.full_map[self.position[0]][self.position[1]] = self.current_node
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

        print("initialized randomized map")
        self.print_map()
        self.set_direction()
        self.update_direction_map()
        print(f"facing {self.direction}")

    def set_direction(self):
        if self.position == [0, 0]:
            possible_directions = ["south", "east"]
        elif self.position == [0, 4]:
            possible_directions = ["south", "west"]
        elif self.position == [4, 0]:
            possible_directions = ["north", "east"]
        else:  # bottom right
            possible_directions = ["north", "west"]
        self.direction = possible_directions[random.randint(0, 1)]

    def update_right(self):
        direction_list = ["north", "east", "south", "west"]
        current_index = direction_list.index(self.direction)
        self.direction = direction_list[(current_index + 1) % 4]
        self.update_direction_map()

    def update_left(self):
        direction_list = ["north", "east", "south", "west"]
        current_index = direction_list.index(self.direction)
        self.direction = direction_list[(current_index - 1) % 4]
        self.update_direction_map()

    def update_direction_map(self):
        direction_list = ["north", "east", "south", "west"]
        current_index = direction_list.index(self.direction)
        self.direction_map["front"] = direction_list[current_index]
        self.direction_map["right"] = direction_list[(current_index + 1) % 4]
        self.direction_map["behind"] = direction_list[(current_index + 2) % 4]
        self.direction_map["left"] = direction_list[(current_index + 3) % 4]

    def check_direction(self, direction) -> bool:
        position_offset_map = {
            "north": [-1, 0],
            "east": [0, 1],
            "south": [1, 0],
            "west": [0, -1],
        }
        offset = position_offset_map[direction]
        new_x = self.position[0] + offset[0]
        new_y = self.position[1] + offset[1]
        if (
            new_x >= 0
            and new_x < len(self.full_map)
            and new_y >= 0
            and new_y < len(self.full_map[0])
            and self.full_map[new_x][new_y] == "x"
        ):
            return True
        return False

    def get_input_options(self, only_move=False) -> list[str]:
        if (
            isinstance(self.current_node, Enemy)
            and self.current_node.health > 0
            and not only_move
        ):
            return ["fight", "run"]
        commands_list = []
        for cardinal in ["north", "east", "south", "west"]:
            if self.check_direction(cardinal):
                commands_list.append(cardinal)
        return commands_list

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

    def attempt_run(self) -> bool:
        if random.random() < 0.75:
            print("Run away successful")
            self.run_away()
            return True
        else:
            print("Run away unsuccessful")
            return False

    def run_away(self):
        positions_index = []
        for x in range(len(self.full_map)):
            for y in range(len(self.full_map[1])):
                if not isinstance(self.full_map[x][y], str) and [x, y] != self.position:
                    positions_index.append([x, y])
        self.position = positions_index[random.randint(0, len(positions_index) - 1)]
        self.current_node = self.full_map[self.position[0]][self.position[1]]

    def get_change_direction(self, direction) -> int:
        if self.direction_map["front"] == direction:
            return 0
        elif self.direction_map["left"] == direction:
            return -1
        elif self.direction_map["right"] == direction:
            return 1
        else:
            return 2

    def update_move_forward(self):
        if self.direction == "north":
            self.position[0] -= 2
        elif self.direction == "south":
            self.position[0] += 2
        elif self.direction == "east":
            self.position[1] += 2
        else:  # west
            self.position[1] -= 2
        self.current_node = self.full_map[self.position[0]][self.position[1]]
        print(self.current_node.__class__)
