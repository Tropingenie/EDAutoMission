# gui.py
# by Pon Pon
# Provide GUI functionality to the script. Note that much of this code was taken
# from https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Multithreaded_Logging.py

import logging
import threading
from queue import Queue, Empty

import PySimpleGUIQt as sg

import helper_functions
from main import main


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


if __name__ == "__main__":
    try:
        helper_functions.module_setup()
    except NotImplementedError as e:
        logging.error(e)

    output = sg.Output()

    layout = [
        [sg.Button("Start")],
        [sg.Button("Quit")],
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

        # Poll queue
        try:
            record = log_queue.get(block=False)
        except Empty:
            pass
        else:
            msg = queue_handler.format(record)
            output.write(msg.strip("\r\n")+'\n')

    window.close()