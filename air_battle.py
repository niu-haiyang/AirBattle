"""
    air battle program
"""
import time
import pygame
import sys
import random
import shelve
import math


class Resource:
    """game resource"""
    # background images TODO <author, dictionary can be set to images dictionary>
    backgrounds = {'start_page': './images/start_page.png',
                   'quit_page': './images/quit_page.png',
                   'ranking_page': './images/rank_page.png',
                   'stage_1': './images/stage_1.png',
                   'stage_2': './images/stage_2.png',
                   'stage_3': './images/stage_3.png',
                   'stage_4': './images/stage_4.png',
                   'stage_5': './images/stage_5.png',
                   }
    # hero images
    heroes = {'hero1': './images/hero1.png',
              'hero2': './images/hero2.png',
              'hero3': './images/hero3.png',
              'hero1_hp': './images/hero1_hp.png',
              'hero2_hp': './images/hero2_hp.png',
              'hero3_hp': './images/hero3_hp.png',
              }

    # enemy images
    enemies = {'enemy1': './images/enemy1.png',
               'enemy2': './images/enemy2.png',
               'enemy3': './images/enemy3.png',
               'enemy4': './images/enemy4.png',
               'old_enemy1': './images/old_enemy1.png',
               'old_enemy2': './images/old_enemy2.png',
               'old_enemy3': './images/old_enemy3.png',
               }
    # bullets
    bullets = {'bullet1': './images/bullet1.png',
               'bullet2': './images/bullet2.png',
               'bullet3': './images/bullet3.png',
               'chase_bullet': './images/chase_bullet.png',
               'supply_left_bullet': './images/supply_left_bullet.png',
               'supply_right_bullet': './images/supply_right_bullet.png',
               'enemy_bullet': './images/enemy_bullet.png',
               'old_enemy_bullet': './images/old_enemy_bullet.png',
               }
    # buttons
    buttons = {'pause_button': './images/pause_button.png',
               'start_button': './images/start_button.png',
               'ranking_button': './images/ranking_button.png'
               }
    # music
    musics = {'stage_3': './musics/DreamItPossible.mp3',
              'stage_2': './musics/GoTime.mp3',
              'stage_1': './musics/nizhan.mp3',
              'victory': './musics/Victory.mp3',
              'boom': './musics/boom.wav',
              'punch': './musics/punch.wav',
              }
    # explosion
    explosions = {'explosion': './images/explosion.png',
                  'small_explosion': './images/small_explosion.png',
                  'old_enemy_explosion': './images/old_enemy_explosion.png'}
    # supply
    supply = {'supply': './images/supply.png'}
    # font
    fonts = {'font': './fonts/font.TTF'}


