#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 23:39:10 2019

@author: shrikar.amirisetty
"""

import random
import time


numberWins = 0
numberCalculations = 0

hand1 = None
hand2 = None
CC1 = None
CC2 = None
CC3 = None
CC4 = None
CC5 = None

numCC = 0
numPlay = 0

def createDic(deck):
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    colors = ["H", "D", "C", "S"]
    
    for i in colors:
        for j in nums:
            deck += [str(j) + i]
    
    def enterCard(newdeck):
        while True:
            card = str(input("Enter card: "))
            
            if card in newdeck:
                newdeck.remove(card)
                return card
            else:
                print("Invalid card. Use syntax = 'Card number' + 'First letter of card pattern'. Example: 1S, 13(K)H")
    
    while True:
        numPlay = str(input("Enter number of players (2-8): "))
        
        if numPlay in range(2, 8):
            break
        else:
            print("Invalid")
    
    hand1 = enterCard(deck)
    hand2 = enterCard(deck)
    
    while True:
        enterCC = str(input("Would you like to enter the Community Cards (y/n): "))
        
        if enterCC == "y":
            while True:
                numCC = int(input("Enter number of cards (3/4/5): "))
                
                if numCC != 3 and numCC != 4 and numCC != 5:
                    print("Invalid")
                else:
                    if numCC >= 3:
                        CC1 = enterCard(deck)
                        CC2 = enterCard(deck)
                        CC3 = enterCard(deck)
                    
                    if numCC >= 4:
                        CC4 = enterCard(deck)
                    
                    if numCC == 5:
                        CC5 = enterCard(deck)
                    
                    break
            break
        elif enterCC == "n":
            break
        else:
            print("Invalid")
        
    return deck

def assignCards(deck):
    handDic = [[hand1, hand2]]
    
    for i in range(1, numPlay):
        oppCard1 = deck[random.randint(0, len(deck))]
        deck.remove(oppCard1)
        oppCard2 = deck[random.randint(0, len(deck))]
        deck.remove(oppCard2)
        handDic += [[oppCard1, oppCard2]]
    
    if numCC < 3:
        CC1 = deck[random.randint(0, len(deck))]
        deck.remove(CC1)
        CC2 = deck[random.randint(0, len(deck))]
        deck.remove(CC2)
        CC3 = deck[random.randint(0, len(deck))]
        deck.remove(CC3)
    
    if numCC < 4:
        CC4 = deck[random.randint(0, len(deck))]
        deck.remove(CC4)
    
    if numCC < 5:
        CC5 = deck[random.randint(0, len(deck))]
        deck.remove(CC5)
    
    return handDic
    
def assignScore(allHands):
    scores = []
    
    for i in allHands:
        score = 0
        hand = i + [CC1, CC2, CC3, CC4, CC5]
        
        #High Card Check
        for i in hand:
            num = int(i[:-1])
            if num > score:
                score = num
        
        #Pair Check
        nums = []
        pairVals = []
        colors = []
        
        for i in hand:
            toAdd = int(i[:-1])
            if toAdd in nums:
                pairVals += [toAdd]
            nums += toAdd
            colors += str(i[-1])
        
        if len(pairVals) == 1:
            score = 14 + pairVals[0]
        
        if len(pairVals) > 1:
            pairVals.sort()
            score = 14*2 + pairVals[-1] + pairVals[-2]
        
        #Three of a Kind Check
        threeVals = []
        
        for i in pairVals:
            if nums.count(i) >= 3:
                threeVals += [i]
                pairVals.remove(i)
        
        if len(threeVals) == 0:
            score = 14*4 + max(threeVals)
        
        #Straight
        nums.sort()
        counter = 1
        seq = []
        
        for i in range(1, len(nums), -1):
            newseq = []
            if len(newseq) == 0:
                newseq = [nums[i]]
            
            if nums[i - 1] == nums[i] - 1:
                newseq += [nums[i - 1]]
                counter += 1
            else:
                newseq = []
                counter = 1
            
            if counter == 5:
                seq = newseq
                score = 14*5 + seq[0]
                break
        
        #Flush
        for i in colors:
            if colors.count(i) >= 5:
                score = 14*7
                break
        
        #

















