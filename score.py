import json

score_file = "scores/leaderboard.json"

class Score(self, score_file):
    
    def __init__(self, score_file, current_player):
        self.player = current_player
        self.leaderboard = self.get_leaderboard(score_file)
    
    
    def get_leaderboard(self, score_file):
        with open(score_file, 'r') as file:
            leaderboard = json.load(file)
            return leaderboard