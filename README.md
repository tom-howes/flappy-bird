# flappy-bird
My take on the popular mobile game flappy bird

Background - https://www.vectorstock.com/royalty-free-vector/cartoon-summer-beach-paradise-nature-vacation-vector-55093623

Bird - https://www.vecteezy.com/png/17229164-free-birds-for-projects

Pipe - https://opengameart.org/content/pipe

Score counter - https://www.vecteezy.com/vector-art/99898-number-counter-2

I didn't want the game to start automatically. I wanted a freeze frame that looped until the user pressed SPACE or UP to signify they were ready. This was achieved through a While loop, pygame event handlers and if/else statements that blit images in place each iteration until the game is started.

Pipes were created using an image found on opengameart - The heights are randomly generated but the gap between the pipes is always the same and they use the same x coordinate to ensure they're opposite each otehr.

is_game_over function checks whether the bird has hit the top/bottom of the window, or the top or bottom pipes (using pipe and bird height variables) - returning True if the game is over and False otherwise.
