import argparse
from src.schemas.users import VoteSchema
from src.logic.shared_logic.hasher import Hash
from src.logic.shared_logic.jwt_handler import encode_auth_token
from src.database.crud import create, read
from src.logic.elo import Elo

class Vote:
    def __init__(self, **kwargs):
        self.kwargs = vars(kwargs) if type(kwargs) is argparse.Namespace else kwargs
        self.vote = VoteSchema(kwargs)

    def cast_vote(self, winner_id, loser_id):
        elo = Elo()
        winner_elo, loser_elo = elo.calculateElo(Elo.get_elo(winner_id), Elo.get_elo(loser_id))
        #save vote
        #update winner elo
        #update loser elo
        create_elo

    def write_vote(self):
        return create(self.vote)
