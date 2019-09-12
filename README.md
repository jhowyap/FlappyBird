# flappy_bird

Flappy bird game using Python
- Implemented AI for gameplay using NEAT algorithm
- Implemented following tutorial https://www.youtube.com/watch?v=OGHA-elMrxI

# Instructions

Run flappy_bird.py to watch the AI train itself to play the game

Default features:
- DRAW_LINES (Default to True)
    Plot the lines between birds and pipes to show what the bird "sees" 
- CHECKPOINT (Default to False)
    Save checkpoint at every NUM_CHECKPOINT generation, and restore to the last checkpoint after the initial training
    Update the winner-genome at the end
- NUM_CHECKPOINT (Default to 2)
    Number of generations between each saved checkpoint
- BREAK_SCORE (Default to 50)
    The score where the game stops during initial training
    Note: if want to disable "break score" during training, please set the variable "break_score" under main() function to "False"
  
