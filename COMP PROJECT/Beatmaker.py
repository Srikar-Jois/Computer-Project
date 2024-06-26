import pygame
from pygame import mixer
import time
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (23,23,23)
white = (227,222,219)
gray = (128,128,128)
light_gray = (182,181,179)
dark_gray = (84,82,80)
green = (201,60,74)
gold = (212,175,55)
blue = (0, 255, 255)


screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('HELN.TTF', 32) 
medium_font = pygame.font.Font('HELN.TTF', 24)



def draw_grid(clicks, beat, actives, volume):
    instrument_colors = [(201, 60, 74),  
                         (240, 118, 70),  
                         (242, 198, 101),  
                         (18, 99, 119),  
                         (31, 150, 153),  
                         (156, 192, 185)]  
    left_box = pygame.draw.rect(screen , gray , [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen , gray , [0, HEIGHT-200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]

    text_labels = ['Hi Hat', 'Snare', 'Kick', 'Crash', 'Clap', 'Bass',]
    index1 = [0,1,2,3,4,5]
    text_positions = [(30, i*100 + 30) for i in range(len(text_labels))]
    for label, pos, num in zip(text_labels, text_positions,index1):
        text_surface = label_font.render(label, True, instrument_colors[num])
        screen.blit(text_surface, pos)

    for i in range(instruments):
        pygame.draw.line(screen, gray, (0,(i*100)+100),(200,(i*100)+100), 3) 

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray

            else:
                if actives[j] == 1:
                    color = instrument_colors[j]
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200)//beats) + 205 ,(j*100)+5, ((WIDTH-200) // beats)-10, ((HEIGHT-200)//instruments -10)],0,3)


            pygame.draw.rect(screen, black, [i * ((WIDTH - 200)//beats) + 200 ,(j*100), ((WIDTH-200) // beats), ((HEIGHT-200)//instruments)],2,5)

            boxes.append((rect, (i,j)))

            active = pygame.draw.rect(screen,blue, [beat*((WIDTH-200)//beats)+200, 0, (WIDTH-200)//beats, instruments*100],5,3)
            if j == 5:
                current_note = notes[note_indices[i]]
                note_text = label_font.render(current_note, True, white)
                screen.blit(note_text, (i * ((WIDTH - 200)//beats) + 220, j * 100 + 20))  # Adjust position as needed
    return(boxes)

def draw_save_menu(beat_name,typing):
    pygame.draw.rect(screen,black,[0,0,WIDTH,HEIGHT])
    menu_text = label_font.render('Save Menu : Enter name for current Beat',True,white)
    saving_btn = pygame.draw.rect(screen,gray,[WIDTH//2 - 200,HEIGHT*0.75,400,100],0,5)
    saving_txt = label_font.render('Save Beat',True,white)
    screen.blit(saving_txt,(WIDTH//2-75,HEIGHT*0.75+30))
    screen.blit(menu_text,(400,40))
    exit_btn = pygame.draw.rect(screen,gray,[WIDTH-200, HEIGHT-100, 180, 90],0,5)
    exit_text = label_font.render('Close',True,white)
    screen.blit(exit_text, (WIDTH-160,HEIGHT-70))
    if typing:
        pygame.draw.rect(screen,dark_gray,[400, 200, 600, 200],0,5)
    entry_rect = pygame.draw.rect(screen,gray,[400,200,600,200],5,5)
    entry_txt = label_font.render(f'{beat_name}',True,white)
    screen.blit(entry_txt,(430,250))
    return exit_btn, saving_btn, entry_rect

def draw_load_menu(index):
    global volume, notes, count
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    loaded_count = 0 
    pygame.draw.rect(screen,black,[0,0,WIDTH,HEIGHT])
    menu_text = label_font.render('Load Menu : Select Beat to Load',True,white)
    loading_btn = pygame.draw.rect(screen,gray,[WIDTH//2 - 200,HEIGHT*0.87,400,100],0,5)
    loading_txt = label_font.render('Load Beat',True,white)
    screen.blit(loading_txt,(WIDTH//2-75,HEIGHT*0.87+30))
    delete_btn = pygame.draw.rect(screen,gray,[(WIDTH//2)-500, HEIGHT * 0.87,200,100],0,5)
    delete_txt = label_font.render("Delete Beat", True, white)
    screen.blit(delete_txt,(WIDTH//2-485, HEIGHT * 0.87 + 30))
    screen.blit(menu_text,(400,40))
    exit_btn = pygame.draw.rect(screen,gray,[WIDTH-200, HEIGHT-100, 180, 90],0,5)
    exit_text = label_font.render('Close',True,white)
    screen.blit(exit_text, (WIDTH-160,HEIGHT-70))
    loaded_rectangle = pygame.draw.rect(screen,gray,[190, 90, 1000, 600],5,5)
    saved_beats.sort(key=lambda x: int(x.split('count:')[1].strip()), reverse=True)
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen,light_gray,[190,100+index*50,1000,50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name:') + 6
            name_index_end = saved_beats[beat].index(", beats: ")
            count_index_start = saved_beats[beat].index('count:') + 7 
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
            count_text = medium_font.render(f'Count: {saved_beats[beat][count_index_start:]}', True, white)  # Render count
            screen.blit(count_text, (700, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beats_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8:beats_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm_start = saved_beats[beat].index('bpm:') + 5
            loaded_bpm_end = saved_beats[beat].index(',volume:')
            loaded_bpm = int(saved_beats[beat][loaded_bpm_start:loaded_bpm_end].strip())
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            loaded_volume_start = saved_beats[beat].index('volume:') + 8
            loaded_volume_end = saved_beats[beat].index(', selected')+1
            loaded_volume_string = saved_beats[beat][loaded_volume_start+1:loaded_volume_end-2]
            loaded_volume = [int(vol) for vol in loaded_volume_string.strip().strip('[]').split(", ")]
            loaded_count_start = saved_beats[beat].index('count:') + 7
            loaded_count = int(saved_beats[beat][loaded_count_start:].strip()) 

            # Assign the loaded volume data to the 'volume' variable
            volume = loaded_volume

    
            
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rectangle = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, entry_rectangle,delete_btn, loaded_rectangle, loaded_info

index = 100
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
count = 0


notes = ['C','C#', 'D','D#', 'E', 'F','F#', 'G','G#', 'A','A#', 'B', 'C']
note_indices = [0 for _ in range(beats)] 
beat_name = ''
typing = False

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
    index2 = [0,1,2,3,4,5]
    text_positions = [(30, i*100 + 30) for i in range(len(text_labels))]
    for pos, num in zip(text_positions,index2 ):
        # Draw volume button
        volume_button_rect = pygame.Rect(150, pos[1], 40, 40)
        pygame.draw.rect(screen, gray, volume_button_rect,0,5)
        volume_list.append(volume_button_rect)
        vol_text = medium_font.render(f'{int(volume[num])}',True,white)
        screen.blit(vol_text,(150, pos[1]+5))

    # SAVE AND LOAD DRAW
    save_button = pygame.draw.rect(screen,gray,[900,HEIGHT-150,200,48],0,5)
    load_button = pygame.draw.rect(screen,gray,[900,HEIGHT-100,200,48],0,5)
    save_text = label_font.render("Save Beat",True,white)
    load_text = label_font.render("Load Beat",True,white)
    screen.blit(save_text,(920,HEIGHT-140))
    screen.blit(load_text,(920,HEIGHT-90))

    # CLEAR BOARD
    clear_button = pygame.draw.rect(screen,gray,[1150,HEIGHT-150,200,100],0,5)
    clear_text = label_font.render("RESET",True,white)
    screen.blit(clear_text,(1190,HEIGHT-120))

    #SAVE and LOAD
    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button,loading_button, entry_rectangle ,delete_button, loaded_rectangle, loaded_info  = draw_load_menu(index)

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  
            if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
                for i in range(len(boxes)):
                    if boxes[i][0].colliderect(pygame.Rect(event.pos[0], event.pos[1], 1, 1)):
                        coords = boxes[i][1]
                        if coords[1] == 5: 
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
                note_indices = [0] * beats 
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
                typing = False
                beat_name = ''
            if entry_rectangle.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False
                    else:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50
            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w')
                    saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm},volume: {volume}, selected: {clicked}, bass_notes: {note_indices}, count: {count}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats[index] = saved_beats[index].strip()  # Remove any leading/trailing whitespace
                        count_index_start = saved_beats[index].index('count:') + 7
                        count_value = int(saved_beats[index][count_index_start:].strip())
                        count_value += 1
                        saved_beats[index] = saved_beats[index][:count_index_start] + f' {count_value}'   # Update the count in the string
                        count = count_value

                        loaded_info = saved_beats[index]
                        beats_index_start = loaded_info.index('beats:') + 7
                        beats_index_end = loaded_info.index(', bpm:')
                        beats = int(loaded_info[beats_index_start:beats_index_end])
                        bpm_index_start = loaded_info.index('bpm:') + 5
                        bpm_index_end = loaded_info.index(',volume:')
                        bpm = int(loaded_info[bpm_index_start:bpm_index_end])
                        volume_index_start = loaded_info.index('volume:') + 8
                        volume_index_end = loaded_info.index(', selected:')
                        volume_string = loaded_info[volume_index_start:volume_index_end].strip().strip('[]')
                        volume = [int(vol) for vol in volume_string.split(',')]
                        clicked_index_start = loaded_info.index('selected:') + 11
                        clicked_index_end = loaded_info.index(', bass_notes:')
                        clicked_string = loaded_info[clicked_index_start:clicked_index_end].strip().strip('[]').split('], [')
                        clicked = [[int(note) for note in row.split(', ')] for row in clicked_string]
                        note_indices_index_start = loaded_info.index('bass_notes:') + 12
                        note_indices_index_end = loaded_info.index(', count:')
                        note_indices_string = loaded_info[note_indices_index_start:note_indices_index_end].strip().strip('[]')
                        note_indices = [int(note) for note in note_indices_string.split(', ')]
                        count_index_start = loaded_info.index('count:') + 7
                        count = int(loaded_info[count_index_start:])
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False

                        file = open('saved_beats.txt', 'w')
                        for line in saved_beats:
                            file.write(str(line) + '\n')
                        file.close()
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0:
                beat_name = beat_name[:-1]
                
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
