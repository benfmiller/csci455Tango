# Final Project - Interactive Game Project

There are a lot of students in this class that are about to graduate next month, congrats. I had several suggestions from students about the FINAL PROJECCT and how to satisfy their Graduation Fever.

So my original idea has changed.

The final project is going to be a Game you can play with your Robot.

Three levels of grading. Each level will have point levels to get to that level.

This final project will be programming an adventure game that you can play with your robot. The adventure is up to you, you just have to follow the steps of the adventure.

I figure you have done a lot of tricky, technical applications up to this point, so I would let you be creative and have fun with this one.

You will use one of the following maps:

### Level 1 (5 modes)
  1
2 3 4
  5

### Level 2 (9 nodes)
1 2 3
6 7 8
11 12 13

### Level 3 (25 nodes)
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25

The map will be in memory in your robot app (2D array is fine). In the adventure game your robot will travel the map and have things happen. Your robot will turn and move according to the map and user input, at each number (node) something will happen......something like ‘ADVENTURE’.......the more interaction and robot animation you can bring to the adventure the more grading points you will earn.

All yellow paths are roads from node to node. Each number is a node where your nodes will encounter things.

Three levels of grading can occur, Level 1, the easy static map, tops out at 75%.

Level two, the medium map, tops out at 86%.

Level three, the large map tops out at 100%.

## All levels have to take an arm and attach it to a body, preferably the bodies that need an arm.

### For level 1-A, 75% will be the perfect score.........
### I call this the “I’m graduating I could care less level”

You will have your robot start in the virtual maze in memory. You will start at Node 1.

You robot will tell the user, with speech, that it sees a path to the South and then ask the user which way they would like to go. ....verbally.

The user can then tell the robot to go South, verbally.

At each intersection these are the things that will happen.

**Robot Movement**: At each intersection if the user chooses South, North, East, or West the robot should turn in the appropriate direction (approx 90 degrees) and move forward a couple of feet.

Node Encounters:

Intersection 3 (according to the map you will hit intersection 3 before 2): The robot will have an encounter with some kind of bad guy that wants to fight. The robot and bad guy take turns taking random hit points off until one dies. Usually the robot should win this fight.......but not always. After the fight is over the robot says “I see a path to the South, North, East, West, which way do you want to go?” User input will make robot go in that direction.

Intersection 2: Box of Gold found, if you have the key to open it, you win the game. If haven’t found key the robot will say I see a box, you have no key, I see a path to the West which way would you like to go. User input will only give chance to go back West.

Intersection 4: More bad guys. Same as intersection 3, except the robot shouldn’t be able to win if it hasn’t gone to intersection 5 yet (unless really, really lucky in first fight). If the robot has gone to intersection 5 then it has been recharged all it’s hit points have been restored and it should win most of the time. After it wins the robot will find a key and then give the paths that it sees. User input will send it on it’s way back to the East.

Intersection 5: Recharging station, all hit points are recharged. Then the only path available is given, North. User input says go North.

After the robot has won at intersection 3, the node becomes just an intersection and the next time there the robot must recognize the paths available and ask the user which way to go. If user takes South back to start the robot should just say nothing is here and give paths available.

## Grading breakdown for Level 1:

The five nodes

    • Start Node (3 points)
    • End Node (4 points)
    • Fight Node (2 nodes) (4 points each)
    • Recharge Node (5 points)
    • Finding key, using on end node (5 points)

Other Points:

    • Proper Robot movement when representing maze: (10 points)
    • Node animations with arm movement (10 points)
    • Screen animations (10 points)
    • Speech Recognition (10 points)
    • Text to Speech (10 points)

This comes out to a total of 75 points.

## Level 2 (Max grade 87%) :

The rules of combat are the same as in Level 1.

There are nine NODES. Your robot must be able to recognize the paths that it is allowed to take at each node it arrives in. The robot should mimic the movements at each nodes at each stage. All user input should be given by voice commands. These are the commands that should be recognized: North, South, East, West, Fight, Run.

The robot should start in a random corner (intersections : 1, 3, 11, 13) and the ending should be in a different random corner.

The nine nodes should consists of these things, and they should all be randomized:

    1. Start
    2. End = but can’t end until key is found.
    3. Recharging station (get all your hit points back)
    4. Four weak bad guys, but can take points from robot.
    5. Two harder bad guys (different type) much harder to beat, need to have all hit points to beat them. One of these two nodes will have the secret key to open the finish line, solve a puzzle to get the key.

