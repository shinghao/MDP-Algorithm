import math
import pygame
import os
import Constants

ROBOT_IMG_FILE = pygame.image.load(os.path.join('Assets', 'Robot.png'))

'''
The Robot class handles the movement and rendering of the robot
'''


class Robot:
    def __init__(self, window):

        # Initialise the position of the robot on the x and y axis
        self.pos_x = Constants.ROBOT_START_X
        self.pos_y = Constants.ROBOT_START_Y

        # Initialise the angle(orientation) of the robot
        self.angle = Constants.ROBOT_START_ANGLE

        # Initialise the velocity(speed) of the robot
        self.velocity = Constants.ROBOT_VEL

        # Initialise the turning radius of the robot
        self.turn_radius = Constants.ROBOT_TURN_RADIUS

        # Initialise the robot's sprite image
        self.img = pygame.transform.scale(
            ROBOT_IMG_FILE, (Constants.ROBOT_WIDTH, Constants.ROBOT_HEIGHT))

        # Initialise the pygame window
        self.window = window
        self.render_robot()

    def get_x_coord(self):

        return self.pos_x

    def get_y_coord(self):
        return self.pos_y

    def get_angle(self):
        return self.angle

    def set_coordinates(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_orientation(self, angle):
        self.angle = angle

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def move_forward(self):
        """
        Moves the robot forward in the direction of its orientation
        """
        self.pos_x += self.velocity * math.sin(self.angle)
        self.pos_y -= self.velocity * math.cos(self.angle)

    def move_backward(self):
        """
        Moves the robot backward in the opposite direction of its orientation
        """
        self.pos_x += self.velocity * \
            math.sin(self.angle)
        self.pos_y += self.velocity * \
            math.cos(self.angle)

    def move_left_forward(self):
        """
        Turns the robot forward and left based on the turning radius
        """
        self.pos_x += self.velocity * math.sin(self.angle)
        self.pos_y -= self.velocity * math.cos(self.angle)
        self.angle -= (self.velocity / self.turn_radius)

    def move_right_forward(self):
        """
        Turns the robot forward and right based on the turning radius
        """
        self.pos_x += self.velocity * math.sin(self.angle)
        self.pos_y -= self.velocity * math.cos(self.angle)
        self.angle += (self.velocity / self.turn_radius)

    def render_robot(self):
        '''
        This function uses WIN.blit method to render the robot image based on it's position and rotation
        '''
        new_angle = math.degrees(self.angle) * -1
        rotated_robot = pygame.transform.rotate(self.img, new_angle)
        self.window.blit(rotated_robot, (self.pos_x, self.pos_y))
