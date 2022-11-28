import pygame
from pygame import Vector2

class BACKGROUND:
    def __init__(self, display_surface, bgimage, pos=Vector2(0,0)) -> None:
        self.image = bgimage
        self.surface = display_surface
        self.height = self.surface.get_height()
        self.width = self.surface.get_width()
        self.pos = pos

        self.buffers = []

        self.buffers.append(Vector2(self.pos.x - self.width, self.pos.y))
        self.buffers.append(Vector2(self.pos.x + self.width, self.pos.y))
    
    def set_mode(self, mode):
        self.buffers = []
        if mode == 1:
            self.buffers.append(Vector2(self.pos.x - self.width, self.pos.y))
            self.buffers.append(Vector2(self.pos.x + self.width, self.pos.y))
        elif mode == 2:
            self.buffers.append(Vector2(self.pos.x, self.pos.y - self.height))
            self.buffers.append(Vector2(self.pos.x, self.pos.y + self.height))
        elif mode == 3:
            self.buffers.append(Vector2(self.pos.x - self.width, self.pos.y))
            self.buffers.append(Vector2(self.pos.x + self.width, self.pos.y))
            self.buffers.append(Vector2(self.pos.x, self.pos.y - self.height))
            self.buffers.append(Vector2(self.pos.x, self.pos.y + self.height))

            self.buffers.append(Vector2(self.pos.x - self.width, self.pos.y - self.height))
            self.buffers.append(Vector2(self.pos.x - self.width, self.pos.y + self.height))
            self.buffers.append(Vector2(self.pos.x + self.width, self.pos.y - self.height))
            self.buffers.append(Vector2(self.pos.x + self.width, self.pos.y + self.height))
    
    def move(self, pos):
        self.pos += pos
        for buffer in self.buffers:
            buffer += pos

    def move_x(self, pos):
        self.move(Vector2(pos, 0))
    
    def move_y(self, pos):
        self.move(Vector2(0, pos))

    def update(self):
        '''
        This repositions the background and buffers when they move out the screen.
        '''
        if self.pos.x > self.width:
            self.pos.x -= self.width
            for buffer in self.buffers:
                buffer.x -= self.width
        if self.pos.x < -self.width:
            self.pos.x += self.width
            for buffer in self.buffers:
                buffer.x += self.width
        if self.pos.y > self.height:
            self.pos.y -= self.height
            for buffer in self.buffers:
                buffer.y -= self.height
        if self.pos.y < -self.height:
            self.pos.y += self.height
            for buffer in self.buffers:
                buffer.y += self.height

    def draw(self):
        self.surface.blit(self.image, self.pos)

        for buffer in self.buffers:
            self.surface.blit(self.image, buffer)
