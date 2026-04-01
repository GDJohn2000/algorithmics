from pygame import *

#clase padre para objetos
class GameSprite(sprite.Sprite):
   #constructor de clase
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # cada objeto debe almacenar una propiedad image
       self.image = transform.scale(image.load(player_image), (55, 55))
       self.speed = player_speed
       # cada objeto debe almacenar la propiedad rect en la cual está inscrito
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y


   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#clase derivada para el objeto del jugador (controlado por las flechas)
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 80:
           self.rect.y += self.speed

#clase derivada para el objeto enemigo (se mueve solo)
class Enemy(GameSprite):
   def update(self):
       if self.rect.x <= 470:
           self.side = "derecha"
       if self.rect.x >= win_width - 85:
           self.side = "izquierda"
       if self.side == "izquierda":
           self.rect.x -= self.speed
       else:
           self.rect.x += self.speed

#clase para objetos de los obstáculos
class Wall(sprite.Sprite):
   def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
       super().__init__()
       self.color_1 = color_1
       self.color_2 = color_2
       self.color_3 = color_3
       self.width = wall_width
       self.height = wall_height
       # imagen de la pared – un rectángulo del color y tamaño deseado
       self.image = Surface((self.width, self.height))
       self.image.fill((color_1, color_2, color_3))
       # cada objeto debe almacenar la propiedad rect
       self.rect = self.image.get_rect()
       self.rect.x = wall_x
       self.rect.y = wall_y
   def draw_wall(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
       #draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))

#Escena del juego:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Laberinto")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

#Personajes del juego:
player = Player('hero.png', 5, win_height - 80, 4)

monsters = [
m1 := Enemy('cyborg.png', win_width - 80, 280, 2),
m2 := Enemy('cyborg.png', win_width - 70, 230, 2),
m1 := Enemy('cyborg.png', win_width - 60, 180, 2),
m1 := Enemy('cyborg.png', win_width - 50, 130, 2),
m1 := Enemy('cyborg.png', win_width - 40, 80, 2),
]

final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

#Walls Color, position, size
walls = [
w1 := Wall(154, 205, 50, 100, 20 , 400, 10),
w2 := Wall(154, 205, 50, 100, 480, 400, 10),
w3 := Wall(154, 205, 50, 100, 20 , 10, 380),
w4 := Wall(154, 205, 50, 200, 100 , 10, 380),
w5 := Wall(154, 205, 50, 300, 20 , 10, 380),
w6 := Wall(154, 205, 50, 400, 100 , 10, 380),
w7 := Wall(154, 205, 50, 500, 20 , 10, 380),
]

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('¡GANASTE!', True, (255, 215, 0))
lose = font.render('¡PERDISTE!', True, (180, 0, 0))

#música
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
   for e in event.get():
       if e.type == QUIT:
           game = False
  
   if finish != True:
       window.blit(background,(0, 0))
       player.update()
       for every_monster in monsters :
        every_monster.update()
    
       player.reset()
       for every_monster in monsters :
        every_monster.reset()
       final.reset()

       for every_wall in walls:
            every_wall.draw_wall()

       #Situación de “Derrota”
       for collide in walls :
            if sprite.collide_rect(player, collide) :
                finish = True
                window.blit(lose, (200, 200))
                kick.play()
       for collide in monsters :
        if sprite.collide_rect(player, collide) :
         finish = True
         window.blit(lose, (200, 200))
         kick.play()

       #Situación de “Victoria”
        if sprite.collide_rect(player, final):
           finish = True
           window.blit(win, (200, 200))
           money.play()

   display.update()
   clock.tick(FPS)
quit()