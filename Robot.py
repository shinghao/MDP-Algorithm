import math
import pygame
import os
import Constants
from Simulator import Sim
from griddyworld import pair

ROBOT_IMG_FILE = pygame.image.load(os.path.join('Assets', 'Robot.png'))

'''
The Robot class handles the movement and rendering of the robot
'''

ONE_CELL = 10 * Constants.UNIT
TURN_LEFT_X, TURN_LEFT_Y = 40 * Constants.UNIT, 20 * Constants.UNIT
TURN_RIGHT_X, TURN_RIGHT_Y = 50 * Constants.UNIT, 30 * Constants.UNIT


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

        self.is_moving = False

    def get_is_moving(self):
        return self.is_moving

    def set_is_moving(self, value: bool):
        self.is_moving = value

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

    def __move_step_towards(self, obj, target_pos, target_dir, velocity):
        """Move obj towards target_pos at velocity and rotate towards target_dir."""

        # Calculate direction vector towards target
        dx = target_pos[0] - self.pos[0]
        dy = target_pos[1] - self.pos[1]
        target_direction = math.atan2(dy, dx)

        # Calculate velocity vector based on direction and speed
        vx = velocity * math.cos(target_direction)
        vy = velocity * math.sin(target_direction)

        # Interpolate towards target direction
        direction = math.atan2(math.sin(
            target_dir - target_direction), math.cos(target_dir - target_direction))

        # Update object position and rotation
        obj.rect.move_ip(vx, vy)
        obj.image = pygame.transform.rotate(
            obj.original_image, math.degrees(-direction))
        obj.rect = obj.image.get_rect(center=obj.rect.center)

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

        self.set_is_moving(True)
        while not self.is_movement_complete(target_pos):
            self.__move_a_step(-self.velocity, 0)
        self.__adjust_robot(target_pos, initial_angle)

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

        self.set_is_moving(True)
        while not self.is_movement_complete(target_pos):
            self.__move_a_step(self.velocity, 0)
        self.__adjust_robot(target_pos, initial_angle)

    def move_left_forward(self):
        """
        Turns the robot forward and left based on the turning radius
        """
        target_pos = initial_pos = self.get_pos()
        target_angle = initial_angle = math.degrees(self.get_angle())

        # Determine target position & angle
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + \
                pair(-TURN_LEFT_X, -TURN_LEFT_Y)
            target_angle = Constants.WEST

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + \
                pair(TURN_LEFT_X, -TURN_LEFT_Y)
            target_angle = Constants.NORTH

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + \
                pair(TURN_LEFT_X, TURN_LEFT_Y)
            target_angle = Constants.EAST

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + \
                pair(-TURN_LEFT_X, TURN_LEFT_Y)
            target_angle = Constants.SOUTH

        self.set_is_moving(True)
        while not self.is_movement_complete(target_pos):
            self.__move_a_step_oval(self.velocity, 1, -1,
                                    TURN_LEFT_X, TURN_LEFT_Y)

        self.__adjust_robot(target_pos, target_angle)

    def move_right_forward(self):
        """
        Turns the robot forward and right based on the turning radius
        """
        target_pos = initial_pos = self.get_pos()
        target_angle = initial_angle = math.degrees(self.get_angle())

        # Determine target position & angle
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + \
                pair(TURN_RIGHT_X, -TURN_RIGHT_Y)
            target_angle = Constants.EAST

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + \
                pair(TURN_RIGHT_X, TURN_RIGHT_Y)
            target_angle = Constants.SOUTH

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + \
                pair(-TURN_RIGHT_X, TURN_RIGHT_Y)
            target_angle = Constants.WEST

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + \
                pair(-TURN_RIGHT_X, -TURN_RIGHT_Y)
            target_angle = Constants.NORTH

        self.set_is_moving(True)

        while not self.is_movement_complete(target_pos):
            self.__move_a_step_oval(-self.velocity, -1, 1,
                                    TURN_RIGHT_X, TURN_RIGHT_Y)

        self.__adjust_robot(target_pos, target_angle)
        # print(abs(self.get_pos().get()[0] - target_pos.get()[0]), abs(self.get_pos().get()[1] - target_pos.get()[1]))

    def move_left_backward(self):
        """
        Turns the robot forward and left based on the turning radius
        """
        target_pos = initial_pos = self.get_pos()
        target_angle = initial_angle = math.degrees(self.get_angle())

        # Determine target position & angle
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + \
                pair(-TURN_LEFT_X, TURN_LEFT_Y)
            target_angle = Constants.EAST

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + \
                pair(-TURN_LEFT_X, -TURN_LEFT_Y)
            target_angle = Constants.SOUTH

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + \
                pair(TURN_LEFT_X, -TURN_LEFT_Y)
            target_angle = Constants.WEST

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + \
                pair(TURN_LEFT_X, TURN_LEFT_Y)
            target_angle = Constants.NORTH

        self.set_is_moving(True)
        while not self.is_movement_complete(target_pos):
            self.__move_a_step_oval(
                -self.velocity, 1, -1, TURN_LEFT_X, TURN_LEFT_Y)

        self.__adjust_robot(target_pos, target_angle)

    def move_right_backward(self):
        """
        Turns the robot forward and right based on the turning radius
        """
        target_pos = initial_pos = self.get_pos()
        target_angle = initial_angle = math.degrees(self.get_angle())

        # Determine target position & angle
        if initial_angle == Constants.NORTH:
            target_pos = initial_pos + \
                pair(TURN_RIGHT_X, TURN_RIGHT_Y)
            target_angle = Constants.WEST

        elif initial_angle == Constants.EAST:
            target_pos = initial_pos + \
                pair(-TURN_RIGHT_X, +TURN_RIGHT_Y)
            target_angle = Constants.NORTH

        elif initial_angle == Constants.SOUTH:
            target_pos = initial_pos + \
                pair(-TURN_RIGHT_X, -TURN_RIGHT_Y)
            target_angle = Constants.EAST

        elif initial_angle == Constants.WEST:
            target_pos = initial_pos + \
                pair(TURN_RIGHT_X, -TURN_RIGHT_Y)
            target_angle = Constants.SOUTH

        self.set_is_moving(True)
        while not self.is_movement_complete(target_pos):
            self.__move_a_step_oval(self.velocity, -1,
                                    1, TURN_RIGHT_X, TURN_RIGHT_Y)
        self.__adjust_robot(target_pos, target_angle)

    def __move_a_step(self, velocity, angle_direction):
        # angle_direction determines if object is moving in negative or postive direction
        step = pair(math.sin(self.angle), math.cos(self.angle)) * velocity
        self.set_pos(self.pos + step)
        self.set_angle(self.angle + angle_direction *
                       (self.velocity / self.turn_radius))
        self.sim.refresh_screen()

    def __move_a_step_oval(self, velocity, x_dir, y_dir, radius_x, radius_y):
        # angle_direction determines if object is moving in negative or postive direction
        theta = self.angle + (velocity / radius_x)
        x = radius_x * math.cos(theta)
        y = radius_y * math.sin(theta)
        dx = (x - radius_x * math.cos(self.angle)) * x_dir
        dy = (y - radius_y * math.sin(self.angle)) * y_dir
        self.set_pos(self.pos + pair(dx, dy))
        self.set_angle(theta)
        self.sim.refresh_screen()

    def __adjust_robot(self, target_pos, target_angle):
        '''
        This function ensures that robot sits perfectly on the grid cell
        This is required as the angle/position might be off by a tiny margin when the robot finish executing each instruction
        '''
        self.set_pos(target_pos)
        self.set_angle(math.radians(target_angle))
        self.set_is_moving(False)
        self.sim.refresh_screen()

    def render_robot(self):
        '''
        This function uses WIN.blit method to render the robot image based on it's position and rotation
        '''
        new_angle = math.degrees(self.angle)
        rotated_robot = pygame.transform.rotate(self.img, new_angle)
        self.window.blit(rotated_robot, (self.get_pos().get()))
