import pygame


class Button:

    def __init__(self, surface, color, x, y, length, height, text, font_size, text_color, function):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.width = 0
        self.text = text
        self.text_color = text_color
        self.function = function

        self.rect = pygame.Rect(x, y, length, height)
        self.font_size = font_size
        self.my_font = pygame.font.SysFont("Calibri", self.font_size)

        self.render_button()

    def is_pressed(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)

    def get_function(self):
        return self.function

    def render_button(self):
        for i in range(1, 3):
            s = pygame.Surface((self.length + (i * 2), self.height + (i * 2)))
            s.fill(self.color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(
                s, self.color, (self.x - i, self.y - i, self.length + i, self.height + i), self.width)
            self.surface.blit(s, (self.x - i, self.y - i))
        pygame.draw.rect(self.surface, self.color,
                         (self.x, self.y, self.length, self.height), 0)
        pygame.draw.rect(self.surface, (190, 190, 190),
                         (self.x, self.y, self.length, self.height), 1)
        # Render text
        my_text = self.my_font.render(self.text, 1, self.text_color)
        self.surface.blit(my_text, ((self.x + self.length / 2) - my_text.get_width() /
                                    2, (self.y + self.height / 2) - my_text.get_height() / 2))