After each round of a fight the user gets an update “I have 16 hit points left, the bad guys have 12” or something similar. The user can then choose to run or fight: give input (Run or Fight) if they choose run they get a 75% chance to run away successfully, but 25% chance they have to stay and fight. If they get to run away they get moved to a random node where nothing happens (the content of the node is ignored), but the robot will say which way would you like to go and the directions for that node are given. The user will not know which node they have run too. They will have to figure it out when they move and find something they have seen before.

There should be a total number of moves allowed, for people that just get totally lost and keep backtracking.

Robot stuff for level 2, the robot should turn the proper direction and pretend to follow the path, if you run out of room you can always pick up robot and move it back to middle of room. All movements are relative to where it starts, not to compass points.......but to starting direction on map.

For each type of node you should have movements and images on screen to show relevant encounters. Full body motion, a little arm movement included(don’t break arm), will need to be used for game interactivity. Your robot should act out scenerios to bring the user in to the game.

## Grading level two:

The nine nodes

    • Start Node (3 points)
    • End Node (3 points)
    • Easy Fight Nodes (4 nodes) (3 points each)
    • Hard Fight Nodes (2 nodes) (4 points each)
    • Recharge Node (3 points)
    • Finding key, using on end node (4 points)

Other Points:

    • Proper Robot movement when representing maze: (10 points)
    • Node animations with arm movement (10 points)
    • Screen animations (10 points)
    • Speech Recognition (8 points)
    • Text to Speech (8 points)
    • Losing if takes too many moves (4 points)
    • Fight or Run working (4 points)

This comes out to a total of 87 points.

## Level Three (100% possible)

Use big map.

The start is always on one outside edge of the map, but it is random which edge the start is located, sometimes you might on the east edge, or South edge, etc. etc. Every time you play it will change and any of the outer 16 nodes are randomly eligible (no hard coding). The end node will be on a randomized node on opposite side. If start is on North wall, the end will be somewhere randomly 21-25.

25 Nodes, all nodes are total randomly placed at start up, here are the 25 nodes needed–

    • one start node
    • one finish node, don’t need key anymore with this complexity.
    • 3 charging stations (replenish hit points) These three nodes should be random, but spread out so they’re not too close to each other.
    • 2 coffee shops where wi-fi will give you a hint on which direction you need to go to finish (East, South, West, North). These two nodes should be spread out, never next to each other, but also randomly placed.
    • 6 easy battles. Random number of bad guys (3-6 maybe, something like that)
    • 5 medium battles. Random number of bad guys
    • 3 hard battles. Random number of bad guys
    • 2 fun nodes, be creative.
    • 1 tricky choice type node where you can find the key if you do something correct. Give options and riddle type choice to user.

Same run or fight scenario will happen from level 2. Where this level differs is if your NODE had 5 bad guys on it and you defeat three before having to run because you are about to die, when you return to this node it will be updated to only have two nodes left for the next fight.

Robot stuff for level 3, the robot should turn the proper direction and pretend to follow the path, if you run out of room you can always pick up robot and move it back to middle of room. All movements are relative to where it starts, not to compass points....... but to starting direction on map.

For each type of node you can have movements and images on screen to show relevant encounters. Full body motion, good relevant arm movement without breaking arm, will need to be used for game interactivity. Your robot should act out scenarios to bring the user in to the game.

The 25 nodes

    • Start Node (2 points)
    • End Node (2 points)
    • Easy Fight Nodes (6 nodes) (1 points each)
    • Medium Fight Nodes (5 nodes) (2 points each)
    • Hard Fight Nodes (3 nodes) (2 points each)
    • Recharge Node (3 nodes) (2 points)
    • Coffee shops (2 nodes) 3 points each
    • Fun Nodes (3 nodes) (3 points each)
    • Puzzle node (1 node) (3 points)
    • Finding key, using on end node (4 points)

Other Points:

    • Proper Robot movement when representing maze: (8 points)
    • Node animations with arm movement (8 points)
    • Screen animations (8 points)
    • Speech Recognition (7 points)
    • Text to Speech (7 points)
    • Losing if takes too many moves (3 points)
    • Fight or Run working (4 points)

This comes out to a total of 100 points.

The assignment is due the week of May 2nd to May 6th.

Teams going for level one or two will need to demo Monday.

Teams going for level two will need to demo for Wednesday.

Teams going for the level 3, the big map, will need to demo on Friday.

If you don’t hit your deadline for you level, say level one doesn’t demo until Friday you lost 10% per demo day, or 20% for being two demo days late.
