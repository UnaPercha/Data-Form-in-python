#Background estilo rendija
#generador aleatorio de n minas
#input de click izq y click dcho
#contador de minas alrededor de cada rendija

import pygame #libreria para hacer juegos en python
import sys #libreria para poder trabajar con el sistema
import os #libreria Operation System

width, height = 1000, 800
screen = pygame.display.set_mode((width, height)) #tamaño de la pantalla
pygame.display.set_caption("El Buscaminas") #nombre que se verá arriba de la ventana

while True:     #este while es para que la ventana no se cierre al instante
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


#COLORES
darkGreen = (100, 223, 54)
lightGreen = (146, 230, 115)
redFlag = (229, 38, 38)
blueOne = (30, 165, 227)
greenTwo = (32, 164, 19)
redThree = (173, 27, 27)
purpleFour = (92, 18, 176)
darkBrown = (223, 163, 115)
lightBrown = (232, 189, 155)

FPS = 60

#background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.jpg")), (width, height))
background = pygame.transform.scale(pygame.image.load(
    os.path.join("C:\Users\Usuario\VisualCodeStudio\py\proyectos\Juegos\buscaminas\Assets\background.jpg")), (width, height))

def drawWindow():
    screen.blit(background, (500, 400))
    pygame.display.update

def main():
    
    clock = pygame.time.Clock()
    run = True
    
    while run:          
        clock.tick(FPS) #reduce la tasa de frames a 60 x segundo
        
        for event in pygame.event.get:  #si cierras la ventana se para el juego
            if event == pygame.QUIT:    
                run = False
                pygame.quit()
            drawWindow()
    main()