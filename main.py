import pygame
import sys
import data
import pickle
import Tkinter
from random import randint


def get_tile(image, coords):
    tile_size = (32, 32)
    rect = pygame.rect.Rect(coords[0] * tile_size[0], coords[1] * tile_size[1], tile_size[0], tile_size[1])
    return image.subsurface(rect)


class DropMenu(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, screen, groups, owner=False):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.groups = groups

        self.pos = pos
        self.size = size
        self.name = name

        self.opened = False
        self.owner = owner

        self.dep = []

        self.rect = pygame.rect.Rect(0, 0, 0, 0)
        self.add(self.groups['drmitems'])

    def update(self):
        if not self.owner:
            self.rect = (self.pos[0], self.pos[1], self.size[0], self.size[1])
            if self.opened:
                if self.dep:
                    for dep in self.dep:
                        dep.rect = pygame.rect.Rect(dep.pos[0], dep.pos[1], dep.size[0], dep.size[1])
            else:
                if self.dep:
                    for dep in self.dep:
                        dep.rect = pygame.rect.Rect(0, 0, 0, 0)

    def render(self):
        if not self.owner:
            pygame.draw.rect(self.screen, (60, 60, 60), self.rect)
            self.screen.blit(data.textfont.render(self.name, True, (255, 255, 255)), (self.pos[0] + 1, self.pos[1]))
            if self.opened:
                if self.dep:
                    for dep in self.dep:
                        pygame.draw.rect(self.screen, (30, 30, 30),
                                         (dep.pos[0] - 1, dep.pos[1] - 1, dep.size[0] + 2, dep.size[1] + 2))
                        pygame.draw.rect(self.screen, (60, 60, 60), dep.rect)
                        # pygame.draw.rect(self.screen, (60,60,60),(dep.pos[0],dep.pos[1],dep.size[0],dep.size[1])
                        self.screen.blit(data.textfont.render(dep.name, True, (255, 255, 255)),
                                         (dep.pos[0] + 1, dep.pos[1]))


class Menu:
    def __init__(self, screen, groups, menu_dict):
        self.screen = screen
        self.groups = groups
        self.menu_dict = menu_dict

        self.menu = []
        self.size = (145, 15)

        for name in self.menu_dict:
            # print name
            self.menu.append(
                DropMenu(name[0], (len(self.menu) * self.size[0] + 2 * len(self.menu) + 2, 2), self.size, self.screen,
                         self.groups))
            if type(name[1]) == type([]):
                for drop_name in name[1]:
                    self.menu[-1].dep.append(
                        DropMenu(
                            drop_name,
                            (
                                self.menu[-1].pos[0],
                                len(self.menu[-1].dep) * self.size[1] + 4 + 2 * len(self.menu[-1].dep) + self.size[1]
                            ),
                            self.size,
                            self.screen,
                            self.groups
                        )
                    )

    def update(self):
        for item in self.menu:
            item.update()

    def render(self):
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, data.screensize[0], 19))
        for item in self.menu:
            item.render()


