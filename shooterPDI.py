from cv2 import flip
import pygame, random, cv2
import numpy as np

#----------------------------------DEFINICION DE VARIABLES----------------------------------
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

#-----------------------------FUNCIONES IMPLEMENTADOS PARA EL PROCESAMIENTO DE IMAGENES-----------------------------
# FUNCION QUE DEFINE EL MOVIMIENTO DEL JUGADOR A PARTIR DEL PROCESAMIENTO DE IMAGENES
def set_movement(cx, shape):
    if cx < int(shape/3):
        return -10, "izquierda"
    elif cx > int(shape/3)*2:
        return 10, "derecha"
    else:
        return 0, "centro"

# FUNCION PARA DIBUJAR LA CUADRICULA EN LA IMAGEN
def draw_grid(shape):
    #cv2.line(frame, (0, int(shape[0]/2)), (int(shape[1]), int(shape[0]/2)), (0, 255, 0), 2)
    cv2.line(frame, (int(shape[1]/3), 0), (int(shape[1]/3), int(shape[0])), (0, 255, 0), 2)
    cv2.line(frame, (int(shape[1]/3)*2, 0), (int(shape[1]/3)*2, int(shape[0])), (0, 255, 0), 2)

# SE DEFINE POR DEFECTO LA WEBCAM (0)
vid = cv2.VideoCapture(0)

hsv_low = np.array([172,109,148], np.uint8)
hsv_high = np.array([179, 255, 255], np.uint8)

#hsv_low = np.array([89,152,89], np.uint8)
#hsv_high = np.array([111, 255, 255], np.uint8)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

#-----------------------------DEFINICION DE LAS CLASES PARA LA IMPLEMENTACIÓN DEL JUEGO-----------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, - 100)
            self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, [0,0])
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#--------------------------------------------------------------------------------------------------------------------

meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
                "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
                "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

#### ---------- GAME OVER
game_over = True
running = True
moving_left = False
moving_right = False
time_elapsed_since_last_action = 0

while running:
    #Pantalla inicial del juego
    if game_over:

        show_go_screen()
        # Define los Sprites para las animaciones en el juego
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        #Crea el jugador como una nueva instancia de la clase
        player = Player()
        all_sprites.add(player)
        for i in range(6): #Generación de los meteoritos, 6 por defecto
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0
        
    dt = clock.tick(60)
    
    time_elapsed_since_last_action += dt
    # dt es medida en milisegundos, 1000 ms = 1 s
    if time_elapsed_since_last_action > 1000:
        player.shoot() # Ejecuta la funcion para disparo shoot()
        time_elapsed_since_last_action = 0 # Resetea a cero el contador 
    
    #PDI
    ret, frame = vid.read() # Realiza la captura frame-por-frame de la webcam
    frame = cv2.flip(frame, 1) # Cambia el frame a una vista espejo
    if ret == True:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Realiza el cambio de representación de RGB a HSV
        mask = cv2.inRange(hsv_frame, hsv_low, hsv_high) # Genera la máscara a partir de los valores HSV para el color del objeto
        contours, hierachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Encuentra los objetos y sus contornos de cada objeto identificado con eso color
        #El parametro CHAIN_APPROX_SIMPLE simplifica la deteccion de los contornos utilizando menos puntos
        for contour in contours: #Ciclo para calcular la posición del objeto a identificar
            area = cv2.contourArea(contour) #Calcula el area de cada objeto identificado por su contorno
            if area > 400: #Condicional para discriminar solo el objeto a partir del area
                M = cv2.moments(contour) #Calculo de los momentos para identificar su posicion
                if M['m00'] != 0: 
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)
                    cv2.putText(frame, str(cx) + " " + str(cy), (50,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)

                    speed, direccion = set_movement(cx, frame.shape[1]) #Funcion para determinar la direccion del movimiento a partir de la posicion en x
                    player.rect.x += speed #Realiza el movimiento del jugador de acuerdo al valor entregado por la funcion anterior
                    cv2.putText(frame, direccion, (int(frame.shape[1]/2)-20,50), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
        
        draw_grid(frame.shape) #Dibuja la cuadricula en la ventana de la webcam            
        cv2.imshow('frame', frame) #Muestra el frame en una nueva ventana
    
    #----------------------------- CONTROL CON EL TECLADO -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
              player.shoot()
    
    all_sprites.update()

    #colisiones - meteoro - laser
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor() 
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Checar colisiones - jugador - meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    #Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # Escudo.
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()
cv2.destroyAllWindows()