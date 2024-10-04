import random
import copy

# stack for undo storage
class Node:
    def __init__(self, data):
        self.data = data
        self.nextnode = None

    def showInfo(self):
        print("Node Info --> " + str(self.data))

class Undo:
    def __init__(self):
        self.top = None

    def push(self, newnode):
        newnode.nextnode = self.top
        self.top = newnode

    def peek(self):
        return self.top

    def pop(self):
        if self.top is None:
            return None
        else:
            s = self.top
            self.top = self.top.nextnode
            return s

# Constants
NUM_BALLS_PER_TUBE = 4
NUM_TUBES = 6
NUM_COLORS = 4
BALL_COLORS = ["#ff3131", "#38b6ff", "#00bf63", "#ffde59", "green"]

# Game logic
def generate_tubes():
    colors = []
    for color in range(NUM_COLORS):
        colors.extend([color] * NUM_BALLS_PER_TUBE)

    random.shuffle(colors)
    tubes = []
    index = 0
    for _ in range(NUM_TUBES):
        if index < len(colors):
            tubes.append(colors[index:index + NUM_BALLS_PER_TUBE])
            index += NUM_BALLS_PER_TUBE
        else:
            tubes.append([])  # Empty tube
    return tubes

# conditon to check move is valid or not
def is_valid_move(tubes, tube_from, tube_to):
    if not tubes[tube_from]:  # tube_from is empty
        return False
    if not tubes[tube_to]:  # tube_to is empty
        return True
    if len(tubes[tube_to]) >= NUM_BALLS_PER_TUBE:  # tube_to cannot hold more than 4 balls
        return False
    return tubes[tube_from][0] == tubes[tube_to][0]  # Colors must match

# Make a move
def make_move(tubes, tube_from, tube_to):
    if is_valid_move(tubes, tube_from, tube_to):
        ball = tubes[tube_from].pop(0)  # Remove ball from tube_from
        tubes[tube_to].insert(0, ball)  # Add ball to tube_to
        return True
    return False

# Check if the game is won
def is_game_won(tubes):
    for tube in tubes:
        if tube and (len(tube) != NUM_BALLS_PER_TUBE or len(set(tube)) > 1):
            return False
    return True
