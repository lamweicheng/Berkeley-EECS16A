# launchpadAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# EECS 16A: The Pacman game was adapted into part of the Touch 2 - Resistive
# Touchscreen lab by Shuming Xu (smxu@berkeley.edu)


from game import Agent
from game import Directions
import random
import serial


BAUD_RATE = 115200


class LaunchpadAgent(Agent):
    """
    An agent controlled by the Launchpad.
    """
    WEST_KEY = 'X = 0 Y = 1'
    EAST_KEY = 'X = 2 Y = 1'
    NORTH_KEY = 'X = 1 Y = 2'
    SOUTH_KEY = 'X = 1 Y = 0'
    STOP_KEY = 'None'

    def __init__(self, index=0, com=-1):
        test_ser = serial.Serial('COM' + str(com))
        test_ser.close()
        self.ser = serial.Serial('COM' + str(com), BAUD_RATE, timeout = 150/1000)

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = ''

    def readSensorData(self):
        # Tell MSP to collect data
        self.ser.write(b'6')

        serial_data = self.ser.readline()
        # Convert ASCII characters from serial port to integers
        serial_data_processed = ''
        for i in serial_data:
            if chr(i) != '\r' and chr(i) != '\n':
                serial_data_processed += chr(i)
        return serial_data_processed

    def getAction(self, state):
        self.keys = self.readSensorData()

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal:
            move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        move = Directions.STOP
        if (self.WEST_KEY in self.keys) and Directions.WEST in legal:
            move = Directions.WEST
        if (self.EAST_KEY in self.keys) and Directions.EAST in legal:
            move = Directions.EAST
        if (self.NORTH_KEY in self.keys) and Directions.NORTH in legal:
            move = Directions.NORTH
        if (self.SOUTH_KEY in self.keys) and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move
      
    def final(self, state):
        self.ser.close()
