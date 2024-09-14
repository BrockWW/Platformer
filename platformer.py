import pygame as pg

class Character(pg.sprite.Sprite):
    def __init__(self, screen_size):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = self.load_image("images/t_louis.jpg", 0.5, -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.bottomleft = 0, screen_size[1]-50+self.rect[0]
        self.move = 18
        self.jump = False
        self.velocity = 0

    def load_image(self, path, scale, colorkey):
        image = pg.image.load(path)
        size = image.get_size()
        size = (size[0] * scale, size[1] * scale)
        image = pg.transform.scale(image, size)
        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        
        return image, image.get_rect()
    
    def move_character(self, keys, level):
        newpos = self.rect.move((self.move, 0))
        movement = [0,0]

        # check out of bounds
        if self.rect.bottom >= level.background.get_height()-5:
            self.rect.bottomleft = 0, screen_size[1]-50+self.rect[0]
            
            level.level_one()

            

        # else continue motion
        else:
            # gravity
            if level.background.get_at(self.rect.midbottom) != (255,255,255):
                self.velocity += 1
                newpos = self.rect.move((0, 5))
                self.rect = newpos
            elif level.background.get_at(self.rect.midbottom) == (255,255,255):
                self.velocity = 0
                self.jump = False

            if keys[pg.K_w] and self.jump == False:
                self.velocity = -30
                self.jump = True

            movement[1] += self.velocity
            newpos = self.rect.move(movement)
            self.rect = newpos


class Level:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.level_one()

    def move_level(self, keys):
        screen_move = pg.Vector2(0,0)
        if keys[pg.K_a]:
            screen_move = pg.Vector2(10,0)
        if keys[pg.K_d]:
            screen_move = pg.Vector2(-10,0)

        for i in range(len(self.platforms)):
            for j in range(len(self.platforms[i])):
                self.platforms[i][j] += screen_move

        self.draw_platforms()
                

    def level_one(self):
        self.screen = pg.display.set_mode(self.screen_size)
        self.background = pg.Surface(self.screen_size)
        self.background.fill("black")
        self.platforms = []
        self.drawn_plats = []

        # plat 1
        self.plat_1_ul = pg.Vector2(0, self.screen_size[1]-50)
        self.plat_1_ur = pg.Vector2(500, self.screen_size[1]-50)
        self.plat_1_br = pg.Vector2(500, self.screen_size[1])
        self.plat_1_bl = pg.Vector2(0, self.screen_size[1])

        self.plat_1 = [self.plat_1_ul, self.plat_1_ur, self.plat_1_br, self.plat_1_bl]
        self.platforms.append(self.plat_1)

        # plat 2
        self.plat_2_ul = pg.Vector2(800, self.screen_size[1]-200)
        self.plat_2_ur = pg.Vector2(2000, self.screen_size[1]-200)
        self.plat_2_br = pg.Vector2(2000, self.screen_size[1]-100)
        self.plat_2_bl = pg.Vector2(800, self.screen_size[1]-100)

        self.plat_2 = [self.plat_2_ul, self.plat_2_ur, self.plat_2_br, self.plat_2_bl]
        self.platforms.append(self.plat_2)

        # plat 3
        self.plat_3_ul = pg.Vector2(0, self.screen_size[1]-500)
        self.plat_3_ur = pg.Vector2(500, self.screen_size[1]-500)
        self.plat_3_br = pg.Vector2(500, self.screen_size[1]-450)
        self.plat_3_bl = pg.Vector2(0, self.screen_size[1]-450)

        self.plat_3 = [self.plat_3_ul, self.plat_3_ur, self.plat_3_br, self.plat_3_bl]
        self.platforms.append(self.plat_3)

        # plat 4
        self.plat_4_ul = pg.Vector2(800, self.screen_size[1]-500)
        self.plat_4_ur = pg.Vector2(1400, self.screen_size[1]-500)
        self.plat_4_br = pg.Vector2(1400, self.screen_size[1]-450)
        self.plat_4_bl = pg.Vector2(800, self.screen_size[1]-450)

        self.plat_4 = [self.plat_4_ul, self.plat_4_ur, self.plat_4_br, self.plat_4_bl]
        self.platforms.append(self.plat_4)

        # plat 5
        self.plat_5_ul = pg.Vector2(1700, self.screen_size[1]-500)
        self.plat_5_ur = pg.Vector2(2000, self.screen_size[1]-500)
        self.plat_5_br = pg.Vector2(2000, self.screen_size[1]-450)
        self.plat_5_bl = pg.Vector2(1700, self.screen_size[1]-450)

        self.plat_5 = [self.plat_5_ul, self.plat_5_ur, self.plat_5_br, self.plat_5_bl]
        self.platforms.append(self.plat_5)

        # plat 6
        self.plat_6_ul = pg.Vector2(2000, self.screen_size[1]-200)
        self.plat_6_ur = pg.Vector2(3000, self.screen_size[1]-200)
        self.plat_6_br = pg.Vector2(3000, self.screen_size[1]-150)
        self.plat_6_bl = pg.Vector2(2000, self.screen_size[1]-150)

        self.plat_6 = [self.plat_6_ul, self.plat_6_ur, self.plat_6_br, self.plat_6_bl]
        self.platforms.append(self.plat_6)

        # saving original positions of platforms
        #self.original_positions = self.platforms.copy()


        # creating platforms 
        self.draw_platforms()

        '''# creating platforms 
        # plat 1
        pg.draw.polygon(self.background, "white", [(0, self.screen_size[1]-50), (500, self.screen_size[1]-50), (500,self.screen_size[1]), (0,self.screen_size[1])])
        # plat 2
        pg.draw.polygon(self.background, "white", [(800, self.screen_size[1]-200), (2000, self.screen_size[1]-200), (2000,self.screen_size[1]-100), (800,self.screen_size[1]-100)])
        # plat 3
        pg.draw.polygon(self.background, "white", [(0, self.screen_size[1]-500), (500, self.screen_size[1]-500), (500,self.screen_size[1]-450), (0,self.screen_size[1]-450)])
        # plat 4
        pg.draw.polygon(self.background, "white", [(800, self.screen_size[1]-500), (1400, self.screen_size[1]-500), (1400,self.screen_size[1]-450), (800,self.screen_size[1]-450)])
        # plat 5
        pg.draw.polygon(self.background, "white", [(1700, self.screen_size[1]-500), (2000, self.screen_size[1]-500), (2000,self.screen_size[1]-450), (1700,self.screen_size[1]-450)])
        # plat 5
        pg.draw.polygon(self.background, "white", [(2000, self.screen_size[1]-200), (3000, self.screen_size[1]-200), (3000,self.screen_size[1]-150), (200,self.screen_size[1]-150)])'''

    def draw_platforms(self):
        self.background.fill("black")
        for platform in self.platforms:
            pg.draw.polygon(self.background, "white", platform)


class GameEnvironment:
    def __init__(self, screen_size):
        self.level = Level(screen_size)
        self.character = Character(screen_size)

    def run_game(self):
        # pygame setup
        clock = pg.time.Clock()
        allsprites = pg.sprite.RenderPlain(self.character)
        #pg.mixer.music.load("music/goofy_ahh.mp3")
        #pg.mixer.music.play(loops=-1)
        running = True

        # creating level
        self.level.level_one()

        # game loop
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            # movement code
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                running = False

            # show louis
            allsprites.update()
            self.level.screen.blit(self.level.background, (0, 0))
            allsprites.draw(self.level.screen)
            
            self.character.move_character(keys, self.level)
            self.level.move_level(keys)

            # flip() the display to put your work on screen
            pg.display.flip()

            # set FPS
            clock.tick(60)

        pg.quit()
        

# initialize pygame modules
pg.init()
pg.font.init()
pg.display.init()

screen_size = [2000, 1000]
platformer = GameEnvironment(screen_size)
platformer.run_game()