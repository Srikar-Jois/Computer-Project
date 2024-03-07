import pygame
from pygame import mixer
import time
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)
dark_gray = (50,50,50)
green = (0,255,0)
gold = (212,175,55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('Arial Rounded Bold.ttf', 32)
medium_font = pygame.font.Font('Arial Rounded Bold.ttf', 24)



def draw_grid(clicks, beat, actives, volume):
    left_box = pygame.draw.rect(screen , gray , [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen , gray , [0, HEIGHT-200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]

    text_labels = ['Hi Hat', 'Snare', 'Kick', 'Crash', 'Clap', 'Bass',]
    index = [0,1,2,3,4,5]
    text_positions = [(30, i*100 + 30) for i in range(len(text_labels))]
    for label, pos, num in zip(text_labels, text_positions,index ):
        text_surface = label_font.render(label, True, colors[actives[num]])
        screen.blit(text_surface, pos)

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0,(i*100)+100),(200,(i*100)+100), 3) 

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray

            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200)//beats) + 205 ,(j*100)+5, ((WIDTH-200) // beats)-10, ((HEIGHT-200)//instruments -10)],0,3)

            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200)//beats) + 200 ,(j*100), ((WIDTH-200) // beats), ((HEIGHT-200)//instruments)],5,5)

            pygame.draw.rect(screen, black, [i * ((WIDTH - 200)//beats) + 200 ,(j*100), ((WIDTH-200) // beats), ((HEIGHT-200)//instruments)],2,5)

            boxes.append((rect, (i,j)))

            active = pygame.draw.rect(screen,blue, [beat*((WIDTH-200)//beats)+200, 0, (WIDTH-200)//beats, instruments*100],5,3)
            if j == 5:
                current_note = notes[note_indices[i]]
                note_text = label_font.render(current_note, True, white)
                screen.blit(note_text, (i * ((WIDTH - 200)//beats) + 220, j * 100 + 20))  # Adjust position as needed
    return(boxes)

def draw_save_menu():
    pygame.draw.rect(screen,black,[0,0,WIDTH,HEIGHT])
    exit_btn = pygame.draw.rect(screen,gray,[WIDTH-200, HEIGHT-100, 180, 90],0,5)
    exit_text = label_font.render('Close',True,white)
    screen.blit(exit_text, (WIDTH-160,HEIGHT-70))
    return exit_btn

def draw_load_menu():
    pygame.draw.rect(screen,black,[0,0,WIDTH,HEIGHT])
    exit_btn = pygame.draw.rect(screen,gray,[WIDTH-200, HEIGHT-100, 180, 90],0,5)
    exit_text = label_font.render('Close',True,white)
    screen.blit(exit_text, (WIDTH-160,HEIGHT-70))
    return exit_btn


fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt','r')
for line in file:
    saved_beats.append(line)

notes = ['C','C#', 'D','D#', 'E', 'F','F#', 'G','G#', 'A','A#', 'B', 'C']
note_indices = [0 for _ in range(beats)] 

# SOUNDS
hi_hat = mixer.Sound('sounds/hi hat.WAV')
snare = mixer.Sound('sounds/snare.WAV')
kick = mixer.Sound('sounds/kick.WAV')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.wav')

volume = [10, 10, 10, 10, 10, 10]

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            # Set volume for each instrument

            if i == 0:
                hi_hat.set_volume(volume[i]/10)
                hi_hat.play()
            if i == 1:
                snare.set_volume(volume[i]/10)
                snare.play()
            if i == 2:
                kick.set_volume(volume[i]/10)
                kick.play()
            if i == 3:
                crash.set_volume(volume[i]/10)
                crash.play()
            if i == 4:
                clap.set_volume(volume[i]/10)
                clap.play()
            if i == 5:
                sound_index = note_indices[active_beat] % len(notes)
                sound = mixer.Sound(f"sounds/BASS Notes/{notes[sound_index]}.wav")
                sound.play()
                sound.set_volume(volume[i]/10)
    
            


# GAME
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list, volume)

    # LOWER MENU
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT-150,200,100],0,5)
    play_text = label_font.render('Play/Pause',True,white)
    screen.blit(play_text, (70, HEIGHT-130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT-90))

    # BPM
    bpm_rect = pygame.draw.rect(screen,gray,[300,HEIGHT-150,200,100],5,5)
    bpm_text = medium_font.render("Beats Per Min",True,white)
    screen.blit(bpm_text,(318,HEIGHT-130))
    bpm_text2 = label_font.render(f'{bpm}' , True, white)
    screen.blit(bpm_text2,(370,HEIGHT-100))
    bpm_add_rect = pygame.draw.rect(screen,gray,[510,HEIGHT-150,48,48],0,5)
    bpm_sub_rect = pygame.draw.rect(screen,gray,[510,HEIGHT-100,48,48],0,5)
    add_text = medium_font.render("+5",True,white)
    sub_text = medium_font.render("-5",True,white)
    screen.blit(add_text,(520,HEIGHT-140))
    screen.blit(sub_text,(520,HEIGHT-90))

    # BEATS
    beats_rect = pygame.draw.rect(screen,gray,[600,HEIGHT-150,200,100],5,5)
    beats_text = medium_font.render("Beats In Loop",True,white)
    screen.blit(beats_text,(618,HEIGHT-130))
    beats_text2 = label_font.render(f'{beats}' , True, white)
    screen.blit(beats_text2,(690,HEIGHT-100))
    beats_add_rect = pygame.draw.rect(screen,gray,[810,HEIGHT-150,48,48],0,5)
    beats_sub_rect = pygame.draw.rect(screen,gray,[810,HEIGHT-100,48,48],0,5)
    beatsadd_text = medium_font.render("+1",True,white)
    beatssub_text = medium_font.render("-1",True,white)
    screen.blit(beatsadd_text,(820,HEIGHT-140))
    screen.blit(beatssub_text,(820,HEIGHT-90))

    # INSTRUMENTS
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0,i*100),(200,100))
        instrument_rects.append(rect)
    
    #VOLUME
    volume_list = []
    text_labels = ['Hi Hat', 'Snare', 'Kick', 'Crash', 'Clap', 'Tom',]
    index = [0,1,2,3,4,5]
    text_positions = [(30, i*100 + 30) for i in range(len(text_labels))]
    for pos, num in zip(text_positions,index ):
        # Draw volume button
        volume_button_rect = pygame.Rect(150, pos[1], 40, 40)
        pygame.draw.rect(screen, gray, volume_button_rect,0,5)
        volume_list.append(volume_button_rect)
        vol_text = medium_font.render(f'{int(volume[num])}',True,white)
        screen.blit(vol_text,(150, pos[1]+5))

    # SAVE AND LOAD
    save_button = pygame.draw.rect(screen,gray,[900,HEIGHT-150,200,48],0,5)
    load_button = pygame.draw.rect(screen,gray,[900,HEIGHT-100,200,48],0,5)
    save_text = label_font.render("Save Beat",True,white)
    load_text = label_font.render("Load Beat",True,white)
    screen.blit(save_text,(920,HEIGHT-140))
    screen.blit(load_text,(920,HEIGHT-90))

    # CLEAR BOARD
    clear_button = pygame.draw.rect(screen,gray,[1150,HEIGHT-150,200,100],0,5)
    clear_text = label_font.render("Clear Board",True,white)
    screen.blit(clear_text,(1160,HEIGHT-120))

    if save_menu:
        exit_button = draw_save_menu()
    if load_menu:
        exit_button = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Check if Shift key is pressed
            if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
                for i in range(len(boxes)):
                    if boxes[i][0].colliderect(pygame.Rect(event.pos[0], event.pos[1], 1, 1)):
                        coords = boxes[i][1]
                        # Shift+click increments the note index and cycles through the notes
                        if coords[1] == 5:  # Check if the clicked instrument is Tom
                            note_indices[coords[0]] = (note_indices[coords[0]] + 1) % len(notes)
        elif event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].colliderect(pygame.Rect(event.pos[0], event.pos[1], 1, 1)):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        
        elif event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
                    active_beat = 0
                    active_length = 0
            if bpm_add_rect.collidepoint(event.pos):
                bpm +=5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -=5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                if beats > len(note_indices):
                    note_indices.extend([0] * (beats - len(note_indices)))
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1 
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
                if beats < len(note_indices):
                    note_indices = note_indices[:beats]
    
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
        
            # Adjust volume on click
            for i, rect in enumerate(volume_list):
                if rect.collidepoint(event.pos):
                    if volume[i] < 10:
                        volume[i] += 1
                    else:
                        volume[i] = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                
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
