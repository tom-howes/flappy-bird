import json

score_file = "scores/leaderboard_current.json"

class Leaderboard():
    
    def __init__(self, score_file):
        self.player = self.get_player()
        self.leaderboard = self.get_leaderboard(score_file)
    
    # Prompts the user to input their name
    def get_player(self):
        player = input("Enter your name: ")
        return player
    
    # Retrieves the leaderboard 
    def get_leaderboard(self, score_file):
        with open(score_file, 'r') as file:
            return json.load(file)
    
    # Function to blit leaderboard onto screen
    def draw(self, window):
        pass

    def add_current_score(self, score):
        leaders = self.leaderboard['players']
        player_score = {"name" : self.player, "score" : str(score)}
        for i in range(len(leaders)):
            if int(leaders[i]["score"]) < score:
                leaders.insert(player_score, i)
        self.leaderboard['players'] = leaders

    # Function to update leaderboard with current player score
    def update(self):
        with open(score_file, 'a') as file:
            updated_leaderboard = json.load(score_file)
            updated_leaderboard['players'] = self.leaderboard['players']
            json.dump(updated_leaderboard, file)


    # Function to reset leaderboard to template
    def reset(self):
        pass