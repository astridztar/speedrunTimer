#!/usr/bin/env python3
import math
import time
from threading import Event as ThreadEvent  # avoid name conflict with tkinter.Event
from threading import Thread
from tkinter import *
from tkinter import ttk
from pynput import keyboard

# make global variables
timerRunning = 0
timerStart = 0
timerEnd = 0
timeDisplay = "test"
PB = ""
PBTime = 0
UIClosed = ThreadEvent()

###############
# functions
###############


# getTimeInMilliseconds
#
# gets current system clock time in milliseconds
def getTimeInMilliseconds() -> int:
    return round(time.time() * 1000)

# convertColons
# takes in a str
# converts time to be nicely formatted
# example input: 1830120
# example output: 0h:3m:30s:120ms
def convertColons(theTime: str) -> str:
    timeInt = int(theTime)
    if timeInt > 999:
        milliseconds = int(theTime[-3:])
    else:
        milliseconds = timeInt
    seconds = (timeInt / 1000) % 60
    minutes = (timeInt / (1000 * 60)) % 60
    hours = (timeInt / (1000 * 60 * 60)) % 60
    return (
        str(math.floor(hours))
        + "h:"
        + str(math.floor(minutes))
        + "m:"
        + str(math.floor(seconds))
        + "s:"
        + str(milliseconds)
        + "ms"
    )

# toggleTimer
#
# starts timer
def toggleTimer() -> None:
    global timerRunning, timerStart, timerEnd, timeDisplay
    if timerRunning == 0:
        # buttonText.set("Stop Timer")
        timerRunning = 1
        timerStart = getTimeInMilliseconds()
        # timeDisplay = str(getTimeInMilliseconds() - timerStart)
        return
    else:
        # buttonText.set("Start Timer")
        # timerRunning = 0
        # timerEnd = getTimeInMilliseconds() - timerStart
        # timeDisplay = str(timerEnd)
        return

# stopTimer
#
# stops timer and resets timerStart
def stopTimer() -> None:
    global timerRunning, timerStart, timerEnd, timeDisplay, PB, PBTime
    timerRunning = 0
    if timerStart == 0:
        return
    timerEnd = getTimeInMilliseconds() - timerStart
    timerStart = 0
    timeDisplay = convertColons(str(timerEnd))

    if PBTime == 0 or PBTime > timerEnd:
        PBTime = timerEnd
        PB = timeDisplay
    return

# updateTimerLabel
#
# updates label to display current time
def updateTimerLabel() -> None:
    global timeDisplay, timerStart, timerEnd

    if timerStart > 0:
        timeDisplay = str(getTimeInMilliseconds() - timerStart)
        timeDisplay = convertColons(timeDisplay)
    else:
        timeDisplay = str(timerEnd)
        timeDisplay = convertColons(timeDisplay)

    timeLabel.set(timeDisplay)
    PBLabel.set("PB: " + PB)
    root.after(10, updateTimerLabel)
    return

# createKeyboardListener
#
# supposed to create a listener for keyboard input
def createKeyboardListener() -> None:
    global UIClosed

    with keyboard.Listener(on_press=onKeyPress) as listener:
        UIClosed.wait()  # wait for UI to close
        listener.stop()  # stop listener

# onKeyPress
#
# handle key that is being pressed
def onKeyPress(key: keyboard.Key | keyboard.KeyCode) -> None:
    try:
        if key.char == "z":
            toggleTimer()
        elif key.char == "x":
            stopTimer()
        elif key.char == "c":
            resetPB()
    except AttributeError:
        # Special keys, we don't care about them
        # Example: CTRL, ALT, ESC, etc.
        pass

# resetTimer
#
# resets global variables back to default
def resetTimer() -> None:
    global timeDisplay, timerStart, timerEnd, timerRunning
    timeDisplay = "0"
    timerStart = 0
    timerEnd = 0
    return

def resetPB():
    global PB, PBTime
    PBTime = 0
    PB = ""
    return

###################
# execute
###################

# run display & mainloop
root = Tk()
# text = root.Text(width = 32, height = 4, font=("Helvetica", 32))
# text.pack()
root.title("astrid ztar's speedrun timer")
root.geometry("500x180")

img = Image("photo", file="appicon.png")
root.tk.call('wm','iconphoto',root._w,img)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# TO-DO: style
style = ttk.Style(root)
style.configure("TLabel", font=("Terminal", 18))
style.configure("TButton", font=("Terminal", 12))
# style.configure(background='yellow')

# labels & buttons
timeLabel = StringVar()
PBLabel = StringVar()
buttonText = StringVar()
button2Text = StringVar()
button3Text = StringVar()
buttonText.set("Start")
button2Text.set("Stop")
button3Text.set("Reset PB")

ttk.Label(mainframe, textvariable=timeLabel).grid(column=1, row=1, sticky=W)
# style.configure('TLabel',font=('Terminal', 12))
ttk.Label(mainframe, textvariable=PBLabel).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, textvariable=buttonText, command=toggleTimer).grid(
    column=1, row=3, sticky=W
)
ttk.Button(mainframe, textvariable=button2Text, command=stopTimer).grid(
    column=1, row=4, sticky=W
)
ttk.Button(mainframe, textvariable=button3Text, command=resetPB).grid(
    column=1, row=5, sticky=W
)

# constantly keep track of timer label
updateTimerLabel()

# keyboard thread
keyboard_thread = Thread(target=createKeyboardListener)
keyboard_thread.start()

# run tkinter loop (blocking)
root.mainloop()

# loop stopped, shut down keyboard listener
UIClosed.set()
keyboard_thread.join()
