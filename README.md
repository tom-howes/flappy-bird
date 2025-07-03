# flappy-bird
My take on the popular mobile game flappy bird

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

Looking to swap to OOP to have birds and pipes as their own classes.

Next steps:
     - Add random element to pipe generation
     - Investigate how to improve visual of pipes (attached to top and bottom of screen)
     - Add animations to bird (flapping wings, tilt up/down)
     - Add double digit scoring
     - Add incrementally increasing bird speed
