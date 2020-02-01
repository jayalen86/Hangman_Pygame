import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512) #used to fix sound delay
pygame.init()
iconimg = pygame.image.load('Images/iconimg.png')
pygame.display.set_caption('Hangman')
pygame.display.set_icon(iconimg)
screen_height = 540
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255,255,255))
clock = pygame.time.Clock()
background = [pygame.image.load('Images/gibbet'+str(number)+'.png') for number in range(1,8)]
all_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = [pygame.image.load('Images/'+x+'.png') for x in all_letters]
line = pygame.image.load('Images/line.png')
wrong_answer_sound = pygame.mixer.Sound("Sounds/wronganswer.wav")
right_answer_sound = pygame.mixer.Sound("Sounds/rightanswer.wav")
wordlist = ['Pie', 'Tire', 'Octagon', 'Car', 'Frog', 'Dinosaur', 'Mother', 'Nylon', 'Torrid', 'Sample','Dog', 'Fire']
word = random.sample(wordlist, len(wordlist))[0]
guessed_letters = []
missed_guesses = []
guesses = 0
gameover = False

def redraw_screen():
    screen.fill((255,255,255))
    screen.blit(background[guesses], (120, 100))
    x_axis = 10
    for x, val in enumerate(all_letters):
        y_axis = 20 if x < 13 else 70
        screen.blit(letters[x], (x_axis, y_axis))
        x_axis = 10 if x_axis >= 550 else x_axis+45
    num = 0
    for x in word:
        num += 0.5
    startpoint = (screen_width/2) - (55 * num)
    for x in word:
        screen.blit(line, (startpoint, 470))
        if x.upper() in guessed_letters:
            font1 = pygame.font.Font(pygame.font.get_default_font(), 36)
            text1 = font1.render(x.upper(), True, (0,0,0))
            screen.blit(text1, (startpoint+15, 440))     
        startpoint += 55
    pygame.display.update()
    return

def draw_gameover_screen():
    screen.fill((255,255,255))
    screen.blit(background[guesses], (120, 100))
    x_axis = 10
    for x, val in enumerate(all_letters):
        y_axis = 20 if x < 13 else 70
        screen.blit(letters[x], (x_axis, y_axis))
        x_axis = 10 if x_axis >= 550 else x_axis+45
    num = 0
    for x in word:
        num += 0.5
    startpoint = (screen_width/2) - (55 * num)
    for x in word:
        screen.blit(line, (startpoint, 470))
        font1 = pygame.font.Font(pygame.font.get_default_font(), 36)
        text1 = font1.render(x.upper(), True, (0,0,0))
        screen.blit(text1, (startpoint+15, 440))   
        startpoint += 55
    font2 = pygame.font.Font(pygame.font.get_default_font(), 20)
    text2 = font2.render("(Press Enter to Play Again)", True, (0,0,0))
    screen.blit(text2, ((screen_width/2)-(text2.get_width()/2), 505)) 
    pygame.display.update()
    return 

game_running = True
while game_running:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            game_running = False
    if game_running == False:
        break
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gameover == False:
        position = pygame.mouse.get_pos()
        x_axis = [[10,55],[55,100],[100,145],[145,190],[190,235],[235,280],
                  [280,325],[325,370],[370,415],[405,460], [450,505],[495,550],[550,595]]
        for number, item in enumerate(x_axis):
            if (position[0] > item[0] and position[0] < item[1]):
                if position[1] > 20 and position[1] < 70:
                    guessed_letter = all_letters[number]
                elif position[1] > 70 and position[1] < 120:
                    guessed_letter = all_letters[number+13]
                else:
                    guessed_letter = None

        if guessed_letter and guessed_letter not in guessed_letters and guesses < 6:
            guessed_letters.append(guessed_letter)
            if guessed_letter in word.upper():
                pygame.mixer.Sound.play(right_answer_sound)  

    for x in guessed_letters:
        if x not in word.upper() and x not in missed_guesses:
            pygame.mixer.Sound.play(wrong_answer_sound)
            missed_guesses.append(x)
            guesses += 1
 
    for x in word:
        if x.upper() not in guessed_letters:
            gameover = False
            break
        else:
            gameover = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if gameover == True or guesses == 6:
            guesses = 0
            del guessed_letters[:]
            del missed_guesses[:]
            gameover = False
            word = random.sample(wordlist, len(wordlist))[0]
            
    if gameover or guesses == 6:
        draw_gameover_screen()
    else:
        redraw_screen()
