import random


class Node:
    number: int = 0

    def __init__(self) -> None:
        pass

    def set_number(self, num):
        self.number = num

    def __str__(self) -> str:
        return str(self.number)


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
    health: float

    def __init__(self) -> None:
        pass


class EasyEnemy(Enemy):
    def __init__(self) -> None:
        self.health = 50


class StrongEnemy(Enemy):
    def __init__(self, has_key=False) -> None:
        self.has_key = has_key
        self.health = 100


class Map:
    full_map = [
        [1, "x", 2, "x", 3],
        [" ", " ", "x", " ", "x"],
        [6, "x", 7, " ", 8],
        ["x", " ", "x", " ", " "],
        [11, " ", 12, "x", 13],
    ]

    direction_map = {
        "front": "north",
        "left": "west",
        "right": "east",
        "behind": "south",
    }
    direction: str
    position: list[int]
    current_node: Node
    state: str  # in fight, moving, just started, all done
    # 9 nodes

    def __init__(self) -> None:
        print("Initializing Map")
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

    def get_input_options(self, only_move=False) -> list[str]:
        Commands_list = [""]

        # Commands_list = [
        #     "north",
        #     "south",
        #     "east",
        #     "west",
        #     "fight",
        #     "run",
        # ]

        # TODO check what current node is,
        # TODO get directions we can go
        # if current node is enemy, fight or run

        current_node: Node = self.full_map[self.position[0]][self.position[1]]
        try:
            if isinstance(self.current_node, Enemy) and self.current_node.health > 0:
                if isinstance(self.current_node, EasyEnemy):
                    Commands_list.append("fight")
                    Commands_list.append("run")
                    # fight easy enemy
                if isinstance(self.current_node, StrongEnemy):
                    Commands_list.append("fight")
                    Commands_list.append("run")
                    # fight hard enemy
                # call fight function or run function
                else:
                    print("current enemy defeated")
            if self.full_map[self.position[0] + 1][self.position[1]] == "x":
                Commands_list.append("east")

                # right exists
            if self.full_map[self.position[0] - 1][self.position[1]] == "x":
                Commands_list.append("west")
                # left exists

            if self.full_map[self.position[0]][self.position[1] + 1] == "x":
                Commands_list.append("north")
                # above exists

            if self.full_map[self.position[0]][self.position[1] - 1] == "x":
                Commands_list.append("south")
                # below exists

        except IndexError:
            print("Out of bounds")

        return Commands_list

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
