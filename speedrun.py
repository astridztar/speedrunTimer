from tkinter import *
from tkinter import ttk
import time
import math
from pynput import keyboard
from threading import Thread
import pygame, sys
from pygame.locals import *
from tkinter.font import Font

# make global variables
timerRunning = 0
timerStart = 0
timerEnd = 0
timeDisplay = 'test'
PB = ''
PBTime = 0

###############
# functions
###############

# getTimeInMilliseconds
#
# gets current system clock time in milliseconds
def getTimeInMilliseconds():
	return round(time.time() * 1000)

# convertColons
# takes in a str
# converts time to be nicely formatted
# example input: 1830120
# example output: 0h:3m:30s:120ms
def convertColons(theTime):
	timeInt = int(theTime)
	if timeInt > 999:
		milliseconds = int(theTime[-3:])
	else:
		milliseconds = timeInt
	seconds = (timeInt/1000)%60
	minutes = (timeInt/(1000*60))%60
	hours = (timeInt/(1000*60*60))%60
	return (str(math.floor(hours)) + "h:" + str(math.floor(minutes)) + "m:" + str(math.floor(seconds)) + "s:" + str(milliseconds) + "ms")

# toggleTimer
#
# starts timer
def toggleTimer():
	global timerRunning, timerStart, timerEnd, timeDisplay
	if(timerRunning == 0):
		#buttonText.set("Stop Timer")
		timerRunning = 1
		timerStart = getTimeInMilliseconds()
		#timeDisplay = str(getTimeInMilliseconds() - timerStart)
		return
	else:
		#buttonText.set("Start Timer")
		#timerRunning = 0
		#timerEnd = getTimeInMilliseconds() - timerStart
		#timeDisplay = str(timerEnd)
		return

# stopTimer
#
# stops timer and resets timerStart
def stopTimer():
	global timerRunning, timerStart, timerEnd, timeDisplay, PB, PBTime
	timerRunning = 0
	if(timerStart == 0):
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
def updateTimerLabel():
	global timeDisplay, timerStart, timerEnd
	if(timerStart > 0):
		timeDisplay = str(getTimeInMilliseconds() - timerStart)
		timeDisplay = convertColons(timeDisplay)
	else:
		timeDisplay = str(timerEnd)
		timeDisplay = convertColons(timeDisplay)
	timeLabel.set(timeDisplay)
	PBLabel.set("PB: " + PB)
	root.after(10, updateTimerLabel)
	#if keyboard.is_pressed('z'):
	#if keyboard.is_pressed('x'):
	return

# on_press
#
# not sure if this even works
def on_press(key):
	print('inside on_press')
	if key == keyboard.Key.z:
		print('pressed z')
		toggleTimer()
	elif key == keyboard.Key.x:
		stopTimer()
	print('leaving on_press')

# checkKeyboard
#
# supposed to check for keyboard input
# & execute methods as if a ui button was pressed
def checkKeyboard():
	# get key press
	key=pygame.key.get_pressed()
	# check if key pressed is z or x
	if key[pygame.K_z]:
		print('z pressed')
		toggleTimer()
	if key[pygame.K_x]:
		print('x pressed')
		stopTimer()
	# keep checking keyboard
	root.after(1, checkKeyboard)
	return

# resetTimer
#
# resets global variables back to default
def resetTimer():
	global timeDisplay, timerStart, timerEnd, timerRunning
	timeDisplay = '0'
	timerStart = 0
	timerEnd = 0
	return

###################
# execute
###################

# run display & mainloop
root = Tk()
#text = root.Text(width = 32, height = 4, font=("Helvetica", 32))
#text.pack()
root.title("astrid ztar's speedrun timer")
root.geometry('500x180')
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# TO-DO: style
style = ttk.Style(root)
style.configure('TLabel', font=('Terminal', 24))
style.configure('TButton', font=('Terminal', 12))

# labels & buttons
timeLabel = StringVar()
PBLabel = StringVar()
buttonText = StringVar()
button2Text = StringVar()
buttonText.set("Start Timer")
button2Text.set("Stop Timer")
ttk.Label(mainframe, textvariable=timeLabel).grid(column=2, row=1, sticky=(W))
#style.configure('TLabel',font=('Terminal', 12))
ttk.Label(mainframe, textvariable=PBLabel).grid(column=2, row=4, sticky=(W))
ttk.Button(mainframe, textvariable=buttonText, command=toggleTimer).grid(column=2, row=2, sticky=W)
ttk.Button(mainframe, textvariable=button2Text, command=stopTimer).grid(column=2, row=3, sticky=W)

# constantly keep track of timer label
updateTimerLabel()

# init pygame for keyboard input?
pygame.init()
#screen = pygame.display.set_mode((200,100))

# hypothetically: another thread to run keyboard input
with keyboard.Listener(on_press=on_press) as listener:
	print('thread started')
	thread = Thread(target=checkKeyboard)
	thread.start()
	#listener.start()

# root mainloop
root.mainloop()
