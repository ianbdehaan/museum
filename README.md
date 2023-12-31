The museum.py is the main code, it deals with all the logic in the game. When someone enters the game it's run through godot with -p and command line arguments relative to the player’s name and email. When a player makes a guess in the game godot runs it with -g with the command line arguments relative to the art_id, room category, and True (if the player guessed Human) or False (if the player guessed AI). when a player tries to end the game, it's run with -e.

In the first scenario (“-p”), the player info is saved in a player.txt file and the database (for which the logic behind is implemented under the artwork_database.py) receives the new player info and the game saves the artwork info from the database under artworks.txt.

When a player makes a guess (“-g”) the museum.py figures out if they guessed it correctly and saves the info under player_guesses.txt and print it in the terminal so godot knows whether the player got it right or not. In addition to that, if this is the first guess in the room the player’s place is updated and it prints closeDoors in the terminal to tell Godot to do so. Last, if it's the last artpiece in the room it erases the player’s place and updates the database with all the guesses from the room.

Last, when a player tries to end a game (“-e”) the museum.py checks if the player is currently in the middle of a room, if it's it prints false indicating to godot it cannot leave the game yet, else it prints true, so godot can proceed with the end of the game.

I added this: With the database filled in, we use matplotlib to create graphs from the collected data. These are saved as files and exported via email.

*There are currently issues with the plotting of the data, due to an issue with importing matplotlib*
