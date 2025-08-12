import json
import shutil
import pygame

# Current score json file
score_file = "scores/leaderboard_current.json"

# Empty template for score json file
score_template = "scores/leaderboard_template.json"

class Leaderboard():
    
    def __init__(self, score_file, player_name):
        """ Initiates new leaderboard based on score json file and input player name
        """
        self.player = player_name
        self.leaderboard = self.load_leaderboard(score_file)
    

    def set_player(self, name):
        """ Updates player name
        """
        self.player = name
     
    def load_leaderboard(self, score_file):
        """ Loads the leaderboard from json file
        """
        with open(score_file, 'r') as file:
            return json.load(file)
    
    
    def get_leaderboard(self):
        """ Returns dict of player names / scores
        """
        return self.leaderboard['players']
    # 
    def add_current_score(self, score):
        """ Adds current player and score to leaderboard if it is higher than some existing score
        """
        # Skip if no score
        if score == 0:
            return
        leaders = self.leaderboard['players']
        player_score = {"name" : self.player, "score" : str(score)}
        # Boolean to track if score added
        added = False
        # If leaderboard is not empty, compare to existing scores, put in appropriate position
        if len(leaders) > 0:
            for i in range(len(leaders)):
                if int(leaders[i]["score"]) < score:
                    leaders.insert(i, player_score)
                    added = True
                    break
        if len(leaders) < 5 and not added:
            leaders.append(player_score)
        self.leaderboard['players'] = leaders[:5]

    def update(self):
        """ Function to update score file with current player score
        """

        with open(score_file, 'w') as file:
            json.dump(self.leaderboard, file)

    def reset(self):
        """ Function to reset leaderboard to template
        """
        shutil.copyfile(score_template, score_file)
        self.load_leaderboard(score_file)