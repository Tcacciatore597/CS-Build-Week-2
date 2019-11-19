from room import Room
from player import Player
from world import World
from threading import Timer

import random

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.

roomGraph={}

world.loadGraph(roomGraph)
world.printRooms()
player = Player("Name", world.startingRoom)


class Stack():
    def __init__(self):
        self.stack= []

    def add(self, value):
        self.stack.append(value)

    def remove(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    
    def size(self):
        return len(self.stack)


traversalPath = []

visited = {}

s = Stack()


while len(visited) < 500:
    # setting the current room
    current = player.currentRoom.id

    # check if the current room has been visited yet
    # get all available exits in the room
    if current not in visited:
        exits = {}
        
        for exit in player.currentRoom.getExits():
            exits[exit] = '?'

        visited[current] = exits
    
    exits = visited[current]

    if 'e' in exits and exits['e'] == '?':
        player.travel('e')
        traversalPath.append('e')

        # create variable for the next room and assing id of the current room
        next_room = player.currentRoom.id
        
        # set id of next room to exits['nsew']
        exits['e'] = next_room

        # repeat the visited process with next room
        if next_room not in visited:
            next_room_exits = {}

            for exit in player.currentRoom.getExits():
                next_room_exits[exit] = '?'

            next_room_exits['w'] = current

            visited[next_room] = next_room_exits
        else:
            visited[next_room]['w'] = current

        # add 'nsew' to the stack
        s.add('w')

        # check if 'nsew' is an exit and has not been visited
        # move player and add to traversalPath list    
    elif 'n' in exits and exits['n'] == '?':
        player.travel('n')
        traversalPath.append('n')

        next_room = player.currentRoom.id

        exits['n'] = next_room

        if next_room not in visited:
            next_room_exits = {}

            for exit in player.currentRoom.getExits():
                next_room_exits[exit] = '?'

            next_room_exits['s'] = current

            visited[next_room] = next_room_exits
        else:
            visited[next_room]['s'] = current

        s.add('s')
    elif 's' in exits and exits['s'] == '?':
        player.travel('s')
        traversalPath.append('s')

        next_room = player.currentRoom.id
        
        exits['s'] = next_room

        if next_room not in visited:
            next_room_exits = {}

            for exit in player.currentRoom.getExits():
                next_room_exits[exit] = '?'

            next_room_exits['n'] = current

            visited[next_room] = next_room_exits
        else:
            visited[next_room]['n'] = current

        s.add('n')
    elif 'w' in exits and exits['w'] == '?':
        player.travel('w')
        traversalPath.append('w')

        next_room = player.currentRoom.id
        
        exits['w'] = next_room

        if next_room not in visited:
            next_room_exits = {}

            for exit in player.currentRoom.getExits():
                next_room_exits[exit] = '?'

            next_room_exits['e'] = current

            visited[next_room] = next_room_exits
        else:
            visited[next_room]['e'] = current

        s.add('e')
    else:
        back = s.remove()

        if back is None:
            break
        
        player.travel(back)
        traversalPath.append(back)




# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")