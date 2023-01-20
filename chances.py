import random



def coin_flip():
    flip = random.randint(0, 1)
    if flip == 0:
        return "heads"
    else:
        return "tails"


def choice(onlyheads=True):
    if onlyheads:
        return "heads"
    flip = random.randint(0, 1)
    if flip == 0:
        return "heads"
    else:
        return "tails"

money = 20000
games = 1000
startingBet = 3
bet = startingBet
multiplier = 3.2
counterTillLose = 0

def simulateGame():
    global games
    global startingBet
    global multiplier
    global money
    global bet
    biggestBet = 0
    lostlast = True
    counter = 0
    while(lostlast or counter < games):
        if(bet > money):
            # print(f"You cant do this!")
            # print(f"bet:{bet} money:{money}")
            bet = startingBet
        biggestBet = max(bet, biggestBet)
        counter += 1
        result = coin_flip()
        money -= bet
        headsortails = choice()
        if headsortails == result:
            lostlast = False
            money += bet * 2
            # print(f"won! before:{money - bet} after:{money} bet:{bet} ")
            bet = startingBet
        else:
            lostlast = True
            # print(f"lost! before:{money + bet} after:{money} bet:{bet} ")
            if money <= 0:
                # print(f"You are broke!")
                # print(f"Biggest bet:{biggestBet} iterations:{counter}")
                return False
            bet *= multiplier
        # print(f"Biggest bet:{biggestBet} iterations:{counter} money:{money}")
    return True


while True:
    if simulateGame():
        counterTillLose += 1
    else:
        break
print(f"lost after: {counterTillLose}")
