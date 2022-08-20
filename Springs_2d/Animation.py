import numpy as np

# Import and initialize the pygame library
import pygame, sys
pygame.init()

# Set up the drawing window
WIN_HIG = 800
WIN_WID = 1000

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

frames_num = 1000
osc_num = 3


def play():
    frames = np.empty([frames_num, osc_num])

    for i in range(frames_num):
        file_name = "frame" + str(i) + ".txt"
        with open(file_name, "r") as file:
            for line in file:
                line = line.split("\t")
                line.remove("")
                frame = np.zeros(osc_num)
                for j in range(len(line)):
                    frame[j] = float(line[j])
        frames[i] = frame
    print(frames)

    # Animation
    win = pygame.display.set_mode([WIN_WID, WIN_HIG])
    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()
    while running:
        for frame in frames:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            clock.tick(20)

            win.fill(BLACK)
            for i in range(osc_num):
                # Draw a solid circle
                pygame.draw.circle(win, ((i + 1) * 20, (i + 1) * 30, (i + 1) * 30),
                                   (WIN_WID / 2 + frame[i], WIN_HIG / 2), 5)
            pygame.display.update()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    play()