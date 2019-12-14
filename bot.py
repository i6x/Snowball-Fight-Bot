#################################################################################
 #SNOWBALL FIGHT BOT
 #NASIF QADRI, TIAN CHEN AND TELMAN HASANLI
 #LAST MODIFIED - DECEMBER 13, 2019
##################################################################################



# IMPORTS
from random import choice, randint
import json

#POSSIBLE MOVES THAT CAN BE RETURNED
possibleMoves = ['THROW', 'RELOAD', 'DUCK']


# get all permutations of moves some length
def perms(length):
    if length == 1:
        return possibleMoves
    
    p = []
    pms = perms(length-1)
    for m in possibleMoves:
        for n in pms:
            p.append(m + n)
    
    return p

# obj was stored in an external file
# obj = json.loads(open('data.json', 'r').read())

maxMoveCount = range(2, 4+1)

# initiate obj if nessasary
# for c in maxMoveCount:
#     for m in perms(c):
#         obj[m] = {
#             'THROW': 0,
#             'RELOAD': 0,
#             'DUCK': 0
#         }

def getMove( myScore, myBalls, myDucksUsed, myMovesSoFar, oppScore, oppBalls, oppDucksUsed, oppMovesSoFar ):
    global obj

    # update obj (only when "training" though)
    # for c in maxMoveCount:
    #     for i in range(len(oppMovesSoFar) - c):
    #         m = ''.join(oppMovesSoFar[i:i+c])
    #         obj[m][oppMovesSoFar[i+c]] += 1

    # check if a move is legal
    def legalMove(m):
        if m == False:
            return False
        
        if m == 'DUCK' and myDucksUsed == 5:
            return False
        elif m == 'THROW' and myBalls == 0:
            return False
        elif m == 'RELOAD' and myBalls == 10:
            return False
        else:
            return True

    def pickMove(throw,duck,rload):

        # look back 2, 3, 4 moves
        for c in maxMoveCount:
            if len(oppMovesSoFar) >= c:
                data = obj[''.join(oppMovesSoFar[-c:])]
                
                t = data['THROW']
                d = data['DUCK']
                r = data['RELOAD']
                avg = (t+d+r) / 4

                
                mx = max(t, d, r)
                if mx == t:
                    duck += 1
                    if t > avg:
                        # bot should really duck
                        duck += 2
                elif mx == d:
                    rload += 1
                    if d > avg:
                        # bot should really reload
                        rload += 2
                elif mx == r:
                    throw += 2
                    rload += 1
                    if t > avg:
                        throw += 5
                    if d > avg:
                        rload += 2

        # keep trying for a legal move
        m = False
        while not legalMove(m):
            ch = randint(1, throw + duck + rload)
            if ch <= throw:
                m = 'THROW'
            elif throw < ch <= duck + throw:
                m = 'DUCK'
            else:
                m = 'RELOAD'
        
        return m

# OPENING MOVE - DECREASED CHANCE TO DUCK
    if oppMovesSoFar == None:
        return(pickMove(420,69,420))  

    else:
        # CHECK FOR THROW AND RELOAD PATTERNS 
        last4Moves = oppMovesSoFar[-4:]

        if last4Moves == ["THROW","RELOAD","THROW","RELOAD"]:
            if myDucksUsed == 5:
                if myBalls > 0:
                    return(pickMove(1,0,0))
                elif myBalls == 0:
                    return(pickMove(0,0,1))
            else:
                return(pickMove(0,1,0))

        elif last4Moves == ["RELOAD","THROW","RELOAD","THROW"]:
            if myBalls == 0:
                return(pickMove(0,0,1))
            else:
                return(pickMove(1,0,0))

        # IF OPPONENT IS OUT OF BALLS
        elif oppBalls == 0:
            if myBalls == 0:
                return(pickMove(0,0,1)) # RELOAD
            else:
                if myBalls > 0:
                    if oppDucksUsed == 5:
                        return(pickMove(1,0,0)) #THROW
                    elif myBalls == 10:
                        return(pickMove(3,2,0)) #THROW OR DUCK
                    else:
                        return(pickMove(1,0,0)) #THROW
                else:
                    return(pickMove(0,0,1)) #RELOAD

        # IF OPP HAS NO MORE DUCKS
        elif oppDucksUsed == 5:
            if oppBalls == 0:
                return(pickMove(1,0,0)) # THROW
            else:
                if myBalls > 0 and myBalls <= 10: 
                    if myDucksUsed < 5:
                        if oppBalls > 2:
                            return(pickMove(3,7,0)) # DUCK OR THROW
                        else: 
                            return(pickMove(4,3,0)) # THROW OR DUCK
                    else:
                        return(pickMove(1,0,0)) #THROW
                        
                else:
                    if myDucksUsed == 5:
                        return(pickMove(0,0,1)) # RELOAD 
                    else:
                        return(pickMove(0,1,1)) # DUCK OR RELOAD

        # IF OUT OF DUCKS
        elif myDucksUsed == 5:
            if myBalls > 0 and myBalls < 10:
                return(pickMove(3,0,2)) # THROW OR RELOAD
            elif myBalls == 10:
                return(pickMove(1,0,0)) # THROW
            else:
                return(pickMove(0,0,1)) # RELOAD

        elif myBalls == 0:
            return(pickMove(0,1,1)) # DUCK OR RELOAD

        # IF I HAVE 10 BALLS AND USED ALL MY DUCKS
        else:
            if myBalls == 10 and myDucksUsed == 5:
                return(pickMove(1,0,0)) #THROW
            elif myBalls == 10:
                return(pickMove(3,1,0)) # THROW OR DUCK
            elif myDucksUsed == 5:
                return(pickMove(2,0,1)) # THROW OR RELOAD
            else:
                return(pickMove(1,1,1)) # THROW DUCK OR RELOAD


##################################################################################
#                                 END OF PROGRAM                                 #