class TextField:
    def __init__(self, title, screen):
        pygame.font.init()
        self.title = title
        self.screen = screen
        self.result = ''
        self.show_cursor = True
        self.show_pick = 50
        self.show_mom = 0
        self.writing = True
        self.keys = {'LALT': False,
                     'RALT': False,
                     'ENTER': False,
                     'shift': False,
                     'ctrl': False}
        self.loop()

    def input_lib(self, key):

        # print 'Target'
        if key == pygame.K_SPACE:
            self.result += ' '
        if key == pygame.K_0:
            if self.keys['shift']:
                self.result += ')'
            else:
                self.result += '0'
        if key == pygame.K_1:
            if self.keys['shift']:
                self.result += '!'
            else:
                self.result += '1'
        if key == pygame.K_2:
            if self.keys['shift']:
                self.result += '@'
            else:
                self.result += '2'
        if key == pygame.K_3:
            if self.keys['shift']:
                self.result += '#'
            else:
                self.result += '3'
        if key == pygame.K_4:
            if self.keys['shift']:
                self.result += '$'
            else:
                self.result += '4'
        if key == pygame.K_5:
            if self.keys['shift']:
                self.result += '%'
            else:
                self.result += '5'
        if key == pygame.K_6:
            if self.keys['shift']:
                self.result += '^'
            else:
                self.result += '6'
        if key == pygame.K_7:
            if self.keys['shift']:
                self.result += '&'
            else:
                self.result += '7'
        if key == pygame.K_8:
            if self.keys['shift']:
                self.result += '*'
            else:
                self.result += '8'
        if key == pygame.K_9:
            if self.keys['shift']:
                self.result += '('
            else:
                self.result += '9'
        # Letters
        if key == pygame.K_q:
            if self.keys['shift']:
                self.result += 'Q'
            else:
                self.result += 'q'
        if key == pygame.K_w:
            if self.keys['shift']:
                self.result += 'W'
            else:
                self.result += 'w'
        if key == pygame.K_e:
            if self.keys['shift']:
                self.result += 'E'
            else:
                self.result += 'e'
        if key == pygame.K_r:
            if self.keys['shift']:
                self.result += 'R'
            else:
                self.result += 'r'
        if key == pygame.K_t:
            if self.keys['shift']:
                self.result += 'T'
            else:
                self.result += 't'
        if key == pygame.K_y:
            if self.keys['shift']:
                self.result += 'Y'
            else:
                self.result += 'y'
        if key == pygame.K_u:
            if self.keys['shift']:
                self.result += 'U'
            else:
                self.result += 'u'
        if key == pygame.K_i:
            if self.keys['shift']:
                self.result += 'I'
            else:
                self.result += 'i'
        if key == pygame.K_o:
            if self.keys['shift']:
                self.result += 'O'
            else:
                self.result += 'o'
        if key == pygame.K_p:
            if self.keys['shift']:
                self.result += 'P'
            else:
                self.result += 'p'
        if key == pygame.K_LEFTBRACKET:
            if self.keys['shift']:
                self.result += '{'
            else:
                self.result += '['
        if key == pygame.K_RIGHTBRACKET:
            if self.keys['shift']:
                self.result += '}'
            else:
                self.result += ']'
        if key == pygame.K_a:
            if self.keys['shift']:
                self.result += 'A'
            else:
                self.result += 'a'
        if key == pygame.K_s:
            if self.keys['shift']:
                self.result += 'S'
            else:
                self.result += 's'
        if key == pygame.K_d:
            if self.keys['shift']:
                self.result += 'D'
            else:
                self.result += 'd'
        if key == pygame.K_f:
            if self.keys['shift']:
                self.result += 'F'
            else:
                self.result += 'f'
        if key == pygame.K_g:
            if self.keys['shift']:
                self.result += 'G'
            else:
                self.result += 'g'
        if key == pygame.K_h:
            if self.keys['shift']:
                self.result += 'H'
            else:
                self.result += 'h'
        if key == pygame.K_j:
            if self.keys['shift']:
                self.result += 'J'
            else:
                self.result += 'j'
        if key == pygame.K_k:
            if self.keys['shift']:
                self.result += 'K'
            else:
                self.result += 'k'
        if key == pygame.K_l:
            if self.keys['shift']:
                self.result += 'L'
            else:
                self.result += 'l'
        if key == pygame.K_SEMICOLON:
            if self.keys['shift']:
                self.result += ':'
            else:
                self.result += ';'
        if key == pygame.K_BACKQUOTE:
            if self.keys['shift']:
                self.result += '"'
            else:
                self.result += '\''
        if key == pygame.K_BACKSLASH:
            if self.keys['shift']:
                self.result += '|'
            else:
                self.result += '\\'
        if key == pygame.K_z:
            if self.keys['shift']:
                self.result += 'Z'
            else:
                self.result += 'z'
        if key == pygame.K_x:
            if self.keys['shift']:
                self.result += 'X'
            else:
                self.result += 'x'
        if key == pygame.K_c:
            if self.keys['shift']:
                self.result += 'C'
            else:
                self.result += 'c'
        if key == pygame.K_v:
            if self.keys['shift']:
                self.result += 'V'
            else:
                self.result += 'v'
        if key == pygame.K_b:
            if self.keys['shift']:
                self.result += 'B'
            else:
                self.result += 'b'
        if key == pygame.K_n:
            if self.keys['shift']:
                self.result += 'N'
            else:
                self.result += 'n'
        if key == pygame.K_m:
            if self.keys['shift']:
                self.result += 'M'
            else:
                self.result += 'm'
        if key == pygame.K_COMMA:
            if self.keys['shift']:
                self.result += '<'
            else:
                self.result += ','
        if key == pygame.K_PERIOD:
            if self.keys['shift']:
                self.result += '>'
            else:
                self.result += '.'
        if key == pygame.K_SLASH:
            if self.keys['shift']:
                self.result += '?'
            else:
                self.result += '/'
        if key == pygame.K_KP0:
            self.result += '0'
        if key == pygame.K_KP1:
            self.result += '1'
        if key == pygame.K_KP2:
            self.result += '2'
        if key == pygame.K_KP3:
            self.result += '3'
        if key == pygame.K_KP4:
            self.result += '4'
        if key == pygame.K_KP5:
            self.result += '5'
        if key == pygame.K_KP6:
            self.result += '6'
        if key == pygame.K_KP7:
            self.result += '7'
        if key == pygame.K_KP8:
            self.result += '8'
        if key == pygame.K_KP9:
            self.result += '9'
        if key == pygame.K_BACKSPACE:
            self.result = self.result[0:-1]

    def handle_keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT:
                self.keys['LALT'] = True
            if event.key == pygame.K_RALT:
                self.keys['RALT'] = True
            if event.key == pygame.K_RETURN:
                self.keys['ENTER'] = True
            if event.key == pygame.K_LCTRL:
                self.keys['ctrl'] = True
            if event.key == pygame.K_LSHIFT:
                self.keys['shift'] = True
            if event.key == pygame.K_RETURN and self.result != '':
                self.writing = False
            self.input_lib(event.key)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LALT:
                self.keys['LALT'] = False
            if event.key == pygame.K_RALT:
                self.keys['RALT'] = False
            if event.key == pygame.K_RETURN:
                self.keys['ENTER'] = False
            if event.key == pygame.K_LCTRL:
                self.keys['ctrl'] = False
            if event.key == pygame.K_LSHIFT:
                self.keys['shift'] = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handle_keyboard(event)
            if event.type == pygame.VIDEORESIZE:
                data.screensize = event.size
                self.screen = pygame.display.set_mode(data.screensize, pygame.RESIZABLE)

    def render(self):
        pygame.draw.rect(self.screen, (50, 0, 0), (10, 10, data.screensize[0] - 20, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, data.screensize[0] - 20, 50), 2)
        pygame.draw.rect(self.screen, (10, 10, 10), (10, 70, data.screensize[0] - 20, 50))
        self.screen.blit(data.edittext.render(self.title, True, (255, 255, 255)), (17, 17))
        if self.show_cursor:
            self.screen.blit(data.edittext.render(self.result + '|', True, (255, 255, 255)), (17, 77))
        else:
            self.screen.blit(data.edittext.render(self.result, True, (255, 255, 255)), (17, 77))
        pygame.display.flip()

    def update(self):
        if (self.keys['LALT'] and self.keys['ENTER']) or (self.keys['RALT'] and self.keys['ENTER']):
            if data.fullscreen:
                data.screensize = (800, 600)
                self.screen = pygame.display.set_mode(data.screensize, pygame.RESIZABLE)
                data.fullscreen = False
            else:
                data.screensize = (Tkinter.Tk().winfo_screenwidth(), Tkinter.Tk().winfo_screenheight())
                self.screen = pygame.display.set_mode(data.screensize, pygame.FULLSCREEN)
                data.fullscreen = True
        self.show_mom += 1
        if self.show_mom >= self.show_pick:
            self.show_cursor = not self.show_cursor
            self.show_mom = 0

    def loop(self):
        tick_clock = pygame.time.Clock()
        while self.writing:
            tick_clock.tick(60)
            pygame.display.set_caption(data.title + ' <Typing mode> FPS:' + str(int(tick_clock.get_fps())))
            self.handle_events()
            self.update()
            self.render()


