import telepot
from pprint import pprint
cubot=telepot.Bot('351057354:AAFk5gALlI2AqCqcCh4EAwR35BzSs1Kq8bA')
updates=cubot.getUpdates()
# pprint(updates)
# from telepot.loop import MessageLoop
# def handle(msg):
#      pprint(msg)
# MessageLoop(cubot, handle).run_as_thread()

# store updates to database
