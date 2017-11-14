# War
Simulator for the card game war, used to find average game length

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
  - Cards are shuffled before returning to the deck. Remove self.shuffle() inside the reset method to turn this off (line 83 default)
  
Results with shuffling:
  - The average game takes about 200-250 rounds
  - Game lengths follow a pretty nice curve
  - Longest game is usually around 2000 rounds
  - No games went infinite
  - 0.4% of games ended after less than 26 rounds, which means that fewer rounds were played than the number of cards each player started with
  
Results without shuffling:
  - Average game takes about 500 rounds
  - Longest game mostly at around 4000 rounds, highest observed is at 6100
  - 10-11% of all games go infinite. Increasing the threshold to 100.000 rounds did nothing except increase runtime drastically
  
  
Conclusion:
  If you want to finish a game of War, shuffle your cards. If you wanna have fun, play something else
