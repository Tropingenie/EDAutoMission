# main.py
# by Pon Pon
# High-level, functional execution of the main goal of the script (to automate
# selection of various missions, and checking of the mission board every 10
# minutes) in a DLC agnostic manner.

import logging
from time import sleep

import helper_functions

missions = 0  # Tracks number of missions accepted

def main():
    global missions
    game_interaction.open_missions_board()
    while not game_interaction.at_bottom():
        mission_text = game_interaction.ocr_mission()
        if "BERT" in mission_text or "GOLD" in mission_text or "SILVER" in mission_text:
            game_interaction.accept_mission()
            missions += 1
        game_interaction.next_mission()
# Note: at_bottom() must be set up to avoid an off by one error
    game_interaction.return_to_starport()

if __name__ == "__main__":
    helper_functions.module_setup()
    game_mode = helper_functions.game_running()
    if game_mode == "horizons":
        import horizons as game_interaction
        logging.debug("Operating in Horizons mode")
    elif game_mode == "odyssey":
        from odyssey import OdysseyHelper as game_interaction
    else:
        raise OSError("Elite: Dangerous not running!")
    sleep(5) # Wait for user to alt-tab to Elite window
    main() # Initial check
    # helper_functions.call_every_10(main) # Call main once every 10 minutes