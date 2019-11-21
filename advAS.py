import requests
import time
import json
url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"


class Adventure:
    def __init__(self):
        self.roomDict = dict()
        self.currentRoom = 433
        self.exits = []
        self.roomTitle = ""
        self.cooldown = 12.5
        self.items = []
    def traverse(self):
        path = []
        backTrack = []
    #setup starting room 0
        self.roomDict[self.currentRoom] = ["s", "n", "e", "w"]
        self.roomTitle = "A brightly lit room"
        self.exits = ["s", "n", "e", "w"]
        while self.roomTitle != "Wishing Well" and len(self.roomDict) < 499:
    # while len(self.roomDict) < 499:
            if self.currentRoom not in self.roomDict:
                currentID = self.currentRoom
                self.roomDict[currentID] = self.exits
                self.roomDict[currentID].remove(backTrack[-1])
            while not len(self.roomDict[self.currentRoom]):
                back = backTrack.pop()
                path.append(back)
            #call to move player pass in direction (back)
                r = requests.post(url, json = {"direction": back}, headers = {"Authorization": "Token b383749c19f1a7d08b8270d4f85bc5e05a47b119", "Content-Type": "application/json"})
                print('**---------------**')
                print(r.status_code)
                data = json.loads(r.text)
                self.currentRoom = data["room_id"]
                self.roomTitle = data["title"]
                self.exits = data["exits"]
                self.cooldown = data["cooldown"]
                self.items = data["items"]
                m = data["messages"]
                e = data["errors"]
                print("back loop")
                print(f"messge: {m}")
                print(f"error: {e}")
                print(">> Current Room: ", self.currentRoom)
                print(">> Title: ", self.roomTitle)
                print('*** Items:', self.items)
                time.sleep(self.cooldown + 1)
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
            r = requests.post(url, json = {"direction": move}, headers = {"Authorization": "Token b383749c19f1a7d08b8270d4f85bc5e05a47b119", "Content-Type": "application/json"})
            print('**---------------**')
            print(r.status_code)
            data = json.loads(r.text)
            self.currentRoom = data["room_id"]
            self.roomTitle = data["title"]
            self.exits = data["exits"]
            self.cooldown = data["cooldown"]
            self.items = data["items"]
            message = data["messages"]
            error = data["errors"]
            print(f"messge: {message}")
            print(f"error: {error}")
            print(">> Current Room: ", self.currentRoom)
            print(">> Title: ", self.roomTitle)
            print('*** Items:', self.items)
            time.sleep(self.cooldown + .2)
        print(path)
        return path
adv = Adventure()
adv.traverse()