# gui.py
# by Pon Pon
# Provide GUI functionality to the script. Note that much of this code was taken
# from https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Multithreaded_Logging.py

import logging
import threading
from queue import Queue, Empty

import PySimpleGUIQt as sg

import helper_functions
from main import main, addMission, removeMission, getMissions


class ThreadedApp(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.kill_queue = Queue()
        self._stop_event = threading.Event()

    def run(self):
        # Note: In production, we want the system to mask any exceptions instead of crashing.
        try:
            main()
        except Exception as e:
            logging.error("Error: {}".format(e))
            raise # Reraise the error to prevent masking

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


def updateMissions(updateWindows):
    i = 0
    missionList = ""
    missionArray = []
    for mission in getMissions():
        i = i+1
        missionList += str(i) +". " + str(mission[1] + "\n")
        missionArray.append(mission[1])
        if updateWindows:
            window["missionList"].update(missionList)
            window["removalDropdown"].update(values=missionArray)
    return [missionList, missionArray]

if __name__ == "__main__":
    try:
        helper_functions.module_setup()
    except NotImplementedError as e:
        logging.error(e)

    output = sg.Output(key="output")

    layout = [
        [sg.Button("Start")],
        [sg.Button("Quit")],
        [sg.Text("Add missions to check for:")],
        [sg.InputText("Mission detection text...", key="missionDetection"), sg.InputText("Mission label...", key="missionType"), sg.Button("Add mission", size=[25,1])],
        [sg.Text(updateMissions(False)[0], key="missionList")],
        [sg.Combo(values=updateMissions(False)[1], key="removalDropdown"), sg.Button("Remove mission", size=[25,1])],
        [output]
    ]

    window = sg.Window(title="Baking Bot", layout=layout, size=(900,300))

    # Setup logging and start app
    logger = logging.getLogger()
    log_queue = Queue()
    queue_handler = QueueHandler(log_queue)
    queue_handler.setLevel(level=logging.INFO)
    logger.addHandler(queue_handler)
    threadedApp = ThreadedApp()
    appStarted = False
    
    # Mainloop
    while True:
        event, values = window.read(timeout=100)
        if event == "Start":
            if not appStarted:
                logging.info("Starting script")
                threadedApp.start()
                window["Start"].update(disabled=True)
                appStarted = True
        if event in ["Quit", sg.WIN_CLOSED]:
            if appStarted:
                logging.info("Stopping script")
                threadedApp.stop()
                appStarted = False
            break

        if event == "Add mission":
            logging.info("Added {} to the list".format(values["missionType"]))
            #Add mission to list (missions_needed) in main.py
            addMission(values["missionDetection"].upper(), values["missionType"])

            #Update list in gui
            updateMissions(True)

        if event == "Remove mission":
            for mission in getMissions():
                if mission[1] == values["removalDropdown"]:

                    #Remove mission from list
                    removeMission(mission)

                    #Update GUI after removing mission check
                    updateMissions(True)
                    logging.info("Removed {} from the list".format(mission[1]))

        # Poll queue
        try:
            record = log_queue.get(block=False)
        except Empty:
            pass
        else:
            msg = queue_handler.format(record)
            output.write(msg.strip("\r\n")+'\n')

    window.close()