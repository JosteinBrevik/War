# War
Simulator for the card game war, in order to find average game length

Simulates two players playing a game of war, until one of them wins.
By simulating a bunch of games, average game length, longest game and number of "infinite"/drawn games are found
The resulting graph of game lenghts is displayed in plotly

Uses the following rules (Norwegian style):
  - For each round, both players remove their top card, and compare those. The player with the highest card receives both
  - If there is a draw, both players add their next three cards to the pot (in addition to the cards that caused the draw), 
    and the player that wins the next round receives all cards in the pot
  - Won cards are placed in a seperate pile. When a player runs out of cards in their deck, they shuffle their pile of won cards and 
    continue playing with that pile
    
Standard values for the statistics:
  - 100.000 games are played
  - Threshold for a drawn game is at 10.000 rounds
  - On the graph, results are grouped into chunks of 25, i.e. game lengths between 100-125 are counted together. Gives a smoother curve
  
