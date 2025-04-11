import pygame as pg

class TypingText:
    def __init__(self, text, font, size, speed, max_width):
        self.text = text
        self.font = pg.font.SysFont(font, size, bold=True)
        self.speed = speed
        self.max_width = max_width
        self.index = 0
        self.current_text = ""
        self.lines = []
        self.last_update = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if self.index < len(self.text) and now - self.last_update > 1000 / self.speed:
            self.current_text += self.text[self.index]
            self.index += 1
            self.last_update = now
            self._wrap_text()

    def _wrap_text(self):
        words = self.current_text.split(' ')
        self.lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] > self.max_width:
                self.lines.append(line.strip())
                line = word + " "
            else:
                line = test_line
        self.lines.append(line.strip())  # adiciona última linha

    def draw(self, screen, pos=(0, 0), color=(255, 255, 255), line_spacing=5):
        x, y = pos
        for line in self.lines:
            rendered = self.font.render(line, True, color)
            screen.blit(rendered, (x, y))
            y += self.font.get_height() + line_spacing

    def isFinished(self):
        return self.index >= len(self.text)
