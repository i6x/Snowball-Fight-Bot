#Imports
import time
from random import *
import random
import math

#Assign strategy names to variables

strat2Name = "Snowball-Fight-Bot"
strat2 = __import__(strat2Name)

duckLimit = 5
snowballLimit = 10
roundLimit = 30

def announce( message ):
    print(message)

                    
def announceGameResult( cheatingFound1, cheatingFound2, score1, score2, roundNum ):
    summary = ""

    if cheatingFound1 == True and cheatingFound2 == True:
        summary = "Both players cheated! Loss for both players"
        
    elif cheatingFound1 == True:
        summary = "Player 1 cheated! Player 2 wins!"
        
    elif cheatingFound2 == True:
        summary = "Player 2 cheated! Player 1 wins!"
        
    elif roundNum >= roundLimit:
        summary = str(roundLimit) + " rounds reached."

        if score1 > score2:
            summary = summary + " Player 1 wins!"
            
        elif score2 > score1:
            summary = summary + " Player 2 wins!"
            
        else:
            summary = summary + " Draw!"

    else:
        if score1 > score2:
            summary = summary + "Player 1 wins!"
            
        elif score2 > score1:
            summary = summary + "Player 2 wins!"

    announce( summary )


def game():
    x=0
    global curMove1, curMove2, cheatingFound1, cheatingFound2

    print("Welcome to SNOWBALL FIGHT!")
    print("First player to score 3 hits wins!")
    print("In each round you may THROW, DUCK, or RELOAD")
    print("You and the computer each have 1 snowball to start.")
    print("You may only THROW if you have at least 1 snowball")
    print("You score a point if you THROW while your opponent is RELOADING")
    print("You may only DUCK up to 5 times during a game")
    print("You cannot hoard more than 10 snowballs")
    print("Good luck!")
    print("")
    
    #Initialize variables
    score1 = 0
    score2 = 0
    
    snowballs1 = 1
    snowballs2 = 1
    
    ducksUsed1 = 0
    ducksUsed2 = 0
    
    movesSoFar1 = []
    movesSoFar2 = []
    
    roundNum = 0
    i = -1

    cheatingFound1 = False  #True if Player 1 has cheated
    cheatingFound2 = False  #True if Player 2 has cheated

    #Main loop
    while score1 < 3 and score2 < 3 and roundNum <= roundLimit and cheatingFound1 == False and cheatingFound2 == False:
        #Increment i 
        i += 1
        
        #Use i to find out whose turn it is 
        if i % 2 == 0:
            #Reset booleans
            duckC1 = False
            duckC2 = False
            throwC1 = False
            throwC2 = False
            reloadC1 = False
            reloadC2 = False

            #Increase round number
            roundNum += 1

            #If not round 1, then add both moves to their move-histories
            if roundNum > 1:
                movesSoFar1.append(curMove1)
                movesSoFar2.append(curMove2)
                
            #Get Player 1's move
            curMove1 = input("Enter THROW, DUCK, or RELOAD: ")

            #In case the user accidentally added an extra space before or after their entry
            if "RELOAD" in curMove1:
                curMove1 = "RELOAD"
            elif "DUCK" in curMove1:
                curMove1 = "DUCK"
            elif "THROW" in curMove1:
                curMove1 = "THROW"
                
            x=x+1

            #Check the validity of Player 1's move
            if curMove1 == "DUCK":
                
                if ducksUsed1 == duckLimit: #ILLEGAL DUCK!
                    print("You tried to duck for the 6th time!")
                    cheatingFound1 = True
                    
                duckC1 = True

            elif curMove1 == "RELOAD":
                
                if snowballs1 >= snowballLimit: #ILLEGAL RELOAD!
                    print("You tried to hoard more than " + str(snowballLimit) + " snowballs!")
                    cheatingFound1 = True
 
                reloadC1 = True

            elif curMove1 == "THROW":
                
                if snowballs1 == 0: #ILLEGAL THROW!
                    print("You tried to use snowballs when you have none left!")
                    cheatingFound1 = True
                    
                throwC1 = True
                
            else: #ILLEGAL WORD
                print( "Sorry," + curMove1 + " is not an option!")
                cheatingFound1 = True
        
        else:
            
            #Get Player 2's move
            curMove2 = strat2.getMove(score2, snowballs2, ducksUsed2, movesSoFar2,
                                      score1, snowballs1, ducksUsed1, movesSoFar1)

            #Check validity of Player 2's move
            if curMove2 == "DUCK":

                if ducksUsed2 == duckLimit: #ILLEGAL DUCK!
                    print("Computer tried to duck for the 6th time")
                    cheatingFound2 = True
                    
                duckC2 = True
                ducksUsed2 = ducksUsed2 + 1
                
            elif curMove2 == "RELOAD":
                snowballs2 += 1
                if snowballs2 > snowballLimit: #ILLEGAL RELOAD!
                    print("Computer tried to hoard more than " + str(snowballLimit) + " snowballs!")
                    cheatingFound2 = True

                reloadC2 = True
                
            elif curMove2 == "THROW":

                if snowballs2 == 0: #ILLEGAL THROW!
                    print("Computer tried to throw when it had no snowballs!")
                    cheatingFound2 = True
                    
                throwC2 = True
                snowballs2 -= 1

            else: #ILLEGAL WORD!
                print( "Hey computer, " + curMove2 + " is not an option!")
                cheatingFound2 = True

            #Adjust snowballs1 and ducksUsed1 (done later so player 2 doesn't know)
            if throwC1:
                snowballs1 -= 1
            if reloadC1:
                snowballs1 += 1
            if duckC1:
                ducksUsed1 = ducksUsed1 + 1
            
            #If no one threw then no one got hit
            if not throwC1 and not throwC2:
                summary = "No one got hit."

            #If any person reloaded that means they got hit (since the other person has thrown as we didn't pass the above if-statement)
            #Also adjusts the scores for the player that scored the hit
            elif reloadC1 or reloadC2:
                if reloadC1:
                    summary = "You got hit!"
                    score2 += 1
                else:
                    summary = "Computer got hit!"
                    score1 += 1  

            #If both players threw, then snowballs collide and no one gets hit        
            elif throwC1 and throwC2:
                summary = "Snowballs collide, so no one got hit."

            #If none of the above happened then one of the players missed
            #Prints out who missed their snowball
            else:
                if throwC1:
                    summary = "You missed!"
                elif throwC2:
                    summary = "Computer missed!"

            #Print a summary of the round
            print("Computer picked", curMove2)
            print(summary)
            print("Score:", score1, score2)
            print("Snowballs:", snowballs1, snowballs2)
            print("Ducks left", duckLimit - ducksUsed1, duckLimit - ducksUsed2)
            print("")         
            
            
    #Once the while-loop stops (by someone winning or cheating, or we reached the round-limit), announce the result   
    announceGameResult( cheatingFound1, cheatingFound2, score1, score2, roundNum )

        
#Start the game
game()
            