class Cursor(pygame.sprite.Sprite):
    def __init__(self, screen, groups):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.last_pos = [0, 0]
        self.type = 0
        self.groups = groups
        self.screen = screen
        self.start = None
        self.finish = None
        self.chance = None
        self.brush = 0
        self.selected = False
        self.collidable = False
        self.editable = False
        self.layer = 0
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 2, 2)
        self.add(self.groups['cursor'])

    def update(self):
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 2, 2)
        if pygame.sprite.spritecollide(self, self.groups['drmitems'], False):
            self.editable = False
        else:
            self.editable = True

    def render(self):
        # self.screen.blit(pygame.font.SysFont('Terminal',15).render('Layer:'+str(self.layer+1),True,(150,0,255)),(data.screensize[0]-80,data.screensize[1]-10))
        self.screen.blit(data.cursorfont.render('Layer:' + str(self.layer + 1), True, (255, 255, 255)),
                         (self.pos[0] + 2, self.pos[1] + 35))
        if self.selected:
            self.screen.blit(self.selected.image, (self.pos[0] + 2, self.pos[1] + 2))
        if self.collidable:
            self.screen.blit(data.cursorfont.render('Collidable', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 50))
        else:
            self.screen.blit(data.cursorfont.render('UnCollidable', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 50))
        if self.brush == 0:
            self.screen.blit(data.cursorfont.render('Brush: normal', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 65))
        if self.brush == 1:
            self.screen.blit(data.cursorfont.render('Brush: Fill', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 65))
        if self.brush == 2:
            self.screen.blit(data.cursorfont.render('Brush: Substitute', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 65))
        if self.brush == 3:
            self.screen.blit(data.cursorfont.render('Brush: Rectangle', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 65))
        if self.brush == 4:
            self.screen.blit(data.cursorfont.render('Brush: Noise fill', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 65))
        if self.brush == 5:
            self.screen.blit(data.cursorfont.render('Brush: Take tile from map', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 65))
        if self.type == 0:
            self.screen.blit(data.cursorfont.render('Type: Tiles', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 80))
        if self.type == 1:
            self.screen.blit(data.cursorfont.render('Type: Player', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 80))
        if self.type == 2:
            self.screen.blit(data.cursorfont.render('Type: Mobs', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 80))
        if self.type == 3:
            self.screen.blit(data.cursorfont.render('Type: Exits', True, (255, 255, 255)),
                             (self.pos[0] + 2, self.pos[1] + 80))

    def left_click(self):
        if self.pos[1] > 19:
            if pygame.sprite.spritecollide(self, self.groups['menutiles'], False):
                self.selected = pygame.sprite.spritecollide(self, self.groups['menutiles'], False)[0]
        if pygame.sprite.spritecollide(self, self.groups['drmitems'], False):
            pygame.sprite.spritecollide(self, self.groups['drmitems'], False)[0].opened = not \
                pygame.sprite.spritecollide(self, self.groups['drmitems'], False)[0].opened


class Tile(pygame.sprite.Sprite):
    def __init__(self, screen, image, coordinates, groups, collide):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0, 0]
        self.image = image
        self.screen = screen
        self.coordinates = coordinates
        self.groups = groups
        self.collide = collide
        if collide:
            self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 32, 32)
            self.add(self.groups['menutiles'])

    def render(self, pos):
        self.pos = pos
        if self.collide:
            self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 32, 32)
        self.screen.blit(self.image, (self.pos[0], self.pos[1]))


class TileSet:
    def __init__(self, image):
        image_size = image.get_size()
        self.image = image
        self.tileset = []
        for iy in range(0, image_size[1] / 32):
            self.tileset.append([])
            for ix in range(0, image_size[0] / 32):
                self.tileset[iy].append(get_tile(image, (ix, iy)))

    def get_tile(self, coordinates):
        return self.tileset[coordinates[1]][coordinates[0]]