class GameSprite(pygame.sprite.Sprite):
    """creat game sprite"""

    def __init__(self, image_path, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Background(GameSprite):
    """creat Background sprite"""

    def __init__(self, image_path, x=0, y=0, speed=1, ready=False):
        """initialize background sprite"""
        super().__init__(image_path, x, y)
        self.speed = speed
        if ready:
            self.rect.y = -self.rect.height

    def update(self):
        """update background location"""
        self.rect.y += self.speed
        if self.rect.y > self.rect.height:
            self.rect.y = -self.rect.height


class Hero(GameSprite):
    """creat hero air"""

    def __init__(self, image_path, speed):
        """initialize hero sprite"""
        super().__init__(image_path)
        self.speed = speed
        # set hero start location
        self.rect.y = WINDOW_SIZE[1] - self.rect.height
        self.rect.x = WINDOW_SIZE[0] / 2 - self.rect.width / 2

    def update(self):
        """update hero location and boundary detect"""
        self.move()
        self.boundary_detect()

    def move(self):
        # get user's keyboard
        keyboard_event = pygame.key.get_pressed()
        hero_speed = self.speed + 5
        if keyboard_event[pygame.K_UP]:
            # hero move up
            self.rect.y -= hero_speed

        if keyboard_event[pygame.K_DOWN]:
            # hero move down
            self.rect.y += hero_speed

        if keyboard_event[pygame.K_LEFT]:
            # hero move left
            self.rect.x -= hero_speed

        if keyboard_event[pygame.K_RIGHT]:
            # hero move right
            self.rect.x += hero_speed

    def boundary_detect(self):
        # boundary detect
        if self.rect.y <= 0:
            self.rect.y = 0

        if self.rect.y >= WINDOW_SIZE[1] - self.rect.height:
            self.rect.y = WINDOW_SIZE[1] - self.rect.height

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x > WINDOW_SIZE[0] - self.rect.width:
            self.rect.x = WINDOW_SIZE[0] - self.rect.width

    def fire(self, bullet_type=1):
        """hero fire"""
        # creat different type bullet sprite
        if bullet_type == 1:
            bullet = HeroBullet(Resource.bullets['bullet1'], self.rect.centerx, self.rect.y)
            return bullet

        if bullet_type == 2:
            bullet = HeroBullet(Resource.bullets['bullet2'], self.rect.centerx, self.rect.y)
            return bullet

        if bullet_type == 3:
            bullet = HeroBullet(Resource.bullets['bullet3'], self.rect.centerx, self.rect.y)
            return bullet


class Enemy(GameSprite):
    """enemy sprite"""

    def __init__(self, image_path, speed, life, enemy_type):
        """initialize enemy"""
        super().__init__(image_path, speed)
        self.speed = speed + 2
        # set enemy location
        self.rect.x = random.randint(0, WINDOW_SIZE[0] - self.rect.width)
        self.rect.y = -self.rect.height
        self.life = life
        self.type = enemy_type

    def update(self):
        """update enemy location and kill them"""
        self.rect.y += self.speed
        if self.rect.y > WINDOW_SIZE[1]:
            # reduce hero score
            # score -= 1
            self.kill()

    def fire(self, speed):
        """enemy fire"""
        enemy_bullet = EnemyBullet(Resource.bullets['enemy_bullet'], self.rect.centerx, self.rect.y, speed)
        return enemy_bullet


class OldEnemy(GameSprite):
    """most powerful enemy"""

    def __init__(self, image_path, life=50, speed_x=3, speed_y=3):
        super().__init__(image_path)
        self.life = life
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        # detect location
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x >= WINDOW_SIZE[0] - self.rect.width:
            self.speed_x = -self.speed_x
        elif self.rect.x <= 0:
            self.speed_x = -self.speed_x

        if self.rect.y <= 0:
            self.speed_y = -self.speed_y
        elif self.rect.y >= WINDOW_SIZE[1] - self.rect.height:
            self.speed_y = -self.speed_y

    def fire(self):
        bullet1 = EnemyBullet(Resource.bullets['old_enemy_bullet'], self.rect.centerx, self.rect.y, speed=5)
        bullet2 = EnemyBullet(Resource.bullets['chase_bullet'],
                              self.rect.centerx, self.rect.y, chase=True)

        return bullet1, bullet2

    def empty_enemy(self):
        pass


class HeroBullet(GameSprite):
    """hero bullet sprite, used to hero fire"""

    def __init__(self, image_path, hero_centerx, hero_y, speed=12, manual_left=False, manual_right=False):
        """initialize hero bullet"""
        super().__init__(image_path)
        self.rect.centerx = hero_centerx
        self.rect.y = hero_y - self.rect.height / 2
        self.hero_centerx = hero_centerx
        self.speed = speed
        # detect whether manual fire
        self.manual_left = manual_left
        self.manual_right = manual_right

    def update(self):
        """update hero bullet and kill hero bullet if bullet out window"""
        self.move()
        self.boundary_detect()

    def move(self):
        """move"""
        self.rect.y -= self.speed
        # manual fire
        if self.manual_left:
            self.rect.x -= self.speed

        if self.manual_right:
            self.rect.x += self.speed

    def boundary_detect(self):
        """detect boundary"""
        if self.rect.y < -self.rect.height:
            self.kill()

        elif self.rect.y > WINDOW_SIZE[1] + self.rect.height:
            self.kill()

        if self.rect.x < -self.rect.width:
            self.kill()

        elif self.rect.x > WINDOW_SIZE[0] + self.rect.width:
            self.kill()


class EnemyBullet(GameSprite):
    """enemy sprite, used to enemy fire"""

    def __init__(self, image_path, enemy_centerx, enemy_y, speed=1, chase=False, life=250):
        """initialize enemy bullet sprite"""
        super().__init__(image_path)
        self.rect.centerx = enemy_centerx
        self.rect.y = enemy_y + self.rect.height * 2
        self.speed = speed + 5
        self.chase = chase
        self.life = life

    def update(self, hero_x=0, hero_y=0):
        """update enemy bullet and kill enemy bullet if bullet out window"""
        if not self.chase:
            self.rect.y += self.speed

        if self.chase:
            self.life -= 1
            if (self.rect.centerx - hero_x) < 0:
                self.rect.centerx += self.speed
            else:
                self.rect.centerx -= self.speed
            if (self.rect.centery - hero_y) < 0:
                self.rect.centery += self.speed
            else:
                self.rect.centery -= self.speed
            if math.sqrt((self.rect.centerx - hero_x) ** 2 + (self.rect.centery - hero_y) ** 2) < 300:
                self.speed = 2
            else:
                self.speed = 5

        if self.life <= 0:
            self.kill()

        if self.rect.y >= WINDOW_SIZE[1]:
            self.kill()


class Button(GameSprite):
    """buttons in the air battle game"""

    def __init__(self, image_path):
        super().__init__(image_path)
        self.rect.x = WINDOW_SIZE[0] - self.rect.width


class Explosion(GameSprite):
    """enemy or hero explosion"""

    def __init__(self, image_path, x, y, life=30):
        super().__init__(image_path, x, y)
        self.life = life

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()


class Supply(GameSprite):
    """supply: strengthen hero fire"""

    def __init__(self, image_path):
        """supply location is random"""
        super().__init__(image_path)
        self.rect.x = random.randint(0, WINDOW_SIZE[0] - 100)
        self.rect.y = random.randint(100, WINDOW_SIZE[1] - 100)


class Protect(Supply):
    """protect hero"""

    def __init__(self, image_path, life=180, collide=False):
        super().__init__(image_path)
        self.life = life
        self.collide = collide

    def update(self, hero_x, hero_y):
        global PRO
        if self.collide:
            self.rect.centerx = hero_x
            self.rect.centery = hero_y
            self.life -= 1
        if self.life <= 0:
            PRO = False
            self.kill()


class Engine:
    """control the game process"""

    def __init__(self, level=1):
        # initialize pygame
        pygame.init()
        # game level
        self.__level = level
        # load background , hero ,buttons, music, font, strengthen_fire
        background1 = Background(Resource.backgrounds['stage_' + str(self.__level)], speed=self.__level)
        background2 = Background(Resource.backgrounds['stage_' + str(self.__level)], speed=self.__level, ready=True)
        self.__hero = Hero(Resource.heroes['hero' + str(self.__level)], speed=self.__level)
        self.__pause_button = Button(Resource.buttons['pause_button'])
        self.__start_button = Button(Resource.buttons['start_button'])
        pygame.mixer.music.load(Resource.musics['stage_' + str(self.__level)])
        self.boom = pygame.mixer.Sound(Resource.musics['boom'])
        self.punch = pygame.mixer.Sound(Resource.musics['punch'])
        self.__font = pygame.font.Font(Resource.fonts['font'], 45)
        self.__strengthen_fire = False
        # creat hero life quantity --- 5
        self.__life = 5
        self.__hero_hp = Background(Resource.heroes['hero%s_hp' % str(self.__level)])
        # hero score
        self.__score = 45
        self.__text = self.__font.render('Score: ' + str(self.__score), True, (255, 0, 0))
        # set game window
        self.__window = pygame.display.set_mode(WINDOW_SIZE, 1, 32)
        pygame.display.set_caption('AirBattle')
        # creat all sprite group
        self.__resource = pygame.sprite.Group(background1, background2, self.__hero, self.__pause_button)
        self.__bullet_group = pygame.sprite.Group()
        self.__enemy_group = pygame.sprite.Group()
        self.__enemy_bullet_group = pygame.sprite.Group()
        self.__supply_group = pygame.sprite.Group()
        self.__old_enemy_group = pygame.sprite.Group()
        self.__old_enemy_bullet_group = pygame.sprite.Group()
        self.__protect_group = pygame.sprite.Group()
        # fps control
        self.clock = pygame.time.Clock()
        # index
        self.__index = 0

    def run(self):
        while True:
            # play music
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            # fps = 60
            self.clock.tick(60)
            self.event_control()
            self.collide()
            self.render()

    def event_control(self):
        """control user's event"""
        # get window keyboard
        event_list = pygame.event.get()
        if len(event_list) > 0:
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ENEMY_EVENT:
                    # load different enemy
                    image = random.randint(1, 4)
                    speed = self.__level
                    if image == 1:
                        enemy = Enemy(Resource.enemies['enemy1'], speed, life=1, enemy_type=1)
                        self.__enemy_group.add(enemy)
                    if image == 2:
                        enemy = Enemy(Resource.enemies['enemy2'], speed, life=2, enemy_type=2)
                        self.__enemy_group.add(enemy)
                    if image == 3:
                        enemy = Enemy(Resource.enemies['enemy3'], speed, life=3, enemy_type=3)
                        self.__enemy_group.add(enemy)
                    if image == 4:
                        enemy = Enemy(Resource.enemies['enemy4'], speed, life=4, enemy_type=4)
                        self.__enemy_group.add(enemy)

                if event.type == FIRE_EVENT:
                    # hero fire
                    bullet = self.__hero.fire(bullet_type=self.__level)
                    self.__bullet_group.add(bullet)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.__strengthen_fire:
                        # manual fire
                        bullet = HeroBullet(Resource.bullets['supply_left_bullet'],
                                            self.__hero.rect.left, self.__hero.rect.y, manual_left=True)
                        self.__bullet_group.add(bullet)
                        bullet = HeroBullet(Resource.bullets['supply_right_bullet'],
                                            self.__hero.rect.right, self.__hero.rect.y, manual_right=True)
                        self.__bullet_group.add(bullet)
                        # supply only can be used 15 times
                        self.punch.play()
                        self.__index += 1
                        if self.__index > 15:
                            self.__strengthen_fire = False

                if event.type == ENEMY_BULLET_EVENT:
                    # enemy fire
                    for enemy in self.__enemy_group.sprites():
                        speed = self.__level
                        bullet = enemy.fire(speed)
                        self.__enemy_bullet_group.add(bullet)

                if event.type == OLD_ENEMY_BULLET_EVENT:
                    i = random.randint(1, 2)
                    for enemy in self.__old_enemy_group.sprites():
                        bullet1, bullet2 = enemy.fire()
                        if i == 1:
                            self.__enemy_bullet_group.add(bullet1)
                        if i == 2:
                            self.__old_enemy_bullet_group.add(bullet2)

                if event.type == SUPPLY_EVENT:
                    # creat supply
                    supply = Supply(Resource.supply['supply'])
                    self.__supply_group.add(supply)

                if event.type == PROTECT_EVENT:
                    protect = Protect('./images/protect.png')
                    self.__protect_group.add(protect)

        # pause, get mouse position
        x, y = pygame.mouse.get_pos()
        lock = False
        # judge mouse whether on pause button
        if WINDOW_SIZE[0] - self.__pause_button.rect.width < x < WINDOW_SIZE[0] and \
                0 < y < self.__pause_button.rect.height:
            mouse_tuple = pygame.mouse.get_pressed()
            if mouse_tuple[0]:
                lock = not lock
                self.__resource.remove(self.__pause_button)
                self.__resource.add(self.__start_button)
                self.__resource.draw(self.__window)
                time.sleep(0.3)
        if lock:
            pygame.mixer.music.pause()
            while True:
                event_list = pygame.event.get()
                if len(event_list) > 0:
                    for event in event_list:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                x, y = pygame.mouse.get_pos()
                # judge mouse whether on pause button
                if WINDOW_SIZE[0] - self.__pause_button.rect.width < x < WINDOW_SIZE[0] and \
                        0 < y < self.__pause_button.rect.height:
                    pygame.event.clear()
                    mouse_tuple = pygame.mouse.get_pressed()
                    if mouse_tuple[0]:
                        lock = not lock
                        self.__resource.remove(self.__start_button)
                        self.__resource.add(self.__pause_button)
                        self.__resource.draw(self.__window)
                        time.sleep(0.5)
                # sprite group render and update
                self.__resource.draw(self.__window)
                self.__enemy_group.draw(self.__window)
                self.__bullet_group.draw(self.__window)
                self.__enemy_bullet_group.draw(self.__window)
                self.__supply_group.draw(self.__window)
                self.__old_enemy_group.draw(self.__window)
                # add life value
                for i in range(1, self.__life + 1):
                    x = WINDOW_SIZE[0] - self.__hero_hp.rect.width * i
                    y = WINDOW_SIZE[1] - self.__hero_hp.rect.height
                    self.__window.blit(self.__hero_hp.image, (x, y))

                # add score
                self.__text = self.__font.render('Score: ' + str(self.__score), True, (255, 0, 0))
                self.__window.blit(self.__text, (0, 0))
                # game window update
                pygame.display.update()
                if not lock:
                    pygame.mixer.music.unpause()
                    break

    def collide(self):
        """collide detected"""
        global PRO
        # judge score
        if self.__score >= 50 * self.__level and len(self.__old_enemy_group) == 0:
            # old enemy appear
            old_enemy = OldEnemy(Resource.enemies['old_enemy' + str(self.__level)], life=50 * self.__level)
            self.__old_enemy_group.add(old_enemy)
            self.__enemy_group.empty()
            self.__enemy_bullet_group.empty()

        # collision detection --- protect
        protect = pygame.sprite.spritecollide(self.__hero, self.__protect_group, False)
        print(protect)
        if protect and not PRO:
            self.__protect_group.remove(protect)
            protect = Protect('./images/protect.png', collide=True)
            self.__protect_group.add(protect)
            PRO = True

        if not PRO:
            # collision detection -- old enemy
            injured_old_enemy = pygame.sprite.spritecollide(self.__hero, self.__old_enemy_group, False)
            if injured_old_enemy:
                self.__life -= 1

            # collision detection
            injured_enemy = pygame.sprite.spritecollide(self.__hero, self.__enemy_group, False)
            injured_bullet = pygame.sprite.spritecollide(self.__hero, self.__enemy_bullet_group, True)
            injured_chase_bullet = pygame.sprite.spritecollide(self.__hero, self.__old_enemy_bullet_group, True)
            # calculate hero life
            if injured_enemy:
                # hero life
                self.__life -= 1
                self.__enemy_group.remove(injured_enemy[0])
                x, y = self.__hero.rect.centerx - 25, self.__hero.rect.bottom - 50
                self.explode(Resource.explosions['small_explosion'], x, y, 5)
            if injured_bullet:
                self.__life -= 1
                x, y = self.__hero.rect.centerx - 25, self.__hero.rect.bottom - 50
                self.explode(Resource.explosions['small_explosion'], x, y, 5)
            if injured_chase_bullet:
                self.__life -= 1
                x, y = self.__hero.rect.x, self.__hero.rect.y
                self.explode(Resource.explosions['explosion'], x, y, 10)

            # hero died, game over
            if self.__life <= 0:
                self.__hero.kill()
                self.explode(Resource.explosions['explosion'], self.__hero.rect.x, self.__hero.rect.y, 20)
                self.boom.play()
                self.__resource.draw(self.__window)
                pygame.display.update()
                time.sleep(3)
                return self.quit_page()

        # collision detection
        bullet_enemy_dict = pygame.sprite.groupcollide(self.__bullet_group, self.__enemy_group, True, False)
        # calculate score
        if bullet_enemy_dict:
            # enemy explosion
            bullet = list(bullet_enemy_dict.keys())[0]
            self.explode(Resource.explosions['small_explosion'], bullet.rect.x, bullet.rect.y - 50, 5)
            injured_enemy = list(bullet_enemy_dict.values())
            injured_enemy = injured_enemy[0][0]
            injured_enemy.life -= 1
            self.boom.play()

            if injured_enemy.life <= 0:
                self.__enemy_group.remove(injured_enemy)
                self.explode(Resource.explosions['explosion'], injured_enemy.rect.x, injured_enemy.rect.y, 20)
                # score
                self.__score += injured_enemy.type
                self.__text = self.__font.render('Score: ' + str(self.__score), True, (255, 0, 0))
        # collision detection ---old enemy
        injured_old_enemy = pygame.sprite.groupcollide(self.__bullet_group, self.__old_enemy_group, True, False)
        if injured_old_enemy:
            bullet = list(injured_old_enemy.keys())[0]
            injured_old_enemy = list(injured_old_enemy.values())
            x, y = bullet.rect.x, bullet.rect.y - 100
            self.explode(Resource.explosions['small_explosion'], x, y, 5)
            # enemy explosion
            injured_old_enemy[0][0].life -= 1
            self.boom.play()
            if injured_old_enemy[0][0].life == 0:
                # level up
                x, y = (injured_old_enemy[0][0]).rect.x, (injured_old_enemy[0][0]).rect.y
                injured_old_enemy[0][0].kill()
                self.explode(Resource.explosions['old_enemy_explosion'], x, y, 20)
                self.__resource.draw(self.__window)
                pygame.display.update()
                time.sleep(3)
                self.level_up(self.__level)

        # collision detection ---supply
        supply = pygame.sprite.spritecollide(self.__hero, self.__supply_group, True)
        if supply:
            self.__strengthen_fire = True
            self.__index = 0

    def render(self):
        # sprite group render and update
        self.__resource.draw(self.__window)
        self.__resource.update()
        self.__enemy_group.draw(self.__window)
        self.__enemy_group.update()
        self.__bullet_group.draw(self.__window)
        self.__bullet_group.update()
        self.__enemy_bullet_group.draw(self.__window)
        self.__enemy_bullet_group.update()
        self.__supply_group.draw(self.__window)
        self.__old_enemy_group.update()
        self.__old_enemy_group.draw(self.__window)
        self.__old_enemy_bullet_group.update(self.__hero.rect.centerx, self.__hero.rect.centery)
        self.__old_enemy_bullet_group.draw(self.__window)
        self.__protect_group.update(self.__hero.rect.centerx, self.__hero.rect.centery)
        self.__protect_group.draw(self.__window)
        # draw life line
        for enemy in self.__old_enemy_group:
            pygame.draw.line(self.__window, (0, 0, 0),
                             (enemy.rect.left, enemy.rect.top - 10),
                             (enemy.rect.right, enemy.rect.top - 10),
                             2)
            # if life > 20%--->green, if life < 20% ---->red
            energy_remain = enemy.life / (50 * self.__level)
            if energy_remain > 0.2:
                energy_color = (0, 255, 0)
            else:
                energy_color = (255, 0, 0)
            pygame.draw.line(self.__window, energy_color,
                             (enemy.rect.left, enemy.rect.top - 10),
                             (enemy.rect.left + enemy.rect.width * energy_remain,
                              enemy.rect.top - 10), 2)
        # add life value
        for i in range(1, self.__life + 1):
            x = WINDOW_SIZE[0] - self.__hero_hp.rect.width * i
            y = WINDOW_SIZE[1] - self.__hero_hp.rect.height
            self.__window.blit(self.__hero_hp.image, (x, y))

        # add score
        self.__text = self.__font.render('Score: ' + str(self.__score), True, (255, 0, 0))
        self.__window.blit(self.__text, (0, 0))
        # game window update
        pygame.display.update()

    def explode(self, image_path, x, y, life):
        """explosion"""
        explosion = Explosion(image_path, x, y, life)
        self.__resource.add(explosion)

    def level_up(self, level):
        """level up"""
        global PRO
        if level == 1:
            level = level + 1
            pygame.time.set_timer(ENEMY_EVENT, 3000)
            pygame.time.set_timer(ENEMY_BULLET_EVENT, 3000 - (level * 300))
            PRO = False
            self.__init__(level=level)
        elif level == 2:
            level = level + 1
            pygame.time.set_timer(ENEMY_EVENT, 2000)
            pygame.time.set_timer(ENEMY_BULLET_EVENT, 3000 - (level * 300))
            PRO = False
            self.__init__(level=level)

    def rank_page(self):
        """display rank data"""

        file = shelve.open('./data/ranks')
        ranks = file['ranks']
        rank_background = Background(Resource.backgrounds['ranking_page'])
        while True:
            self.clock.tick(60)
            event_list = pygame.event.get()
            if len(event_list) > 0:
                for event in event_list:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            self.__window.blit(rank_background.image, (0, 0))
            for rank in range(1, 11):
                text = self.__font.render('%s      ' % str(rank) + str(ranks[rank - 1]), True, (0, 104, 150))
                x, y = WINDOW_SIZE[0] / 2 - 100, rank * 50 + 150
                self.__window.blit(text, (x, y))

            # click the quit button to quit page
            x, y = pygame.mouse.get_pos()
            if 500 < x < WINDOW_SIZE[0] and WINDOW_SIZE[1] - 100 < y < WINDOW_SIZE[1]:
                event_tuple = pygame.mouse.get_pressed()
                if event_tuple[0]:
                    return self.quit_page()
            pygame.display.update()

    def start_page(self):
        """start page"""
        pygame.init()
        pygame.mixer.music.load(Resource.musics['victory'])
        while True:
            # play music
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            # control event
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            start_background = Background(Resource.backgrounds['start_page'], speed=0)
            # click the region to enter game
            x, y = pygame.mouse.get_pos()
            if 70 < x < start_background.rect.width and \
                    start_background.rect.height - 200 < y < start_background.rect.height:

                event_tuple = pygame.mouse.get_pressed()
                if event_tuple[0]:
                    break

            self.__window.blit(start_background.image, (0, 0))
            pygame.display.update()
        self.__init__(level=1)
        return self.run()

    def quit_page(self):
        """quit page"""
        pygame.init()
        self.__window = pygame.display.set_mode(WINDOW_SIZE, 1, 32)
        pygame.mixer.music.load(Resource.musics['victory'])
        # finally score and level
        level = self.__font.render('Hero Level: ' + str(self.__level), True, (45, 148, 250))
        score = self.__font.render('Score: ' + str(self.__score) + '\t(截图分享, 谁人不服?)', True, (45, 128, 250))
        # rank data
        file = shelve.open('./data/ranks')
        ranks = file['ranks']
        rank = (self.__level - 1) * 100 + self.__score
        ranks.append(rank)
        ranks.sort(reverse=True)
        ranks = ranks[0:10]
        file['ranks'] = ranks
        file.close()
        while True:
            # play music
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            quit_background = Background(Resource.backgrounds['quit_page'], speed=0)
            ranking_button = Button(Resource.buttons['ranking_button'])
            # click the quit button to quit game
            x, y = pygame.mouse.get_pos()
            if 500 < x < quit_background.rect.width and \
                    quit_background.rect.height - 100 < y < quit_background.rect.height:
                event_tuple = pygame.mouse.get_pressed()
                if event_tuple[0]:
                    pygame.quit()
                    sys.exit()

            # click the again button to again game
            x, y = pygame.mouse.get_pos()
            if 500 < x < quit_background.rect.width and \
                    quit_background.rect.height - 200 < y < quit_background.rect.height - 100:
                event_tuple = pygame.mouse.get_pressed()
                if event_tuple[0]:
                    self.__init__(self.__level)
                    return self.run()

            # click the Ranking button to ranking page
            x, y = pygame.mouse.get_pos()
            if WINDOW_SIZE[0] - 100 < x < WINDOW_SIZE[0] and 0 < y < WINDOW_SIZE[1] - 50:
                event_tuple = pygame.mouse.get_pressed()
                if event_tuple[0]:
                    return self.rank_page()

            self.__window.blit(quit_background.image, (0, 0))
            self.__window.blit(ranking_button.image, (WINDOW_SIZE[0] - ranking_button.rect.width - 10, 0))
            self.__window.blit(level, (WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 3 - 100))
            self.__window.blit(score, (WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 3))
            pygame.display.update()


# set user event --- constants
FIRE_EVENT = pygame.USEREVENT
pygame.time.set_timer(FIRE_EVENT, 500)
ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_EVENT, 4000)
ENEMY_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_BULLET_EVENT, 3000)
SUPPLY_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(SUPPLY_EVENT, 30000)
OLD_ENEMY_BULLET_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(OLD_ENEMY_BULLET_EVENT, 6000)
PROTECT_EVENT = pygame.USEREVENT + 5
pygame.time.set_timer(PROTECT_EVENT, 20000)
PRO = False
WINDOW_SIZE = (1200, 900)

if __name__ == '__main__':
    engine = Engine()
    engine.start_page()
