Recommendations:

For Creating a GUI I would recommend using Tkinter and creating a button representing each hexagon. When that button is clicked 
then depending on which player's turn it will channge color. All the functional code for the game to work is already made.
If you decide to use Pygame or a diffeent thing for the GUI it might be more work.

For creating alpha beta prunning. You would need to call the evaluator for every possible move. I created a basic evaluator which we can fine tune,
but how it works iss by getting segements. To use the evaluator it would require you to most likely copy hex_states or do something else. 
If the function has to be change to have hex_states as parameter instead of using self to make easier let me know.

For iterative deeping I would recommend it being time based such as keep going as long as time < 10 seconds for example. We would need to create
a new function for each number of moves ahead or allow that to be taken as an input in the same function.
