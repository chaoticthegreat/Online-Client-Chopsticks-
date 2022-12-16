import requests
from threading import Thread
import time, os, sys

def type(string:str):
  for char in string:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(0.025)
  print()
quit=False
def alive(username):
  while not quit:
    r=requests.post("https://Online-Server-Chopsticks.proryan.repl.co/check/", json = {"username":username, "checking":False}).json()
    if r["Kick"] == True:
      type("The other player left!")
      type("Re-run the program to play again :D")
      sys.exit()
    time.sleep(4)
username = input("What's your username: \n")
while not requests.post("https://Online-Server-Chopsticks.proryan.repl.co/check/", json = {"username":username,"checking":True}).json()["Username"]:
  print("Pick a different one!")
  username = input("What's your username: \n")

Thread(target = alive, args = (username,)).start()
type("Please wait while we match you up with someone!\nFor a quicker match up, call a partner to play on a different computer!")  
r = requests.get("https://Online-Server-Chopsticks.proryan.repl.co/"+username).json()
match_id = str(r["match_id"])
player_num = "1"
if r["match_found"] == False:
  player_num = "2"
  while requests.get("https://Online-Server-Chopsticks.proryan.repl.co/match/"+match_id).json()["match_found"] == False:
    time.sleep(3)
type("Match FOUND!")
def printBoard(user_right, user_left, opp_right, opp_left):
  print(f'''
  Opponent Left Hand: {"|"*opp_left}      Opponent Right Hand: {"|"*opp_right}


  Your Left Hand: {"|"*user_left}        Your Right Hand: {"|"*user_right}
  ''')
while True:
  os.system("clear")
  base_data =requests.get("https://Online-Server-Chopsticks.proryan.repl.co/server/", json={"match_id":match_id}).json()
  opp_user = base_data["Username"]
  opp_user.remove(username)
  print(f"{username} vs. {opp_user[0]}")
  if player_num=="1":opp_num="2"
  else:opp_num="1"
  printBoard(base_data[player_num]["right"], base_data[player_num]["left"], base_data[opp_num]["right"], base_data[opp_num]["left"])
  if base_data["Win"] == player_num:
    print("You have won!!")
    sys.exit()
  elif base_data["Win"] ==opp_num:
    print("You have lost :((")
    sys.exit()
  if base_data["Turn"] == player_num:
    choice1 = None
    while choice1 not in ["1", "2"]:
      choice1 = input("Do you want to attack or transfer:\n1. Attack\n2. Transfer\n")
    if choice1 == "1":
      choice2 = None
      while choice2 not in ["1", "2"]:
        os.system("clear")
        printBoard(base_data[player_num]["right"], base_data[player_num]["left"], base_data[opp_num]["right"], base_data[opp_num]["left"])
        choice2 = input("Do you want to use your left hand or right hand:\n1. Left Hand\n2. Right Hand\n")
        if choice2=="1":
          if base_data[player_num]["left"] == 0:
            type("Sorry, you don't have any chopsticks in your left hand")
            choice2 = None
          attack_hand="left"
        else:
          if base_data[player_num]["right"] == 0:
            type("Sorry, you don't have any chopsticks in your right hand")
            choice2 = None
          attack_hand="right"
      
      choice3 = None
      while choice3 not in ["1", "2"]:
        os.system("clear")
        printBoard(base_data[player_num]["right"], base_data[player_num]["left"], base_data[opp_num]["right"], base_data[opp_num]["left"])
        choice3 = input("Do you want to attack your opponents left hand or right hand:\n1. Left Hand\n2. Right Hand\n")
        if choice3=="1":
          if base_data[opp_num]["left"] == 0:
            type("Sorry, you can't attack their left hand because they have 0 chopsticks in that hand")
            choice3 = None
          victim_hand="left"
        else:
          if base_data[opp_num]["right"] == 0:
            type("Sorry, you can't attack their right hand because they have 0 chopsticks in that hand")
            choice3 = None
          victim_hand="right"
      data =requests.post("https://Online-Server-Chopsticks.proryan.repl.co/server/", json={"match_id":match_id, "player_num":player_num, "attack_hand":attack_hand, "victim_hand":victim_hand, "move":"attack"}).json()
    else:
      passed = True
      if base_data[player_num]["right"] ==1 and base_data[player_num]["left"] ==0:
        type("Sorry, you can't transfer at this moment (It would be unfair)")
        passed = False
        
      elif base_data[player_num]["left"] ==1 and base_data[player_num]["right"] ==0:
        type("Sorry, you can't transfer at this moment (It would be unfair)")
        passed = False
      if passed:
        choice1 = None
        while choice1 not in ["1", "2"]:
          os.system("clear")
          printBoard(base_data[player_num]["right"], base_data[player_num]["left"], base_data[opp_num]["right"], base_data[opp_num]["left"])
          choice1 = input("What hand do you want to take away sticks from?\n1. Left Hand\n2. Right Hand\n")
          if choice1 == "1":
            user_hand = "left"
            opp_hand = "right"
            if base_data[player_num]["left"] <= 0:
              type("Sorry, you don't have any sticks in that hand")
              choice1 = None
          elif choice1 == "2": 
            user_hand = "right"
            opp_hand = "left"
            if base_data[player_num]["right"] <=0:
              type("Sorry, you don't have any sticks in that hand")
              choice1 = None
        while True:
          os.system("clear")
          printBoard(base_data[player_num]["right"], base_data[player_num]["left"], base_data[opp_num]["right"], base_data[opp_num]["left"])
          choice2 = int(input("How much chopsticks do you want to take away?\n"))
          if choice2 > base_data[player_num][user_hand]:
            type("Sorry, you don't have that many chopsticks")
          elif choice2+base_data[player_num][user_hand] >=5:
            type("Sorry, that is too many chopsticks for the hand you are transferring too")
          else:break
        data =requests.post("https://Online-Server-Chopsticks.proryan.repl.co/server/", json={"match_id":match_id, "player_num":player_num, "move":"transfer", "sub_hand":user_hand, "transfer_amount": choice2}).json()
      time.sleep(1)
          
    
  else:
    type("Waiting for your opponent to make a move...")
    while requests.get("https://Online-Server-Chopsticks.proryan.repl.co/server/", json={"match_id":match_id}).json()["Turn"] != player_num: time.sleep(1)


