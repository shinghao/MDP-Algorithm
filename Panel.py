import Constants
import Button


class Panel(object):

    def __init__(self, window):
        self.window = window
        self.buttons = []
        self.reset_button = Button.Button(window, Constants.COLOR_BTN_RESET, Constants.BTN_RESET_X,
                                          Constants.BTN_RESET_Y, Constants.BTN_WIDTH, Constants.BTN_HEIGHT, "Reset", Constants.BTN_FONT_SIZE, Constants.WHITE, Constants.BTN_STATE_RESET)
        self.buttons.append(self.reset_button)
        self.start_button = Button.Button(window, Constants.COLOR_BTN_START, Constants.BTN_START_X,
                                          Constants.BTN_START_Y, Constants.BTN_WIDTH, Constants.BTN_HEIGHT, "Start", Constants.BTN_FONT_SIZE, Constants.WHITE, Constants.BTN_STATE_START)
        self.buttons.append(self.start_button)

    def render_panel(self):
        for button in self.buttons:
            button.render_button()

    def check_button_pressed(self):
        for button in self.buttons:
            if button.is_pressed():
                return button.get_function()
