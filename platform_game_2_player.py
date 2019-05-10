import pygame, os
import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'          # centrowanie okna
pygame.init()


## ustawienia ekranu i gry
screen = pygame.display.set_mode(gm.SIZESCREEN)
pygame.display.set_caption('Prosta gra platformowa...')
clock = pygame.time.Clock()


# klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.items = set()
        self.movement_x = 0
        self.movement_y = 0
        self.count = 0
        self.lifes = 3
        self.level = None
        self.direction_of_movement = 'right'

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def turn_left(self):
        self.direction_of_movement='left'
        self.movement_x=-6

    def turn_right(self):
        self.direction_of_movement = 'right'
        self.movement_x= 6

    def stop(self):
        self.movement_x=0
    def _move(self, image_list):
        if self.count <4:
            self.image=image_list[0]
        if self.count>=4 and self.count<8:
            self.image=image_list[1]

        if self.count>8:
            self.count=0
        else:
            self.count += 1

    def update(self):
        #Ruch w poziomie
        self.rect[0]+=self.movement_x
        #animacja (co 4)
        if self.movement_x  > 0:
            self._move(gm.IMAGES_R)
        if self.movement_x  < 0:
            self._move(gm.IMAGES_L)
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                self.turn_left()
            if event.key==pygame.K_RIGHT:
                self.turn_right()
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT and self.movement_x < 0:
                self.stop()
                self.image=gm.STAND_L
            if event.key == pygame.K_RIGHT and self.movement_x > 0:
                self.stop()
                self.image = gm.STAND_R


class Platform(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, rect_x, rect_y):
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Level():

    def __init__(self,player:Player):
        self.player = player
        self.set_of_platforms = set()

    def update(self):
        for s in self.set_of_platforms:
            s.update()

    def draw(self, surface):
        for s in self.set_of_platforms:
            s.draw(surface)


class Level_1(Level):
    def __init__(self, player:Player):
        super().__init__(player)


        list_platforms = [[420, 70, 750, 330],
                          [980, 70, 0, gm.HEIGHT - 70],
                          [560, 70, 0, 170],
                          [140, 70, 1240, 50]]

        for w in list_platforms:
            self.set_of_platforms.add(Platform(gm.DARKRED, *w))

# konkretyzacja obiektów
player = Player(gm.STAND_R)
player.rect.center = screen.get_rect().center
current_level = Level_1(player)
player.level = current_level


# głowna pętla gry
window_open = True
while window_open:
    screen.fill(gm.LIGHTBLUE)
    # pętla zdarzeń
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        elif event.type == pygame.QUIT:
            window_open = False
        player.get_event(event)



    # rysowanie i aktualizacja obiektów
    player.draw(screen)
    player.update()

    current_level.update()
    current_level.draw(screen)

    # aktualizacja okna pygame
    pygame.display.flip()
    clock.tick(30)

pygame.quit()