SuitNames = ['Spade', 'Heart', 'Diamond', 'Club']
ChineseSuitNames = ['黑桃', '红桃', '方块', '梅花']
ValueNames = [str(SmallValue) for SmallValue in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A']
def TranslateCard(Card, bUseChinese = True):
    InnerSuitNames = ChineseSuitNames if bUseChinese else SuitNames
    return InnerSuitNames[Card[0]] + ValueNames[Card[1] - 4]

if __name__ == "__main__":
    import TexasSimulator

    # All Test
    PlayerNumber = 5
    Simulator = TexasSimulator.TexasSimulator(PlayerNumber)
    for i in range(100):
        Simulator.WashCards()
        print('=' * 10 + ' Start ' + '=' * 10)
        for Player in range(PlayerNumber):
            print('Player ' + str(Player) + ': ' + TranslateCard(Simulator.CardLayout[Player]) +
                  ', ' + TranslateCard(Simulator.CardLayout[Player + PlayerNumber]))
        PublicCards = [TranslateCard(Simulator.CardLayout[2 * PlayerNumber + 1]),
                       TranslateCard(Simulator.CardLayout[2 * PlayerNumber + 2]),
                       TranslateCard(Simulator.CardLayout[2 * PlayerNumber + 3]),
                       TranslateCard(Simulator.CardLayout[2 * PlayerNumber + 5]),
                       TranslateCard(Simulator.CardLayout[2 * PlayerNumber + 7])]
        print('Public : ' + str(PublicCards))
        CardType, Winners = Simulator.CheckGameResult()
        print('\n\t Result, Hit Card Type ' + CardType + ', Winner is ' + str(Winners))
        print('=' * 10 + ' End ' + '=' * 10, end='\n\n')