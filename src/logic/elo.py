def calculateElo(winner, loser):
    '''https://www.omnicalculator.com/sports/elo'''
    winner = getEloScore(winner)[0]
    loser = getEloScore(loser)[0]
    EA = (1 / (1 + 10**((loser - winner)/400)))
    EB = (1 / (1 + 10**((winner - loser)/400)))
    
    winner = winner + 30 * (0.5 - EA)
    loser = loser + 30 * (0.5 - EB)
    
    return winner, loser


