import math
import pygame
import os
import Constants
from Simulator import Sim
from Pair import pair

ROBOT_IMG_FILE = pygame.image.load(os.path.join('Assets', 'Robot.png'))

'''
The Robot class handles the movement and rendering of the robot
'''

ONE_CELL = 10 * Constants.UNIT


class Robot:

    def __init__(self, window, sim: Sim, pos: pair):

        # Initialise the position of the robot on the x and y axis
        self.pos = pos

        # Initialise the angle(orientation) of the robot
        self.angle = Constants.ROBOT_START_ANGLE

        # Initialise the velocity(speed) of the robot
        self.velocity = Constants.ROBOT_VEL

        # Initialise the turning radius of the robot
        self.turn_radius = Constants.ROBOT_TURN_RADIUS

        # Initialise the robot's sprite image
        self.img = pygame.transform.scale(
            ROBOT_IMG_FILE, (Constants.ROBOT_WIDTH, Constants.ROBOT_HEIGHT))

        self.window = window
        self.sim = sim

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle

    # Returns a pair object
    def get_pos(self):
        return self.pos

    def set_pos(self, pos: pair):
        self.pos = pos

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def is_movement_complete(self, target_pos: pair):
        return abs(self.get_pos().get()[0] - target_pos.get()[0]) < self.velocity and abs(
            self.get_pos().get()[1] - target_pos.get()[1]) < self.velocity

    def move_forward(self):
        """
        Moves the robot forward in the direction of its orientation
        """
        initial_pos = self.get_pos()
        initial_angle = math.degrees(self.get_angle())
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + pair(0, -ONE_CELL)

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + pair(ONE_CELL, 0)

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + pair(0, ONE_CELL)

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + pair(-ONE_CELL, 0)

        while not self.is_movement_complete(target_pos):
            step = pair(math.sin(self.angle), math.cos(self.angle))
            step *= -self.velocity
            self.set_pos(self.pos + step)
            self.sim.refresh_screen()
        self.set_pos(target_pos)
        self.sim.refresh_screen()

    def move_backward(self):
        """
        Moves the robot backward in the opposite direction of its orientation
        """
        initial_pos = self.get_pos()
        initial_angle = math.degrees(self.get_angle())
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + pair(0, ONE_CELL)

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + pair(-ONE_CELL, 0)

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + pair(0, -ONE_CELL)

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + pair(ONE_CELL, 0)

        while not self.is_movement_complete(target_pos):
            step = pair(math.sin(self.angle), math.cos(self.angle))
            step *= self.velocity
            self.set_pos(self.pos + step)
            self.sim.refresh_screen()
        self.set_pos(target_pos)
        self.sim.refresh_screen()

    def move_left_forward(self):
        """
        Turns the robot forward and left based on the turning radius
        """
        target_pos = initial_pos = self.get_pos()
        target_angle = initial_angle = math.degrees(self.get_angle())

        # Determine target position & angle
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + \
                pair(-self.turn_radius, -self.turn_radius)
            target_angle = Constants.WEST

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + \
                pair(self.turn_radius, -self.turn_radius)
            target_angle = Constants.NORTH

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + \
                pair(self.turn_radius, self.turn_radius)
            target_angle = Constants.EAST

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + \
                pair(-self.turn_radius, self.turn_radius)
            target_angle = Constants.SOUTH

        while not self.is_movement_complete(target_pos):
            step = pair(math.sin(self.angle), math.cos(self.angle))
            step *= -self.velocity
            self.set_pos(self.pos + step)
            self.set_angle(self.angle + (self.velocity / self.turn_radius))
            self.sim.refresh_screen()
        self.set_pos(target_pos)
        self.set_angle(math.radians(target_angle))
        self.sim.refresh_screen()

    def move_right_forward(self):
        """
        Turns the robot forward and right based on the turning radius
        """
        target_pos = initial_pos = self.get_pos()
        target_angle = initial_angle = math.degrees(self.get_angle())

        # Determine target position & angle
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + \
                pair(self.turn_radius, -self.turn_radius)
            target_angle = Constants.EAST

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + \
                pair(self.turn_radius, self.turn_radius)
            target_angle = Constants.SOUTH

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + \
                pair(-self.turn_radius, self.turn_radius)
            target_angle = Constants.WEST

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + \
                pair(-self.turn_radius, -self.turn_radius)
            target_angle = Constants.NORTH

        while not self.is_movement_complete(target_pos):
            step = pair(math.sin(self.angle), math.cos(self.angle))
            step *= -self.velocity
            self.set_pos(self.pos + step)
            self.set_angle(self.angle - (self.velocity / self.turn_radius))
            self.sim.refresh_screen()
        self.set_pos(target_pos)
        self.set_angle(math.radians(target_angle))
        self.sim.refresh_screen()

    def render_robot(self):
        '''
        This function uses WIN.blit method to render the robot image based on it's position and rotation
        '''
        new_angle = math.degrees(self.angle)
        rotated_robot = pygame.transform.rotate(self.img, new_angle)
        self.window.blit(rotated_robot, (self.get_pos().get()))