class Map:
    def __init__(self, screen, size):
        self.screen = screen

        self.map = [[], [], [], [], []]
        self.collide_list = []
        self.mobs_spawn = []
        self.player_spawn = [0, 0]
        self.ways = []
        self.ways = [[], [], [], [], []]

        self.draw_collide = True
        self.pos = [96, 19]
        self.size = size
        self.draw_up_grid = False
        self.showSubTriggers = True
        self.layer_show = [True, True, True, True, True]
        self.tileset = TileSet(data.tileset)
        self.map_surface = pygame.surface.Surface((size[0] * 32, size[1] * 32))
        self.grid_surface = pygame.surface.Surface((size[0] * 32, size[1] * 32))

        for iy in xrange(size[1]):
            pygame.draw.aaline(self.grid_surface, (180, 180, 180), (0, iy * 32), (size[0] * 32, iy * 32))
        for ix in xrange(size[0]):
            pygame.draw.aaline(self.grid_surface, (180, 180, 180), (ix * 32, 0), (ix * 32, size[1] * 32))

        for map_layer_index in xrange(len(self.map)):
            for iy in xrange(size[1]):
                self.map[map_layer_index].append([])
                for ix in xrange(size[0]):
                    self.map[map_layer_index][iy].append((-1, -1))
        self.get_surface()

    def clear(self, layer, tile_coordinates):
        for iy in range(0, len(self.map[layer])):
            for ix in range(0, len(self.map[layer][iy])):
                self.map[layer][iy][ix] = (-1, -1)

    def fill(self, layer, tile_coordinates, cursor_pos):
        for iy in range(0, len(self.map[layer])):
            for ix in range(0, len(self.map[layer][iy])):
                self.map[layer][iy][ix] = tile_coordinates

    def subs(self, layer, tile_coordinates, target):
        change_place = self.map[layer][tile_coordinates[1]][tile_coordinates[0]]
        if change_place != (-1, -1):
            for iy in range(0, len(self.map[layer])):
                for ix in range(0, len(self.map[layer][iy])):
                    if self.map[layer][iy][ix] == change_place:
                        self.map[layer][iy][ix] = target

    def noise_fill(self, layer, target, chance):
        for iy in range(0, len(self.map[layer])):
            for ix in range(0, len(self.map[layer][iy])):
                if randint(0, 100) < chance:
                    self.map[layer][iy][ix] = target

    def new(self, screen, size):
        self.screen = screen
        self.map = [[], [], [], []]
        self.collide_list = []
        self.draw_collide = True
        self.pos = [96, 19]
        self.size = size
        self.tileset = TileSet(data.tileset)
        self.map_surface = pygame.surface.Surface((size[0] * 32, size[1] * 32))
        self.grid_surface = pygame.surface.Surface((size[0] * 32, size[1] * 32))

        for iy in range(0, size[1]):
            pygame.draw.aaline(self.grid_surface, (180, 180, 180), (0, iy * 32), (size[0] * 32, iy * 32))
        for ix in range(0, size[0]):
            pygame.draw.aaline(self.grid_surface, (180, 180, 180), (ix * 32, 0), (ix * 32, size[1] * 32))

        for map in range(0, len(self.map)):
            for iy in range(0, size[1]):
                self.map[map].append([])
                for ix in range(0, size[0]):
                    self.map[map][iy].append((-1, -1))
        self.get_surface()

    def save(self, filename):
        fl = open(filename, 'wb')
        pickle.dump(self.map, fl, -1)
        pickle.dump(self.collide_list, fl, -1)
        pickle.dump(self.mobs_spawn, fl, -1)
        pickle.dump(self.player_spawn, fl, -1)
        pickle.dump(self.ways, fl, -1)
        fl.close()

    def load(self, filename):
        try:
            fl = open(filename, 'rb')
        except IOError:
            return False
        self.map = pickle.load(fl)
        self.collide_list = pickle.load(fl)
        self.mobs_spawn = pickle.load(fl)
        self.player_spawn = pickle.load(fl)
        self.ways = pickle.load(fl)
        if len(self.ways) != 5:
            self.ways = [[], [], [], [], []]
        self.size = (len(self.map[0][0]), len(self.map[0]))

        fl.close()

        self.map_surface = pygame.surface.Surface((self.size[0] * 32, self.size[1] * 32))
        self.grid_surface = pygame.surface.Surface((self.size[0] * 32, self.size[1] * 32))

        for iy in range(0, self.size[1]):
            pygame.draw.aaline(self.grid_surface, (180, 180, 180), (0, iy * 32), (self.size[0] * 32, iy * 32))
        for ix in range(0, self.size[0]):
            pygame.draw.aaline(self.grid_surface, (180, 180, 180), (ix * 32, 0), (ix * 32, self.size[1] * 32))
        self.get_surface()

        return True

    def set_map(self, coords, layer, set):
        self.map[layer][coords[1]][coords[0]] = set

    def get_surface(self):
        self.map_surface.blit(self.grid_surface, (0, 0))
        for map in range(0, len(self.map) - 1):
            if self.layer_show[map]:
                for iy in range(0, len(self.map[map])):
                    for ix in range(0, len(self.map[map][iy])):
                        if self.map[map][iy][ix] != (-1, -1):
                            self.map_surface.blit(self.tileset.get_tile((self.map[map][iy][ix])), (ix * 32, iy * 32))
        if self.showSubTriggers:
            self.map_surface.blit(data.player, (self.player_spawn[0] * 32, self.player_spawn[1] * 32))
            for mob in self.mobs_spawn:
                self.map_surface.blit(data.mobs, (mob[0] * 32, mob[1] * 32))
            for layer in range(0, len(self.ways)):
                for way in self.ways[layer]:
                    self.map_surface.blit(data.ways, (way[0] * 32, way[1] * 32))
                    self.map_surface.blit(data.textfont.render(str(layer + 1), True, (255, 255, 255)),
                                         (way[0] * 32, way[1] * 32))

        if self.layer_show[-1]:
            for iy in range(0, len(self.map[-1])):
                for ix in range(0, len(self.map[-1][iy])):
                    if self.map[-1][iy][ix] != (-1, -1):
                        self.map_surface.blit(self.tileset.get_tile((self.map[-1][iy][ix])), (ix * 32, iy * 32))

        if self.draw_up_grid:
            for iy in range(0, self.size[1]):
                pygame.draw.aaline(self.map_surface, (180, 180, 180), (0, iy * 32), (self.size[0] * 32, iy * 32))
            for ix in range(0, self.size[0]):
                pygame.draw.aaline(self.map_surface, (180, 180, 180), (ix * 32, 0), (ix * 32, self.size[1] * 32))
        if self.draw_collide:
            for collide in self.collide_list:
                pygame.draw.rect(self.map_surface, (150, 0, 5), (collide[0] * 32, collide[1] * 32, 32, 32), 3)

    def render(self):
        self.screen.blit(self.map_surface, (self.pos[0], self.pos[1]))


