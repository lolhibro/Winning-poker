#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 23:39:10 2019

@author: shrikar.amirisetty
"""

win_prob = None
num_players = None
hand = None
flop = None
checked_cards = None

def key(item):
    if item == 't':
        return 10
    if item == 'j':
        return 11
    if item == 'q':
        return 12
    if item == 'k':
        return 13
    if item == 'a':
        return 14
    return int(item)

def key_reverse(item_num):
    if item_num == 10:
        return 't'
    if item_num == 11:
        return 'j'
    if item_num == 12:
        return 'q'
    if item_num == 13:
        return 'k'
    if item_num == 14:
        return 'a'
    return str(item_num)

def rsf_prob_calculator(start, cards, color):
    global win_prob
    if len(cards) == 5:
        return True
    elif len(cards) == 4:
        item_num = start
        found = False
        your_flush = False
        for i in range(4):
            if key_reverse(item_num) == cards[i]:
                item_num += 1
            else:
                found = True
                your_flush = key_reverse(item_num) + color in hand
                break
        if not found:
            your_flush = key_reverse(item_num) + color in hand
        if your_flush:
            return True
        elif key_reverse(item_num) + color not in checked_cards:
            cards_left = (50 - 2*(len(flop) - 1) - len(checked_cards))
            win_prob -= min(win_prob, (1 - (cards_left - 2*(num_players - 1))/cards_left))
            checked_cards.add(key_reverse(item_num) + color)
        return False
    else:
        item_num = start
        num_to_find = 2
        i = 0
        while i != len(cards) or item_num < start + 5:
            if i < len(cards) and key_reverse(item_num) == cards[i]:
                i += 1
            elif key_reverse(item_num) + color in checked_cards:
                return False
            elif key_reverse(item_num) + color in hand:
                num_to_find -= 1
            item_num += 1
        if num_to_find == 0:
            return True
        elif num_to_find == 2:
            cards_left = (50 - 2*(len(flop) - 1) - len(checked_cards))
            probsum = 0
            for i in range(num_players):
                probsum += 1/(cards_left - 1 - 2*i)
            win_prob -= min(win_prob, probsum/cards_left)
        return False

def foak_prob_calculator(numcount):
    global win_prob
    for i in sorted(numcount, reverse=True):
        if len(numcount[i]) == 4:
            return True
        elif len(numcount[i]) == 3:
            colorset = set(['s','d','h','c'])
            for color in numcount[i]:
                colorset.remove(color)
            card = i + colorset.pop()
            if card not in checked_cards:
                if card in hand:
                    return True
                else:
                    cards_left = (50 - 2*(len(flop) - 1) - len(checked_cards))
                    win_prob -= min(win_prob, (1 - (cards_left - 2*(num_players - 1))/cards_left))
                    checked_cards.add(card)
        elif len(numcount[i]) == 2:
            colorset = set(['s','d','h','c'])
            for color in numcount[i]:
                colorset.remove(color)
            num_to_find = 2
            for color in colorset:
                if i + color in checked_cards:
                    return False
                if i + color in hand:
                    num_to_find -= 1
            if num_to_find == 0:
                return True
            elif num_to_find == 2:
                cards_left = (50 - 2*(len(flop) - 1) - len(checked_cards))
                probsum = 0
                for i in range(num_players):
                    probsum += 1/(cards_left - 1 - 2*i)
                win_prob -= min(win_prob, probsum/cards_left)
    return False

def check_num(num, numcount):
    global win_prob
    for card in hand:
        if card[0] == num:
            return True
    colorset = set(['s','d','h','c'])
    for color in numcount[num]:
        colorset.remove(color)
    for color in colorset:
        if num + color not in checked_cards:
            cards_left = (50 - 2*(len(flop) - 1) - len(checked_cards))
            win_prob -= min(win_prob, (1 - (cards_left - 2*(num_players - 1))/cards_left))
            checked_cards.add(num + color)
    return False

def fh_prob_calculator(num1, num2, numcount):
    global win_prob
    if len(numcount[num1]) == 3:
        if num2 not in numcount:
            num_num2_in_hand = 0
            for card in hand:
                if card[0] == num2:
                    num_num2_in_hand += 1
            if num_num2_in_hand == 2:
                return True
            else:
                num_num2 = 4 - num_num2_in_hand:
                colors = ['s','d','h','c']
                for color in colors:
                    if num2 + color in checked_cards:
                        num_num2 -= 1
                
        elif len(numcount[num2]) == 2:
            return True
        else:
            return check_num(num2, numcount)
    elif len(numcount[num2]) >= 2:
        if not (key_reverse(num2) > key_reverse(num1) and len(numcount[num2]) > 2):
            return check_num(num1, numcount)
    else:
        colorset1 = set(['s','d','h','c'])
        for color in numcount[num1]:
            colorset1.remove(color)
        colorset2 = set(['s','d','h','c'])
        for color in numcount[num2]:
            colorset2.remove(color)
        cards_left = (50 - 2*(len(flop) - 1) - len(checked_cards))
        toadd = 0
        for i in range(num_players):
            toadd += 1/(cards_left - 1 - 2*i)
        count = 0
        for color1 in colorset1:
            found1 = False
            if num1 + color1 in checked_cards:
                continue
            if num1 + color1 in hand:
                found1 = True
            for color2 in colorset2:
                if num2 + color2 not in checked_cards:
                    if num2 + color2 in hand:
                        if found1:
                            return True
                    elif not found1:
                        count += 1
        win_prob -= min(win_prob, count*toadd/cards_left)
    return False

def print_win_prob():
    print("Win probability: {}%".format(win_prob*100))

def main():
    global win_prob
    numcount = {}
    colorcount = {}
    for i in flop:
        if i[0] not in numcount:
            numcount[i[0]] = [i[1]]
        else:
            numcount[i[0]].append(i[1])
        if i[1] not in colorcount:
            colorcount[i[1]] = [i[0]]
        else:
            colorcount[i[1]].append(i[0])

    for i in colorcount:
        colorcount[i].sort(key=key)

    completed = False

    # Royal/Straight flush check

    for color in colorcount:
        if len(colorcount[color]) >= 3:
            endidx = len(colorcount[color]) - 1
            startidx = endidx
            start = 10
            while start >= 2:
                while startidx >= 0 and key(colorcount[color][startidx]) >= start:
                    startidx -= 1
                while endidx >= 0 and key(colorcount[color][endidx]) >= start + 5:
                    endidx -= 1
                if endidx - startidx >= 3:
                    completed = rsf_prob_calculator(start, colorcount[color][startidx+1:endidx+1], color)
                    if completed:
                        break
                start -= 1
            break

    if completed:
        print("Royal/Straight Flush!")
        print_win_prob()
        return

    # Four of a kind check

    completed = foak_prob_calculator(numcount)

    if completed:
        print("Four of a Kind!")
        print_win_prob()
        return

    # Full house check

    sortedkeys = sorted(numcount, reverse=True)
    for num1 in sortedkeys:
        if len(numcount[num1]) == 3:
            for num2 in range(14, 1, -1):
                if num1 == key_reverse(num2):
                    continue
                completed = fh_prob_calculator(num1, key_reverse(num2), numcount)
                if completed:
                    break
        elif len(numcount[num1]) == 2:
            for num2 in sortedkeys:
                if num1 == num2:
                    continue
                completed = fh_prob_calculator(num1, num2, numcount)
                if completed:
                    break
        elif len(numcount[num1]) == 1:
            for num2 in sortedkeys:
                if num1 == num2 or numcount[num2] < 2:
                    continue
                completed = fh_prob_calculator(num1, num2, numcount)
                if completed:
                    break
        if completed:
            break
    if completed:
        print("Full House!")
        print_win_prob()
        return

    # Flush check

    print("You Lose")

if __name__ == '__main__':
    print("POKER WIN PROBABILITY CALCULATOR\n")

    print("Card notation: number or 't' for ten/'j'/'q'/'k'/'a' followed by suit abbreviation - 's'/'d'/'h'/'c'. Example: 9d, tc, as, qh\n")

    print("Input notation: when prompted for input, list relevant card names using commas. Example: '7d, td, 4c'\n")

    num_players = int(input("number of players: "))

    while True:
        hand = set([i.strip() for i in input("input hand: ").split(',')])
        flop = [i.strip() for i in input("input flop: ").split(',')]

        while True:
            win_prob = 1
            checked_cards = set()

            main()

            game_over = input("End of game? (y/n): ")
            if game_over == 'y':
                break
            flop.append(input("Next card: ").strip())

        reset = input("Reset? (y/n): ")
        if reset != 'y':
            break












