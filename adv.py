
import requests
import time

url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"

class Adventure:
    def __init__(self):
        self.roomDict = dict()
        self.currentRoom = 0
        self.exits = []
        self.roomTitle = ""
        self.cooldown = 15

    def traverse(self):
        path = []
        backTrack = []

    #setup starting room 0
        self.roomDict[self.currentRoom] = ["n", "s", "e", "w"]
        self.roomTitle = "A Bright Room"
        self.exits = ["n", "s", "e", "w"]

        while self.roomTitle != "Pirate Ry":

    # while len(self.roomDict) < 499:
    
            time.sleep(self.cooldown + 1)

            if self.currentRoom not in self.roomDict:
                currentID = self.currentRoom
                exits = self.exits
                self.roomDict[currentID] = exits
                self.roomDict[currentID].remove(backTrack[-1])

            while not len(self.roomDict[self.currentRoom]):
                back = backTrack.pop()
                path.append(back)
            #call to move player pass in direction (back)
                r = requests.post(url, data = {"direction": back}, headers =  {"Authorization": "Token 630d593ddd37dfd19902d98ef025638b39131316", "Content-Type": "application/json"})
                data = r.json()
                self.currentRoom = data.get("room_id")
                self.roomTitle = data.get("title")
                self.exits = data.get("exits")
                self.cooldown = data.get("cooldown")

            move = self.roomDict[self.currentRoom].pop(0)
            path.append(move)

            if move == "n":
                backTrack.append("s")
            elif move == "s":
                backTrack.append("n")
            elif move == "e":
                backTrack.append("w")
            elif move == "w":
                backTrack.append("e")
        
        #travel to next room passing in (move)
            r = requests.post(url, data = {"direction": move}, headers =  {"Authorization": "Token 630d593ddd37dfd19902d98ef025638b39131316", "Content-Type": "application/json"})
            data = r.json()
            self.currentRoom = data.get("room_id")
            self.roomTitle = data.get("title")
            self.exits = data.get("exits")
            self.cooldown = data.get("cooldown")

        print(path)
        return path


adv = Adventure()
adv.traverse()