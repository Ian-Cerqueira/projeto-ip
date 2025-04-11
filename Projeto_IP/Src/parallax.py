import pygame as pg

class ParallaxVertical:
    def __init__(self, image, speed, width, height):
        self.image = pg.transform.scale(image, (width, height))
        self.maxHeight = height
        self.speed = speed
        self.pos_up = [0, -height]
        self.pos_down = [0, 0]
        
        
    def draw(self, screen):
        screen.blit(self.image, self.pos_down)
        screen.blit(self.image, self.pos_up)
    
    def move(self):
        self.pos_up[1] += self.speed
        self.pos_down[1] += self.speed
        
        if(self.pos_up[1] > self.maxHeight):
            self.pos_up[1] = -self.maxHeight
        if(self.pos_down[1] > self.maxHeight):
            self.pos_down[1] = -self.maxHeight
    
    def update(self, screen):
        self.draw(screen)
        self.move()
        
    