class TileMenu:
    def __init__(self, screen, groups):
        self.groups = groups
        self.screen = screen
        self.tileset = TileSet(data.tileset)
        self.tiles = []
        self.scroll = 0

        for iy in range(0, len(self.tileset.tileset)):
            for ix in range(0, len(self.tileset.tileset[iy])):
                self.tiles.append(Tile(self.screen, self.tileset.get_tile((ix, iy)), (ix, iy), self.groups, True))

    def render(self):
        pygame.draw.rect(self.screen, (150, 150, 150), (0, 0, 96, data.screensize[1]))
        pos = [-32, 19]
        for tile in self.tiles:
            if pos[0] >= 64:
                pos[0] = 0
                pos[1] += 32
            else:
                pos[0] += 32
            # print pos
            tile.render((pos[0], pos[1] + self.scroll))


class Scene:
    @staticmethod
    def load_tiles(filename):
        try:
            data.tileset = pygame.image.load(filename)
        except pygame.error:
            return False
        return True

    def __init__(self):
        pygame.init()
        if data.fullscreen:
            data.screensize = (Tkinter.Tk().winfo_screenwidth(), Tkinter.Tk().winfo_screenheight())
            self.screen = pygame.display.set_mode(data.screensize, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(data.screensize, pygame.RESIZABLE)
        pygame.display.set_caption(data.title)
        loading = True
        while loading:
            if self.load_tiles(TextField('Enter tileset filename', self.screen).result):
                loading = False
        self.keys = {  # Mouse
                       'middle': False,
                       # Keyboard
                       's': False,
                       'ctrl': False,
                       'lshift': False,
                       'rshift': False,
                       'l': False,
                       'UP': False,
                       'DOWN': False,
                       'LEFT': False,
                       'RIGHT': False,
                       'LALT': False,
                       'RALT': False,
                       'ENTER': False,
                       }
        # init editor
        self.groups = {
            'menutiles': pygame.sprite.Group(),
            'cursor': pygame.sprite.Group(),
            'drmitems': pygame.sprite.Group(),
        }

        self.map = Map(
            self.screen,
            (
                int(TextField('Input X size', self.screen).result),
                int(TextField('Input Y size', self.screen).result)
            )
        )
        self.cursor = Cursor(self.screen, self.groups)
        self.tile_menu = TileMenu(self.screen, self.groups)
        self.menu = Menu(self.screen, self.groups, (('File', ['New (ctrl+n)',
                                                              'Save (ctrl+s)',
                                                              'Load (ctrl+l)',
                                                              'Exit']),
                                                    ('View', ['View collide  (tab)',
                                                              'Go to tile',
                                                              'Show/Un show layer 1',
                                                              'Show/Un show layer 2',
                                                              'Show/Un show layer 3',
                                                              'Show/Un show layer 4',
                                                              'Show/Un show layer 5',
                                                              'Show/Un show grid',
                                                              'Show/Un show triggers',
                                                              'Toggle fullscreen']),
                                                    ('Editor', ['Draw 1 layer (1)',
                                                                'Draw 2 layer (2)',
                                                                'Draw 3 layer (3)',
                                                                'Draw 4 layer (4)',
                                                                'Draw 5 layer (5)',
                                                                'Draw collide (c)']),
                                                    ('Brush', ['Normal',
                                                               'Fill',
                                                               'Substitute',
                                                               'Rectangle',
                                                               'Noise fill',
                                                               'Take tile']),
                                                    ('Brush type', ['Tiles',
                                                                    'Player',
                                                                    'Mobs',
                                                                    'Ways'])))

        self.gameloop()

    def gui(self):
        if not self.map.draw_collide:
            self.screen.blit(data.cursorfont.render('Collide area don\'t shown.', True, (255, 255, 255)),
                             (data.screensize[0] - 160, 18))
        else:
            self.screen.blit(data.cursorfont.render('Collide area are shown.', True, (255, 255, 255)),
                             (data.screensize[0] - 160, 18))

    def render(self):
        self.screen.fill((0, 0, 0))

        self.map.render()
        self.tile_menu.render()
        self.menu.render()
        self.gui()
        self.cursor.render()

        pygame.display.flip()

    def update(self):
        # Menu set
        if self.menu.menu[0].dep[0].opened:
            self.menu.menu[0].dep[0].opened = False
            self.map.new(
                self.screen,
                (
                    int(TextField('Input X size', self.screen).result),
                    int(TextField('Input Y size', self.screen).result)
                )
            )

        if self.menu.menu[0].dep[1].opened:
            self.menu.menu[0].dep[1].opened = False
            filename = TextField('SAVE Enter filename', self.screen).result
            isd = False
            for letter in filename:
                if letter == '.':
                    isd = True
                    break
            if not isd:
                filename += '.mp'
            self.map.save(filename)

        if self.menu.menu[0].dep[2].opened:
            self.menu.menu[0].dep[2].opened = False
            loading = True
            while loading:
                filename = TextField('LOAD Enter filename', self.screen).result
                isd = False
                for letter in filename:
                    if letter == '.':
                        isd = True
                        break
                if not isd:
                    filename += '.mp'
                if self.map.load(filename):
                    loading = False
        if self.menu.menu[0].dep[3].opened:
            self.menu.menu[0].dep[3].opened = False
            pygame.quit()
            sys.exit()

        if self.menu.menu[1].dep[0].opened:
            self.menu.menu[1].dep[0].opened = False
            self.map.draw_collide = not self.map.draw_collide
            self.map.get_surface()

        if self.menu.menu[1].dep[1].opened:
            self.menu.menu[1].dep[1].opened = False
            self.map.pos = [0 - int(TextField('Enter X pos', self.screen).result) * 32 + 96,
                            0 - int(TextField('Enter Y pos', self.screen).result) * 32 + 19]

        if self.menu.menu[1].dep[2].opened:
            self.menu.menu[1].dep[2].opened = False
            self.map.layer_show[0] = not self.map.layer_show[0]
            self.map.get_surface()

        if self.menu.menu[1].dep[3].opened:
            self.menu.menu[1].dep[3].opened = False
            self.map.layer_show[1] = not self.map.layer_show[1]
            self.map.get_surface()

        if self.menu.menu[1].dep[4].opened:
            self.menu.menu[1].dep[4].opened = False
            self.map.layer_show[2] = not self.map.layer_show[2]
            self.map.get_surface()

        if self.menu.menu[1].dep[5].opened:
            self.menu.menu[1].dep[5].opened = False
            self.map.layer_show[3] = not self.map.layer_show[3]
            self.map.get_surface()

        if self.menu.menu[1].dep[6].opened:
            self.menu.menu[1].dep[6].opened = False
            self.map.layer_show[4] = not self.map.layer_show[4]
            self.map.get_surface()

        if self.menu.menu[1].dep[7].opened:
            self.menu.menu[1].dep[7].opened = False
            self.map.draw_up_grid = not self.map.draw_up_grid
            self.map.get_surface()

        if self.menu.menu[1].dep[8].opened:
            self.menu.menu[1].dep[8].opened = False
            self.map.showSubTriggers = not self.map.showSubTriggers
            self.map.get_surface()

        if self.menu.menu[1].dep[9].opened:
            self.menu.menu[1].dep[9].opened = False
            if data.fullscreen:
                data.screensize = (800, 600)
                self.screen = pygame.display.set_mode(data.screensize, pygame.RESIZABLE)
                data.fullscreen = False
            else:
                data.screensize = (Tkinter.Tk().winfo_screenwidth(), Tkinter.Tk().winfo_screenheight())
                self.screen = pygame.display.set_mode(data.screensize, pygame.FULLSCREEN)
                data.fullscreen = True

        if self.menu.menu[2].dep[0].opened:
            self.menu.menu[2].dep[0].opened = False
            self.cursor.layer = 0

        if self.menu.menu[2].dep[1].opened:
            self.menu.menu[2].dep[1].opened = False
            self.cursor.layer = 1

        if self.menu.menu[2].dep[2].opened:
            self.menu.menu[2].dep[2].opened = False
            self.cursor.layer = 2

        if self.menu.menu[2].dep[3].opened:
            self.menu.menu[2].dep[3].opened = False
            self.cursor.layer = 3

        if self.menu.menu[2].dep[4].opened:
            self.menu.menu[2].dep[4].opened = False
            self.cursor.layer = 4

        if self.menu.menu[2].dep[5].opened:
            self.menu.menu[2].dep[5].opened = False
            self.cursor.collidable = not self.cursor.collidable

        if self.menu.menu[3].dep[0].opened:
            self.menu.menu[3].dep[0].opened = False
            self.cursor.brush = 0

        if self.menu.menu[3].dep[1].opened:
            self.menu.menu[3].dep[1].opened = False
            self.cursor.brush = 1

        if self.menu.menu[3].dep[2].opened:
            self.menu.menu[3].dep[2].opened = False
            self.cursor.brush = 2

        if self.menu.menu[3].dep[3].opened:
            self.menu.menu[3].dep[3].opened = False
            self.cursor.brush = 3

        if self.menu.menu[3].dep[4].opened:
            self.menu.menu[3].dep[4].opened = False
            self.cursor.brush = 4
            self.cursor.chance = int(TextField('Enter percentage', self.screen).result)

        if self.menu.menu[3].dep[5].opened:
            self.menu.menu[3].dep[5].opened = False
            self.cursor.brush = 5

        if self.menu.menu[4].dep[0].opened:
            self.menu.menu[4].dep[0].opened = False
            self.cursor.type = 0

        if self.menu.menu[4].dep[1].opened:
            self.menu.menu[4].dep[1].opened = False
            self.cursor.type = 1

        if self.menu.menu[4].dep[2].opened:
            self.menu.menu[4].dep[2].opened = False
            self.cursor.type = 2

        if self.menu.menu[4].dep[3].opened:
            self.menu.menu[4].dep[3].opened = False
            self.cursor.type = 3
        # Stop
        if self.keys['s'] and self.keys['ctrl']:
            filename = TextField('SAVE Enter filename', self.screen).result
            isd = False
            for letter in filename:
                if letter == '.':
                    isd = True
                    break
            if not isd:
                filename += '.mp'
            self.map.save(filename)
            self.keys['s'] = False
            self.keys['ctrl'] = False
        if self.keys['l'] and self.keys['ctrl']:
            loading = True
            while loading:
                filename = TextField('LOAD Enter filename', self.screen).result
                isd = False
                for letter in filename:
                    if letter == '.':
                        isd = True
                        break
                if not isd:
                    filename += '.mp'
                if self.map.load(filename):
                    loading = False
            self.map.load(filename)
            self.keys['l'] = False
            self.keys['ctrl'] = False
        if self.keys['DOWN']:
            if self.keys['lshift'] or self.keys['rshift']:
                self.map.pos[1] -= 5
            else:
                self.map.pos[1] -= 2
        if self.keys['RIGHT']:
            if self.keys['lshift'] or self.keys['rshift']:
                self.map.pos[0] -= 5
            else:
                self.map.pos[0] -= 2
        if self.keys['UP']:
            if self.keys['lshift'] or self.keys['rshift']:
                self.map.pos[1] += 5
            else:
                self.map.pos[1] += 2
        if self.keys['LEFT']:
            if self.keys['lshift'] or self.keys['rshift']:
                self.map.pos[0] += 5
            else:
                self.map.pos[0] += 2

        if (self.keys['LALT'] and self.keys['ENTER']) or (self.keys['RALT'] and self.keys['ENTER']):
            if data.fullscreen:
                data.screensize = (800, 600)
                self.screen = pygame.display.set_mode(data.screensize, pygame.RESIZABLE)
                data.fullscreen = False
            else:
                data.screensize = (Tkinter.Tk().winfo_screenwidth(), Tkinter.Tk().winfo_screenheight())
                self.screen = pygame.display.set_mode(data.screensize, pygame.FULLSCREEN)
                data.fullscreen = True

        self.menu.update()
        self.cursor.update()

    def editor(self, event):
        if self.cursor.pos[0] > 96 and self.cursor.pos[1] > 19 and self.cursor.editable:
            if self.cursor.type == 0 and self.cursor.selected:
                if self.cursor.brush == 0:
                    fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                    if tile_coordinates[1] < self.map.size[1] and self.map.size[0] > tile_coordinates[0] > -1 and \
                                    tile_coordinates[1] > -1:
                        self.map.set_map(tile_coordinates, self.cursor.layer, self.cursor.selected.coordinates)
                        if self.cursor.collidable:
                            if not tile_coordinates in self.map.collide_list:
                                self.map.collide_list.append(tile_coordinates)
                        self.map.get_surface()
                if self.cursor.brush == 1:
                    fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                    self.map.fill(self.cursor.layer, self.cursor.selected.coordinates, tile_coordinates)
                    self.map.get_surface()
                if self.cursor.brush == 2:
                    fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                    self.map.subs(self.cursor.layer, tile_coordinates, self.cursor.selected.coordinates)
                    self.map.get_surface()
                if self.cursor.brush == 3:
                    fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                    if not self.cursor.start:
                        self.cursor.start = tile_coordinates
                    else:
                        self.cursor.finish = (tile_coordinates[0] + 1, tile_coordinates[1] + 1)
                        for iy in range(self.cursor.start[1], self.cursor.finish[1]):
                            for ix in range(self.cursor.start[0], self.cursor.finish[0]):
                                print self.cursor.start, self.cursor.finish, (ix, iy)
                                self.map.map[self.cursor.layer][iy][ix] = self.cursor.selected.coordinates
                        self.cursor.start = None
                        self.cursor.finish = None
                        self.map.get_surface()
                if self.cursor.brush == 4:
                    fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                    self.map.noise_fill(self.cursor.layer, self.cursor.selected.coordinates, self.cursor.chance)
                    self.map.get_surface()
                if self.cursor.brush == 5:
                    fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                    self.cursor.selected = Tile(self.screen, self.map.tileset.get_tile(
                        self.map.map[self.cursor.layer][tile_coordinates[1]][tile_coordinates[0]]),
                                                self.map.map[self.cursor.layer][tile_coordinates[1]][tile_coordinates[0]], None,
                                                False)

            if self.cursor.type == 1:
                fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                self.map.player_spawn = tile_coordinates
                self.map.get_surface()
            if self.cursor.type == 2:
                fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                if not tile_coordinates in self.map.mobs_spawn:
                    self.map.mobs_spawn.append(tile_coordinates)
                    self.map.get_surface()
            if self.cursor.type == 3:
                fact_position = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                tile_coordinates = [int(float(fact_position[0]) / 32.0), int(float(fact_position[1]) / 32.0)]
                if not tile_coordinates in self.map.ways[self.cursor.layer]:
                    self.map.ways[self.cursor.layer].append(tile_coordinates)
                    self.map.get_surface()

    def delete(self, event):
        if self.cursor.pos[0] > 96 and self.cursor.pos[1] > 19 and self.cursor.editable:
            if self.cursor.type == 0 and self.cursor.selected:
                if self.cursor.brush == 0:
                    factpos = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tilecoords = [int(float(factpos[0]) / 32.0), int(float(factpos[1]) / 32.0)]
                    if tilecoords[0] < self.map.size[0] and tilecoords[1] < self.map.size[1] and tilecoords[0] > -1 and \
                                    tilecoords[1] > -1:
                        self.map.set_map(tilecoords, self.cursor.layer, (-1, -1))
                        print self.map.collide_list
                        if tilecoords in self.map.collide_list:
                            num = 0
                            for i in self.map.collide_list:
                                if i == tilecoords:
                                    break
                                num += 1
                            print num
                            del (self.map.collide_list[num])
                        self.map.get_surface()
                if self.cursor.brush == 1:
                    factpos = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tilecoords = [int(float(factpos[0]) / 32.0), int(float(factpos[1]) / 32.0)]
                    self.map.clear(self.cursor.layer, tilecoords)
                    self.map.get_surface()
                if self.cursor.brush == 2:
                    factpos = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                    tilecoords = [int(float(factpos[0]) / 32.0), int(float(factpos[1]) / 32.0)]
                    self.map.subs(self.cursor.layer, tilecoords, (-1, -1))
                    self.map.get_surface()
            if self.cursor.type == 1:
                pass
            if self.cursor.type == 2:
                factpos = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                tilecoords = [int(float(factpos[0]) / 32.0), int(float(factpos[1]) / 32.0)]
                if tilecoords in self.map.mobs_spawn:
                    num = 0
                    for mobpos in self.map.mobs_spawn:
                        if mobpos == tilecoords:
                            break
                        else:
                            num += 1
                    del (self.map.mobs_spawn[num])
                    self.map.get_surface()
            if self.cursor.type == 3:
                factpos = [self.cursor.pos[0] - self.map.pos[0], self.cursor.pos[1] - self.map.pos[1]]
                tilecoords = [int(float(factpos[0]) / 32.0), int(float(factpos[1]) / 32.0)]
                if tilecoords in self.map.ways[self.cursor.layer]:
                    num = 0
                    for waypos in self.map.ways[self.cursor.layer]:
                        if waypos == tilecoords:
                            break
                        else:
                            num += 1
                    del (self.map.ways[self.cursor.layer][num])
                    self.map.get_surface()

    def handleKeyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.keys['s'] = True
            if event.key == pygame.K_l:
                self.keys['l'] = True
            if event.key == pygame.K_LCTRL:
                self.keys['ctrl'] = True
            if event.key == pygame.K_UP:
                self.keys['UP'] = True
            if event.key == pygame.K_DOWN:
                self.keys['DOWN'] = True
            if event.key == pygame.K_LEFT:
                self.keys['LEFT'] = True
            if event.key == pygame.K_RIGHT:
                self.keys['RIGHT'] = True
            if event.key == pygame.K_LSHIFT:
                self.keys['lshift'] = True
            if event.key == pygame.K_RSHIFT:
                self.keys['rshift'] = True
            if event.key == pygame.K_LALT:
                self.keys['LALT'] = True
            if event.key == pygame.K_RALT:
                self.keys['RALT'] = True
            if event.key == pygame.K_RETURN:
                self.keys['ENTER'] = True
            if event.key == pygame.K_1:
                self.cursor.layer = 0
            if event.key == pygame.K_2:
                self.cursor.layer = 1
            if event.key == pygame.K_3:
                self.cursor.layer = 2
            if event.key == pygame.K_4:
                self.cursor.layer = 3
            if event.key == pygame.K_5:
                self.cursor.layer = 4
            if event.key == pygame.K_c:
                self.cursor.collidable = not self.cursor.collidable
            if event.key == pygame.K_TAB:
                self.map.draw_collide = not self.map.draw_collide
                self.map.get_surface()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.keys['s'] = False
            if event.key == pygame.K_UP:
                self.keys['UP'] = False
            if event.key == pygame.K_DOWN:
                self.keys['DOWN'] = False
            if event.key == pygame.K_LEFT:
                self.keys['LEFT'] = False
            if event.key == pygame.K_RIGHT:
                self.keys['RIGHT'] = False
            if event.key == pygame.K_LSHIFT:
                self.keys['lshift'] = False
            if event.key == pygame.K_RSHIFT:
                self.keys['rshift'] = False
            if event.key == pygame.K_LALT:
                self.keys['LALT'] = False
            if event.key == pygame.K_RALT:
                self.keys['RALT'] = False
            if event.key == pygame.K_RETURN:
                self.keys['ENTER'] = False
            if event.key == pygame.K_l:
                self.keys['l'] = False
            if event.key == pygame.K_LCTRL:
                self.keys['ctrl'] = False

    def handleMouse(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.cursor.last_pos = self.cursor.pos
            self.cursor.pos = event.pos
            change = [self.cursor.last_pos[0] - self.cursor.pos[0], self.cursor.last_pos[1] - self.cursor.pos[1]]
            if self.keys['middle']:
                self.map.pos[0] -= change[0]
                self.map.pos[1] -= change[1]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                self.tile_menu.scroll -= 32
            if event.button == 4:
                if self.tile_menu.scroll < 0:
                    self.tile_menu.scroll += 32
            if event.button == 1:
                self.cursor.left_click()
                self.editor(event)
            if event.button == 2:
                self.keys['middle'] = True
            if event.button == 3:
                self.delete(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                self.keys['middle'] = False

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.map.save('ExitBU.mp')
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                data.screensize = event.size
                self.screen = pygame.display.set_mode(data.screensize, pygame.RESIZABLE)
                # pygame.display.toggle_fullscreen()
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                self.handleKeyboard(event)
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.handleMouse(event)

    def gameloop(self):
        self.clock = pygame.time.Clock()
        while True:
            self.clock.tick(60)
            pygame.display.set_caption(data.title + ' FPS: ' + str(int(round(self.clock.get_fps()))))
            self.update()
            self.handleEvents()
            self.render()


if __name__ == "__main__":
    scene = Scene()
