# to determine real win rate of all card types
# todo:
#   1. core logics - 60 points - [[ done ]]
#   2. result storage - 20 points
#   3. unit tests - 20 points
#   4. batch data - 20 points
#   5. gui / mobilize : cocos? unity? or anything can be pack as an app, game or miniapp to RELEASE. - 100 points
#

import random
import TexasUtils

NumOfSuits = 4
NumOfValues = 13
PlayerNumberLowerBound = 2
PlayerNumberUpperBound = 10

# Card: (Suit [H = 0, D = 1, S = 2, C = 3], Value [2 = 4, 3 = 5, 4 = 6, ..., A = 16])
class TexasSimulator:
    def __init__(self, PlayerNum = 5, CardLayout = None):
        if CardLayout:
            self.CardLayout = CardLayout
        else:
            self.CardLayout = []
            for Suit in range(NumOfSuits):
                for Value in range(NumOfSuits, NumOfSuits + NumOfValues):
                    self.CardLayout.append((Suit, Value))
            self.WashCards()

        self.PlayerNumber = PlayerNum
        self.AllTypes = dict()
        self.CollectAllTypes()

    def SetCardLayout(self, CardLayout):
        self.CardLayout = CardLayout

    def WashCards(self):
        random.shuffle(self.CardLayout) 
            
    def CollectAllTypes(self):
        # Set Public Cards
        PublicCards = [self.CardLayout[2 * self.PlayerNumber + 1],
                       self.CardLayout[2 * self.PlayerNumber + 2],
                       self.CardLayout[2 * self.PlayerNumber + 3],
                       self.CardLayout[2 * self.PlayerNumber + 5],
                       self.CardLayout[2 * self.PlayerNumber + 7]]
        # collect all card types from all player
        self.AllTypes.clear()
        for Player in range(self.PlayerNumber):
            self.AllTypes[Player] = dict()
            CurrentPlayerType = self.AllTypes[Player]
            # index -1 signify the card type of player
            CurrentPlayerType[-1] = [self.CardLayout[Player], self.CardLayout[self.PlayerNumber + Player]] + PublicCards
            for Card in CurrentPlayerType[-1]:
                for Type in Card:
                    if Type not in CurrentPlayerType:
                        CurrentPlayerType[Type] = 1
                    else:
                        CurrentPlayerType[Type] += 1


    def CheckStraightFlush(self):
        Winners = []
        HitFlushCards = []
        HitFlushIndexMap = dict()

        # check flush hit
        for Player in range(self.PlayerNumber):
            HitSuit = -1
            CurrentPlayerType = self.AllTypes[Player]
            for Suit in range(4):
                if Suit in CurrentPlayerType and CurrentPlayerType[Suit] >= 5:
                    HitSuit = Suit
                    break
            if HitSuit >= 0:
                CurrentPlayerCards = CurrentPlayerType[-1]
                HitFlushCards.append([Card for Card in CurrentPlayerCards if Card[0] == HitSuit])
                HitFlushIndexMap[len(HitFlushCards) - 1] = Player

        # check flush cards straight
        StraightResult = TexasUtils.CheckStraight(HitFlushCards)
        if len(StraightResult) > 0:
            Winners = [HitFlushIndexMap[index] for index in StraightResult]
        return Winners

    # return list of winners who hit Four Of Kind
    def CheckFourOfKind(self):
        Winners = []
        HitPlayers = dict()
        MaxHit = 0

        # check four of kind hit
        for Player in range(self.PlayerNumber):
            CurrentPlayerType = self.AllTypes[Player]
            HitValue = 0
            for Value in range(16, 3, -1): # 2 = 4, ..., A = 16
                if Value in CurrentPlayerType and CurrentPlayerType[Value] == 4:
                    HitValue = Value
                    break
            if HitValue > 0:
                HitPlayers[Player] = HitValue
                MaxHit = HitValue if HitValue > MaxHit else MaxHit

        # filter max four of kind
        if len(HitPlayers) > 0:
            HitKickers = dict()
            for HitPlayer in HitPlayers:
                if HitPlayers[HitPlayer] == MaxHit:
                    for Kicker in range(16, 3, -1):
                        if Kicker in self.AllTypes[HitPlayer] and Kicker != MaxHit:
                            HitKickers[HitPlayer] = Kicker
                            break

            # check max kicker in same four of kind
            MaxKicker = max(HitKickers.values(), default = 0)
            if 4 <= MaxKicker <= 16:
                for HitPlayer in HitKickers:
                    if HitKickers[HitPlayer] == MaxKicker:
                        Winners.append(HitPlayer)
            
        return Winners

    # return list of winners who hit Full House
    def CheckFullHouse(self):
        Winners = []
        HitPlayers = dict()
        MaxHit = 0

        # check full house hit
        for Player in range(self.PlayerNumber):
            CurrentPlayerType = self.AllTypes[Player]
            HitValue = 0
            for Value in range(16, 3, -1):  # 2 = 4, ..., A = 16
                if Value in CurrentPlayerType and CurrentPlayerType[Value] == 3:
                    HitValue = Value
                    break
            if HitValue > 0:
                HitPlayers[Player] = HitValue
                MaxHit = HitValue if HitValue > MaxHit else MaxHit

        # check full house max pair kicker
        if len(HitPlayers) > 0:
            HitKickers = dict()
            for HitPlayer in HitPlayers:
                if HitPlayers[HitPlayer] == MaxHit:
                    for Kicker in range(16, 3, -1):
                        if Kicker in self.AllTypes[HitPlayer] and Kicker != MaxHit and self.AllTypes[HitPlayer][Kicker] >= 2:
                            HitKickers[HitPlayer] = Kicker
                            break

            MaxKicker = max(HitKickers.values(), default=0)
            if 4 <= MaxKicker <= 16:
                for HitPlayer in HitKickers:
                    if HitKickers[HitPlayer] == MaxKicker:
                        Winners.append(HitPlayer)
        return Winners

    # return list of winners who hit Flush
    def CheckFlush(self):
        Winners = []
        HitFlushCards = []
        HitFlushIndexMap = dict()

        # check flush hit
        for Player in range(self.PlayerNumber):
            HitSuit = -1
            CurrentPlayerType = self.AllTypes[Player]
            for Suit in range(4):
                if Suit in CurrentPlayerType and CurrentPlayerType[Suit] >= 5:
                    HitSuit = Suit
                    break
            if HitSuit >= 0:
                CurrentPlayerCards = CurrentPlayerType[-1]
                HitFlushCards.append([ Card for Card in CurrentPlayerCards if Card[0] == HitSuit])
                HitFlushCards[-1] = HitFlushCards[-1][:5]
                HitFlushIndexMap[len(HitFlushCards) - 1] = Player

        # compare suited high card
        if len(HitFlushCards) > 0:
            FlushWinnerIndexes = TexasUtils.CheckHighCard(HitFlushCards)
            Winners = [HitFlushIndexMap[FlushIndex] for FlushIndex in FlushWinnerIndexes]
        return Winners

    # return list of winners who hit Straight
    def CheckStraight(self):
        return TexasUtils.CheckStraight([self.AllTypes[Player][-1] for Player in range(self.PlayerNumber)])

    # return list of winners who hit Three Of Kind
    def CheckThreeOfKind(self):
        Winners = []
        HitPlayers = dict()
        MaxHit = 0

        # check three of kind hit
        for Player in range(self.PlayerNumber):
            CurrentPlayerType = self.AllTypes[Player]
            HitValue = 0
            for Value in range(16, 3, -1):  # 2 = 4, ..., A = 16
                if Value in CurrentPlayerType and CurrentPlayerType[Value] == 3:
                    HitValue = Value
                    break
            if HitValue > 0:
                HitPlayers[Player] = HitValue
                MaxHit = HitValue if HitValue > MaxHit else MaxHit

        # filter max hit players
        if len(HitPlayers) > 0:
            HitKickers = dict()
            for HitPlayer in HitPlayers:
                if HitPlayers[HitPlayer] == MaxHit:
                    for Kicker in range(16, 3, -1):
                        if Kicker in self.AllTypes[HitPlayer] and Kicker != MaxHit:
                            if HitPlayer not in HitKickers:
                                HitKickers[HitPlayer] = [Kicker,]
                            else:
                                HitKickers[HitPlayer].append(Kicker)
                                break

            # check max kickers
            MaxKicker = [-1, -1]
            for HitPlayer in HitKickers:
                if MaxKicker < HitKickers[HitPlayer]:
                    Winners = [HitPlayer, ]
                    MaxKicker = HitKickers[HitPlayer]
                elif MaxKicker == HitKickers[HitPlayer]:
                    Winners.append(HitPlayer)
        return Winners

    # return list of winners who hit Two Pairs
    def CheckTwoPairs(self):
        Winners = []
        HitPlayers = dict()
        MaxHit = [-1, -1]

        # check two pairs hit
        for Player in range(self.PlayerNumber):
            CurrentPlayerType = self.AllTypes[Player]
            HitValue = [-1, -1]
            NumOfPairs = 0
            for Value in range(16, 3, -1):  # 2 = 4, ..., A = 16
                if Value in CurrentPlayerType and CurrentPlayerType[Value] == 2:
                    HitValue[NumOfPairs] = Value
                    NumOfPairs += 1
                    if NumOfPairs >= 2:
                        break
            if HitValue[1] > 0:
                HitPlayers[Player] = HitValue
                MaxHit = HitValue if HitValue > MaxHit else MaxHit

        # filter max hit two pairs
        if len(HitPlayers) > 0:
            HitKickers = dict()
            for HitPlayer in HitPlayers:
                if HitPlayers[HitPlayer] == MaxHit:
                    for Kicker in range(16, 3, -1):
                        if Kicker in self.AllTypes[HitPlayer] and Kicker not in MaxHit:
                            HitKickers[HitPlayer] = Kicker
                            break

            # compare kicker
            MaxKicker = max(HitKickers.values(), default=0)
            if 4 <= MaxKicker <= 16:
                for HitPlayer in HitKickers:
                    if HitKickers[HitPlayer] == MaxKicker:
                        Winners.append(HitPlayer)
        return Winners

    # return list of winners who hit One Pair
    def CheckOnePair(self):
        Winners = []
        HitPlayers = dict()
        MaxHit = 0

        # check pair hit
        for Player in range(self.PlayerNumber):
            CurrentPlayerType = self.AllTypes[Player]
            HitValue = 0
            for Value in range(16, 3, -1):  # 2 = 4, ..., A = 16
                if Value in CurrentPlayerType and CurrentPlayerType[Value] == 2:
                    HitValue = Value
                    break
            if HitValue > 0:
                HitPlayers[Player] = HitValue
                MaxHit = HitValue if HitValue > MaxHit else MaxHit

        # filter max hit pair
        if len(HitPlayers) > 0:
            HitKickers = dict()
            for HitPlayer in HitPlayers:
                if HitPlayers[HitPlayer] == MaxHit:
                    for Kicker in range(16, 3, -1):
                        if Kicker in self.AllTypes[HitPlayer] and Kicker != MaxHit:
                            if HitPlayer not in HitKickers:
                                HitKickers[HitPlayer] = [Kicker, ]
                            else:
                                HitKickers[HitPlayer].append(Kicker)
                                if len(HitKickers[HitPlayer]) >= 3:
                                    break

            # compare kickers
            MaxKicker = [-1, -1, -1]
            for HitPlayer in HitKickers:
                if MaxKicker < HitKickers[HitPlayer]:
                    Winners = [HitPlayer, ]
                    MaxKicker = HitKickers[HitPlayer]
                elif MaxKicker == HitKickers[HitPlayer]:
                    Winners.append(HitPlayer)
        return Winners

    # return list of winners who hit High Card
    def CheckHighCard(self):
        Winners = [Player for Player in range(self.PlayerNumber)]
        RemainCompareCardNumber = 5
        for Value in range(16, 3, -1):
            HitPlayers = []
            for Player in Winners:
                if Value in self.AllTypes[Player]:
                    HitPlayers.append(Player)
            if len(HitPlayers) > 0:
                Winners = HitPlayers
                RemainCompareCardNumber -= 1
            if RemainCompareCardNumber == 0 or len(Winners) == 1:
                return Winners
        return Winners

    def CheckGameResult(self):
        self.CollectAllTypes()
        CheckFunctionList = {'StraightFlush' : self.CheckStraightFlush
               , 'FourOfKind' : self.CheckFourOfKind
               , 'FullHouse' : self.CheckFullHouse
               , 'Flush' : self.CheckFlush
               , 'Straight' : self.CheckStraight
               , 'ThreeOfKind' : self.CheckThreeOfKind
               , 'TwoPairs' : self.CheckTwoPairs
               , 'OnePair' : self.CheckOnePair
               , 'HighCard' : self.CheckHighCard}
        for CheckType, CheckFunction in CheckFunctionList.items():
            GameResult = CheckFunction()
            if len(GameResult) > 0:
                return CheckType, GameResult

    def Run(self, Iterations, Mode = None, InCards = None):
        for Iteration in range(Iterations):
            WinnerResult = self.CheckGameResult()
            # serialize part...