# NOTE: Use This as our map constructor file.
# Handles randomness and classes and stuff
# ----------------------------------
# Level 1 Map
L1 = [
    [" ", " ", 1, " ", " "],
    [" ", " ", "x", " ", " "],
    [2, "x", 3, "x", 4],
    [" ", " ", "x", " ", " "],
    [" ", " ", 5, " ", " "],
]
print("Level 1 Map")
for x in L1:
    for y in x:
        print(y, end=" ")
    print()
# ----------------------------------
# Level 2 Memory
L2 = [
    [1, "x", 2, "x", 3],
    [" ", " ", "x", " ", "x"],
    [6, "x", 7, " ", 8],
    ["x", " ", "x", " ", " "],
    [11, " ", 12, "x", 13],
]
print(" ")
print("Level 2 Map")
for x in L2:
    for y in x:
        print(y, end=" ")
    print()
# -----------------------------------
# Level 3 Memory
L3 = [
    [1, "x", 2, "x", 3, " ", 4, "x", 5],
    [" ", " ", "x", " ", "x", " ", " ", " ", "x"],
    [6, "x", 7, " ", 8, " ", 9, "x", 10],
    ["x", " ", "x", " ", " ", " ", "x", " ", "x"],
    [11, " ", 12, "x", 13, "x", 14, " ", 15],
    ["x", " ", " ", " ", " ", " ", "x", " ", "x"],
    [16, "x", 17, " ", 18, " ", 19, "x", 20],
    [" ", " ", "x", " ", "x", " ", "x", 24, 25],
]
print(" ")
print("Level 3 Map")
for x in L3:
    for y in x:
        print(y, end=" ")
    print()


class Map:
    position: list[int]
    state: str  # in fight, moving, just started, all done
    # 9 nodes

    def __init__(self) -> None:
        print("Initializing Map")
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


class Enemy:
    def __init__(self) -> None:
        print("Initialized a Base enemy")


class EasyEnemy(Enemy):
    def __init__(self) -> None:
        print("Initialized an easy enemy")


class StrongEnemy(Enemy):
    def __init__(self) -> None:
        print("Initialized a strong enemy")
