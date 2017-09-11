import pygame as pg
from os import path

import prepare, tools, sprites, tilemap

vec = pg.math.Vector2

class World(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        # self.start_time = 0.0
        # self.current_time = 0.0
        self.done = False
        self.quit = False
        # self.next = None
        # self.previous = None
        # self.persist = {}
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.event = pg.sprite.Group()
        self.encounter = pg.sprite.Group()
        self.player = sprites.Player(self,0,0)

    def make_map(self):
        self.map = tilemap.TiledMap(prepare.play_map)
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        #self.map_img_forgound.rect = self.map_img_forgound.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':

                self.player = sprites.Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                sprites.Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

            if tile_object.name == 'event':
                sprites.Event(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,
                      tile_object.properties['destination'])

            if tile_object.name == 'encounter':
                sprites.Encounter(self, tile_object.x, tile_object.y,
                      tile_object.width, tile_object.height,
                      tile_object.properties['location'])


        self.camera = tilemap.Camera(self.map.width, self.map.height)

    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""

        self.persist = persistant
        self.start_time = current_time
        self.make_map()

    def cleanup(self):
        """Stop the music when scene is done."""
        return tools._State.cleanup(self)


    def get_event(self, event):
        """Go back to intro on escape key."""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
        if event.type == pg.KEYUP:
            pass



    def draw(self, surface):
        """Blit all elements to surface."""
        surface.blit(self.map_img, self.camera.apply(self.map))

        for sprite in self.all_sprites:
            surface.blit(sprite.image, self.camera.apply(sprite))
            #if self.draw_debug:
                #pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)


    def update(self, surface, keys, current_time):
        """Update function for state.  Must be overloaded in children."""
        if self.player.map_change:
            self.make_map()
        self.draw(surface)

