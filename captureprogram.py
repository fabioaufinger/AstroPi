import sys
import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

WIDTH = 1280
HEIGHT = 720

black = (0, 0, 0)
red = (255, 0, 0)
darkred = (180, 0, 0)

#screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(WIDTH, HEIGHT))
cam.start()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        
        if click[0] == 1 and action != None:
            action()
            
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    
def quit_programm():
    cam.stop()
    pygame.quit()
    sys.exit()
    
    
while True:
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              cam.stop()
              pygame.quit()
              sys.exit()

    image1 = cam.get_image()
    image1 = pygame.transform.scale(image1,(640,480))
    screen.blit(image1,(25, 25))
    
    
    button("EXIT", 740, 480, 100, 50, darkred, red, quit_programm)
   
    

    pygame.display.update()