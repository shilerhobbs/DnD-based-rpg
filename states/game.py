"""
The class for our Game scene is found here.
"""

import pygame as pg

import prepare, tools, sprites


class Game(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        # self.start_time = 0.0
        # self.current_time = 0.0
        self.done = False
        # self.quit = False
        self.next = "WORLD"
        # self.previous = None
        # self.persist = {}


    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        self.persist = persistant
        self.start_time = current_time
        self.player = sprites.Player()

    def cleanup(self):
        """Stop the music when scene is done."""
        return tools._State.cleanup(self)


    def get_event(self, event):
        """Go back to intro on escape key."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True

    def draw(self, surface):
        """Blit all elements to surface."""
        surface.blit(self.player.frames,0,0)


    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.draw(surface)