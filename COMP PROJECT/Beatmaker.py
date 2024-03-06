import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)
green = (0,255,0)
gold = (212,175,55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('Arial Rounded Bold.ttf', 40)

def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen , gray , [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen , gray , [0, HEIGHT-200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]

    text_labels = ['Hi Hat', 'Snare', 'Kick', 'Crash', 'Clap', 'Tom',]
    text_positions = [(30, i*100 + 30) for i in range(len(text_labels))]
    for label, pos in zip(text_labels, text_positions):
        text_surface = label_font.render(label, True, white)
        screen.blit(text_surface, pos)

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0,(i*100)+100),(200,(i*100)+100), 3) 

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200)//beats) + 205 ,(j*100)+5, ((WIDTH-200) // beats)-10, ((HEIGHT-200)//instruments -10)],0,3)

            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200)//beats) + 200 ,(j*100), ((WIDTH-200) // beats), ((HEIGHT-200)//instruments)],5,5)

            pygame.draw.rect(screen, black, [i * ((WIDTH - 200)//beats) + 200 ,(j*100), ((WIDTH-200) // beats), ((HEIGHT-200)//instruments)],2,5)

            boxes.append((rect, (i,j)))

            active = pygame.draw.rect(screen,blue, [beat*((WIDTH-200)//beats)+200, 0, (WIDTH-200)//beats, instruments*100],5,3)
    return(boxes)



fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

#SOUNDS
hi_hat = mixer.Sound('sounds/hi hat.WAV')
snare = mixer.Sound('sounds/snare.WAV')
kick = mixer.Sound('sounds/kick.WAV')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.wav')
tom = mixer.Sound("sounds/tom.WAV")

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()



run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].colliderect(pygame.Rect(event.pos[0], event.pos[1], 1, 1)):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
    beat_length = fps * 60 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit()