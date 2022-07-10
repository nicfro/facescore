import os
import sys

sys.path.insert(0, os.getcwd())

import unittest

from src.logic.elo import calculateElo

class TestHasher(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHasher, self).__init__(*args, **kwargs)

    def test_01_elo_score_is_higher_for_winner(self):
        res = calculateElo(3, 8)
        self.assertTrue(res["winner_mu"] > res["loser_mu"])
