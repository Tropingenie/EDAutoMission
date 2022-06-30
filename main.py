# main.py
# by Pon Pon
# High-level, functional execution of the main goal of the script (to automate
# selection of various missions, and checking of the mission board every 10
# minutes) in a DLC agnostic manner.

import logging
from time import sleep, localtime 
from queue import Empty
from platform import system

import helper_functions

if system() == "Windows":
    from pywintypes import error as PyWinError
    from tab_to import tab_to

def _main(game_interaction):
    missions = 0

    def _accept_mission(mission_type):
        logging.info("{} mission detected. Accepting...".format(mission_type))
        game_interaction.accept_mission()
        missions += 1

    logging.info("Checking missions...")

    game_interaction.open_missions_board()
    while not game_interaction.at_bottom():
        mission_text = game_interaction.ocr_mission()
        if "BERT" in mission_text:
            _accept_mission("Bertrandite")
        elif "GOLD" in mission_text:
            _accept_mission("Gold")
        elif "SILVER" in mission_text:
            _accept_mission("Silver")

        game_interaction.next_mission()
    # Note: at_bottom() must be set up to avoid an off by one error
    game_interaction.return_to_starport()

    logging.info("Mission check complete.")
    return missions

def main():
    missions = 0
    helper_functions.module_setup()
    if not helper_functions.game_running():
        raise OSError("Elite: Dangerous not running!")

    try:
        raise OSError("Win 11 debug")
        if system() == "Windows":
            tab_to("Elite.+Dangerous.+CLIENT")
            sleep(1)
        else:
            raise OSError("Automatic alt tab only works on Windows")
    except (PyWinError, OSError) as e:
        logging.debug("Excepted PyWinError: {}".format(e))
        logging.info("Please focus on the Elite window before timer expires.")
        i = 5
        while i >= 0:
            logging.info("Starting script in: {}".format(i))
            sleep(1)
            i -= 1

    game_mode = helper_functions.game_mode()
    if game_mode == "horizons":
        import horizons as game_interaction
        logging.info("Operating in Horizons mode")
    elif game_mode == "odyssey":
        from odyssey import OdysseyHelper as game_interaction
        logging.info("Operating in Odyssey mode")

    missions = game_interaction.check_missions_accepted()
    logging.info("Detected that {} missions already in depot.".format(missions))

    sleep(1)  # Brief pause to prevent errors

    missions += _main(game_interaction) # Initial check
    logging.info(
        "Script will now be run every 10 minutes, on the 5 minute mark (e.g. {}:{})".format(
            int(localtime()[3]),
            int(round(localtime()[4], -1))+5
            )
        )

    mission_count_update = False
    while missions < 20:
        logging.debug("Current minute reading is: {}".format(localtime()[4]))
        # To check every 10 minutes, we look when the clock reads the 5 minute mark
        # e.g. for 1:55, time.gmtime()[4] will be 55, 55+5=60, 60%10 == 0
        if ((localtime()[4] + 5) % 10 == 0):
<<<<<<< HEAD
            missions += _main(game_interaction)
=======
            missions += _main(game_interaction) # debug
>>>>>>> 8ed57194759b01256798772b38cd47cac170f3e8
            mission_count_update = True
        if mission_count_update:
            mission_count_update = False
            logging.info("{} missions in depot.".format(missions))
            logging.info("Next update at {}:{}".format(
                int(localtime()[3]),
                int(round(localtime()[4], -1))+5
                )
            )
        sleep(20) # Slows loop rate to thrice per minute

if __name__ == "__main__":
    main()

