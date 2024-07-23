import pygame
import random
import time
import csv
import datetime as datetime

# variables used
num_practice_trials = 1
num_trials = 3

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((1200, 950))
pygame.display.set_caption("Pitch Identification Task")

# INSERT SOUND FILES FROM GITHUB HERE
sounds = {
    'V': pygame.mixer.Sound('/Users/taneeshkondapally/Desktop/File_A4.wav'), # INSERT LOWER PITCH HERE
    'B': pygame.mixer.Sound('/Users/taneeshkondapally/Desktop/File_A5.wav') # INSERT HIGHER PITCH HERE
}

# Mapping keys to pitches
key_pitch_map = {
    pygame.K_v: 'V',
    pygame.K_b: 'B'
}

# Function to log data
def log_data(ObjShowTime, ReactionTime, StimType, Guess, correct, filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ObjShowTime, ReactionTime, StimType, Guess, correct])
        
# Practice Round Correct/Incorrect function
def printCorrect(correctness):
    screen.fill((0,0,0))
    if correctness:
        correctnessSuper = font.render('Correct!', True, (255,255,255))
        screen.blit(correctnessSuper, (50, 300))
    else:
        falsenessSuper = font.render('Incorrect!', True, (255, 255, 255))
        screen.blit(falsenessSuper, (50, 300))
    pygame.display.flip()

# Instruction input function
def waitingFunction(keyPress):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == keyPress:
                waiting = False
    pygame.mixer.stop()

# Print Function
def printText(instructions):
    screen.fill((0,0,0))
    screen.blit(instructions, (50, 300))
    pygame.display.flip()
        
# Protocol function
def protocolFunction(trials):
    for trial in range(trials):
        time.sleep(random.uniform(1,3))
        # Plays random pitch
        pitch = random.choice(list(sounds.keys()))
        sounds[pitch].play()
        start_time = time.time()
        # Wait for response
        response = None
        correct = None
        responding = True
        # Take Data
        while responding:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    response_time = time.time()
                    response = event.key
                    if key_pitch_map.get(response) == pitch:
                        correct = True
                    else:
                        correct = False
                    responding = False
                    sounds[pitch].stop()
        # Do different things for practice and normal trials
        if trials == num_practice_trials:
            printCorrect(correct)
        else:
            log_data(start_time, response_time, pitch, key_pitch_map.get(response), correct, filename)

# receiving name of participant
font = pygame.font.Font(None, 36)
nameInstructions = font.render('Enter your name: ', True, (255, 255, 255))
printText(nameInstructions)

text = ''
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"Entered name: {text}")
                done = True
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode
filename = f"{text}.2SrtData.{datetime.datetime.now()}.csv"
# so that the file has the name of each participant

# Display instructions
instructionsTotal = font.render('Press V or B for the corresponding pitch. Press SPACE to start.', True, (255, 255, 255))
printText(instructionsTotal)
waitingFunction(pygame.K_SPACE)

instructions_key1 = font.render('This is Pitch 1. Press "V" for this pitch.', True, (255, 255, 255))
sounds['V'].play()
printText(instructions_key1)
waitingFunction(pygame.K_v)


instructions_key2 = font.render('This is Pitch 2. Press "B" for this pitch.', True, (255, 255, 255))
sounds['B'].play()
printText(instructions_key2)
waitingFunction(pygame.K_b)

# Practice rounds
instructions_practice = font.render('These are a few practice rounds to familiarize yourself', True, (255, 255, 255))
printText(instructions_practice)
protocolFunction(num_practice_trials)

# Begin experiment
log_data('ObjShowTime', 'ReactionTime', 'StimType', 'Guess', 'Correct', filename)
instructions_final = font.render("The pitches will play now!", True, (255,255,255))
printText(instructions_final)
protocolFunction(num_trials)

pygame.quit()

# End of the experiment
print(f"Experiment completed. Results are saved in {filename}")