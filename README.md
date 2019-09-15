# flappy_bird

Flappy bird game using Python
- flappy_bird.py: Regular version for Flappy bird game
- flappy_bird_ai.py: Implemented AI for gameplay using NEAT algorithm
- Implemented following tutorial https://www.youtube.com/watch?v=OGHA-elMrxI

# Instructions

1. Run flappy_bird.py for regular gameplay:
- Press S to start the game
- Control the bird by pressing SpaceBar, Enter or Up keys on keyboard.

2. Run flappy_bird_ai.py to watch the AI train itself to play the game

# Features
Default features:
- DRAW_LINES (Default to True)
    Plot the lines between birds and pipes to show what the bird "sees" 
- FPS (Default to 15 for flappy_bird.py, 120 for flappy_bird_ai.py)
    Determine the speed at which the frame is refreshed. Higher FPS indicates faster gameplay

1. Feature for flappy_bird.py
- HARD_MODE (Default to False)
  Enable to play the game at twice the set FPS, and pipes will be generated at random interval

2. Features for flappy_bird_ai.py
- CHECKPOINT (Default to False)
    Save checkpoint at every NUM_CHECKPOINT generation, and restore to the last checkpoint after the initial training
    Update the winner-genome at the end
- NUM_CHECKPOINT (Default to 2)
    Number of generations between each saved checkpoint
- BREAK_SCORE (Default to 50)
    The score where the game stops during initial training
    Note: if want to disable "break score" during training, please set the variable "break_score" under main() function to "False"
