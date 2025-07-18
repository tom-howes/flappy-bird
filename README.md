# flappy-bird
My take on the popular game flappy bird

Background - https://www.vectorstock.com/royalty-free-vector/cartoon-summer-beach-paradise-nature-vacation-vector-55093623

Bird - https://www.vecteezy.com/png/17229164-free-birds-for-projects

Pipe - https://opengameart.org/content/pipe

Score counter - https://www.vecteezy.com/vector-art/99898-number-counter-2

I didn't want the game to start automatically. I wanted a freeze frame that looped until the user pressed SPACE or UP to signify they were ready. This was achieved through a While loop, pygame event handlers and if/else statements that blit images in place each iteration until the game is started.

Pipes were created using an image found on opengameart - The heights are randomly generated but the gap between the pipes is always the same and they use the same x coordinate to ensure they're opposite each otehr.

is_game_over function checks whether the bird has hit the top/bottom of the window, or the top or bottom pipes (using pipe and bird height variables) - returning True if the game is over and False otherwise.

Encountering bugs with pipe placement and the game randomly triggering is_game_over without any visual indication as to why. Will remove the random element of pipe placement for now in order to better to debug.

Refactored the pipe dictionaries to simplify them and ensure that pipes were being generated correctly (without random element). As of now, one pipe is generated initially and once that reaches the end of the screen another set of pipes of the same dimensions is generated. Pipe creation and score tracking work as intended.

Collisions fixed, bottom pipe is simply pipe['y'], top pipe is pipe['y'] + pipe_height, to reflect that the pipe is blitted from pipe['y'] down. -3 added at the moment to account for the slight border around the png.

Swapped to Object-Oriented approach, giving birds and pipes their own classes.

Investigated pygame's masks feature to enable more accurate sprite collisions.

Added if/else statements to cycle through bird images to display wings up or down based on velocity and player pressing flap (space/up)

Added pipe acceleration based on incrementing score (0.5 per 5 score) to make the game harder as the player progresses

Added intro screen with title and blinking text to prompt user to start the game.

Working on implementing a leaderboard. Using json files and parsing with Python's inbuilt library. Score class will handle retrieving and updating leaderboard - looking to work with a template (blank) leaderboard and a current (up-to-date) leaderboard.

Realised that User Interface class will be needed to create buttons and have the user enter their name, refresh the leaderboard etc. - For testing purposes will initially handle in the terminal.

Added mechanism to write player name / score to leaderboard json file, testing now.

If score is 0, not added - else check if it is higher than any scores on current leaderboard - if it is insert it, or the leaderboard is not full (cap. 5), add it to the end. slice the leaderboard to only store the top 5 scores.

Need to create current leaderboard from template if it doesn't exist

Updated name text box to prompt user to enter input, restrict name length and prevent user starting game without a name.

Added leaderboard screen with up-to-date leaderboard and button to navigate to it.

Next steps:
     - Add animations to bird (flapping wings (done), tilt up/down, flop on death)
     - Add start (done) and finish animation
     - Explore ways to increase difficulty
     - Add leaderboard (done) and player stats etc.
     - Implement UI class for buttons / user input etc. (not sure if needed - maybe refactor)
     - Create separate screen for leaderboard (done)
     - Add back button for leaderboard screen (done)
