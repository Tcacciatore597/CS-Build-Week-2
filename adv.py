
import requests
import time
import json

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
        self.roomDict[self.currentRoom] = ["s", "n", "e", "w"]
        self.roomTitle = "A brightly lit room"
        self.exits = ["s", "n", "e", "w"]

        while self.roomTitle is not "Pirate Ry":

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
                r = requests.post(url, json = {"direction": back}, headers = {"Authorization": "Token 630d593ddd37dfd19902d98ef025638b39131316", "Content-Type": "application/json"})
                print(r.status_code)
                data = json.loads(r.text)
                self.currentRoom = data["room_id"]
                self.roomTitle = data["title"]
                self.exits = data["exits"]
                self.cooldown = data["cooldown"]
                print(self.currentRoom)

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
        
            r = requests.post(url, json = {"direction": move}, headers = {"Authorization": "Token 630d593ddd37dfd19902d98ef025638b39131316", "Content-Type": "application/json"})
            print(r.status_code)
            data = json.loads(r.text)
            self.currentRoom = data["room_id"]
            self.roomTitle = data["title"]
            self.exits = data["exits"]
            self.cooldown = data["cooldown"]
            print(self.currentRoom)

        print(path)
        return path

adv = Adventure()
adv.traverse()