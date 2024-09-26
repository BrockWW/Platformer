import pygame as pg

class Character(pg.sprite.Sprite):
    def __init__(self, screen_size):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = self.load_image("images/t_louis.jpg", 0.5, -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.bottomleft = 10, screen_size[1]-50+self.rect[0]
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
        # initialize position and movement each update
        newpos = self.rect.move((self.move, 0))
        movement = [0,0]

        # check out of bounds
        if self.rect.bottom >= level.background.get_height()-5:
            # reload the level
            level.level_one()
            # reset louis location
            self.rect.bottomleft = 10, screen_size[1]-50+self.rect[0]

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
            # jump
            if keys[pg.K_w] and self.jump == False:
                self.velocity = -30
                self.jump = True
            # move until half way across screen, then allow backward motion to left edge of screen
            if self.rect.right < level.screen_size[0]//2 and keys[pg.K_d]:
                movement = [10, 0]
            if self.rect.left >= 5 and keys[pg.K_a]:
                movement = [-10, 0]

            # move louis
            movement[1] += self.velocity
            newpos = self.rect.move(movement)
            self.rect = newpos


class Level:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.level_one()

    def move_level(self, keys, character):
        screen_move = pg.Vector2(0,0)
        if keys[pg.K_d] and character.rect.right >= screen_size[0]//2:
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

        #############################
        # building platforms of level

        self.platforms.append(self.create_vectors([20, 500, self.screen_size[1]-50, self.screen_size[1]]))
        self.platforms.append(self.create_vectors([800, 2000, self.screen_size[1]-200, self.screen_size[1]-150]))
        self.platforms.append(self.create_vectors([800, 1400, self.screen_size[1]-500, self.screen_size[1]-450]))
        self.platforms.append(self.create_vectors([1700, 2000, self.screen_size[1]-500, self.screen_size[1]-450]))
        self.platforms.append(self.create_vectors([2000, 3000, self.screen_size[1]-200, self.screen_size[1]-150]))
        self.platforms.append(self.create_vectors([3500, 3700, self.screen_size[1]-100, self.screen_size[1]-50]))

        #############################

        # creating platforms 
        self.draw_platforms()

    def draw_platforms(self):
        self.background.fill("black")
        for platform in self.platforms:
            pg.draw.polygon(self.background, "white", platform)

    def create_vectors(self, corners):
        x_0, x_1, y_0, y_1 = corners
        ul = pg.Vector2(x_0, y_1)
        ur = pg.Vector2(x_1, y_1)
        br = pg.Vector2(x_1, y_0)
        bl = pg.Vector2(x_0, y_0)

        return [ul,ur,br,bl]



class GameEnvironment:
    def __init__(self, screen_size, music):
        self.level = Level(screen_size)
        self.character = Character(screen_size)
        self.music = music

    def run_game(self):
        # pygame setup
        clock = pg.time.Clock()
        allsprites = pg.sprite.RenderPlain(self.character)
        if self.music == True:
            pg.mixer.music.load("music/goofy_ahh.mp3")
            pg.mixer.music.play(loops=-1)
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
            self.level.move_level(keys, self.character)

            # flip() the display to put your work on screen
            pg.display.flip()

            # set FPS
            clock.tick(60)

        pg.quit()
        

# initialize pygame modules
pg.init()
pg.font.init()
pg.display.init()

screen_size = [2000, 1200]
platformer = GameEnvironment(screen_size, False)
platformer.run_game()