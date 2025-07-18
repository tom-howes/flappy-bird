import json
import shutil
import pygame

score_file = "scores/leaderboard_current.json"
score_template = "scores/leaderboard_template.json"

class Leaderboard():
    
    def __init__(self, score_file, player_name):
        self.player = player_name
        self.leaderboard = self.load_leaderboard(score_file)
    
    # Prompts the user to input their name
    def get_player(self):
        player = input("Enter your name: ")
        return player
    
    # Loads the leaderboard from json file 
    def load_leaderboard(self, score_file):
        with open(score_file, 'r') as file:
            return json.load(file)
    
    # Function to blit leaderboard onto screen
    def get_leaderboard(self):
        return self.leaderboard['players']
    # Adds current player and score to leaderboard if its is higher than the others
    def add_current_score(self, score):
        if score == 0:
            return
        leaders = self.leaderboard['players']
        player_score = {"name" : self.player, "score" : str(score)}
        for i in range(len(leaders)):
            if int(leaders[i]["score"]) < score:
                leaders.insert(i, player_score)
                break
        
        if len(leaders) < 5:
            leaders.append(player_score)
        self.leaderboard['players'] = leaders[:5]

    # Function to update leaderboard with current player score
    def update(self):

        with open(score_file, 'w') as file:
            json.dump(self.leaderboard, file)


    # Function to reset leaderboard to template
    def reset(self):
        shutil.copyfile(score_template, score_file)