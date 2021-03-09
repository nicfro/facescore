from src.endpoints.elo import get_elo_by_image_id
from src.endpoints import DBC
from trueskill import rate_1vs1, Rating


def calculateElo(winner, loser):
    """https://trueskill.org/"""
    winner = get_elo_by_image_id(winner, DBC.Session())
    loser = get_elo_by_image_id(loser, DBC.Session())
    
    winner_prev_trueskill = Rating(mu = winner["mu"], sigma = winner["sigma"])  
    loser_prev_trueskill = Rating(mu = loser["mu"], sigma = loser["sigma"])  

    winner_trueskill, loser_trueskill = rate_1vs1(winner_prev_trueskill, loser_prev_trueskill)
    
    return {"winner_mu": winner_trueskill.mu,
            "winner_sigma": winner_trueskill.sigma,
            "loser_mu": loser_trueskill.mu,
            "loser_sigma": loser_trueskill.sigma,}