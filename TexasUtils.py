def CompareHighCards(Cards1, Cards2):
    # return True if Cards1 >= Cards2
    CardValue1 = [Card[1] for Card in Cards1]
    CardValue2 = [Card[1] for Card in Cards2]
    if CardValue1 == CardValue2:
        return 0
    elif CardValue1 < CardValue2:
        return -1
    else:
        return 1

def CheckStraight(AllCards):
    Winners = []
    MaxStraight = -1
    for Player in range(len(AllCards)):
        NumOfStraight = 1
        CurrentPlayerCards = AllCards[Player]
        CurrentPlayerCards.sort(key=lambda x: x[1], reverse=True)
        for index in range(1, len(CurrentPlayerCards)):
            if CurrentPlayerCards[index][1] - CurrentPlayerCards[index - 1][1] == 1:
                NumOfStraight += 1
            else:
                NumOfStraight = 1
            if NumOfStraight == 5:
                if CurrentPlayerCards[index][1] > MaxStraight:
                    MaxStraight = CurrentPlayerCards[index][1]
                    Winners = [Player, ]
                elif CurrentPlayerCards[index][1] == MaxStraight:
                    Winners.append(Player)
                break
        # Check Special Straight: A 2 3 4 5
        if NumOfStraight == 4 and CurrentPlayerCards[-1][1] == 4 \
                and CurrentPlayerCards[0][1] == 16 and MaxStraight < 0:
            Winners.append(Player)
    return Winners

def CheckHighCard(AllCards):
    Winners = [0, ]
    MaxCardType = AllCards[0]
    MaxCardType.sort(key=lambda x: x[1], reverse=True)
    MaxCardType = MaxCardType[:5]
    for Player in range(1, len(AllCards)):
        CurrentPlayerCards = AllCards[Player]
        CurrentPlayerCards.sort(key=lambda x: x[1], reverse=True)
        CompareResult = CompareHighCards(MaxCardType, CurrentPlayerCards[:5])
        if CompareResult < 0:
            Winners = [Player, ]
            MaxCardType = CurrentPlayerCards[:5]
        elif CompareResult == 0:
            Winners.append(Player)
    return Winners