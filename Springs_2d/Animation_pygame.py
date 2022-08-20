import numpy as np
import os
# Import and initialize the pygame library
import pygame, sys
pygame.init()

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#frames_num = 20

def sigmoid(x):
    return 1/(1 + np.exp(-x))


def play(osc_num, frames_num):
    
    # Set up the drawing window
    WIN_HIG = 800
    WIN_WID = 1200

    l_rest = 10

    scale_down = ( WIN_WID / (osc_num * l_rest * 1.1) ) 
    radius = (l_rest / 10) * scale_down * 2*sigmoid(osc_num)
    
    frames = np.empty([frames_num, osc_num])

    file_dir = ""
    if os.path.isfile("frame1.txt"):
        pass
    elif os.path.isfile("frames/frame1.txt"):
        file_dir = "frames/"


    for i in range(frames_num):
        file_name = file_dir + "frame" + str(i) + ".txt"
        with open(file_name, "r") as file:
            for line in file:
                line = line.split("\t")
                line.remove("")
                frame = np.zeros(osc_num)
                for j in range(len(line)):
                    frame[j] = float(line[j])
        frames[i] = frame

    # this is the location of the middle oscillator in t=0. Using it, we can center the "camera"
    mid_osc = frames[0][int(osc_num / 2)]
    mid_osc_even = (osc_num-1)*l_rest/2

    # Animation
    win = pygame.display.set_mode([WIN_WID, WIN_HIG])
    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()

    while running:
        count = 0
        for frame in frames:
            count += 1
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            clock.tick(20)

            win.fill(BLACK)
            for i in range(osc_num):
                if osc_num%2 == 0:
                    if i < osc_num-1:
                        pygame.draw.line(win, WHITE,
                                         (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2),
                                         (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i+1]), WIN_HIG / 2),
                                         1)

                    # Draw a solid circle
                    if i==1:
                        pygame.draw.circle(win, WHITE,
                                        (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius*1.1)
                        pygame.draw.circle(win, RED,
                                        (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius)
                    elif i==2:
                        pygame.draw.circle(win, WHITE,
                                        (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius*1.1)
                        pygame.draw.circle(win, GREEN,
                                        (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius)    
                    else:
                        pygame.draw.circle(win, WHITE,
                                        (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius*1.1)
                        pygame.draw.circle(win, BLUE,
                                        (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius)
                else:
                    if i < osc_num-1:
                        pygame.draw.line(win, WHITE,
                                         (WIN_WID/2 + scale_down*(-mid_osc + frame[i]), WIN_HIG / 2),
                                         (WIN_WID/2 + scale_down*(-mid_osc + frame[i+1]), WIN_HIG / 2),
                                         1)

                    # Draw a solid circle
                    pygame.draw.circle(win, WHITE,
                                       (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius*1.1)
                    pygame.draw.circle(win, BLUE,
                                       (WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2), radius)

            # Draw text: number of the frame
            font = pygame.font.SysFont(None, 72)
            img = font.render('Frame: ' + str(count), True, WHITE)
            win.blit(img, (20, 20))
            pygame.display.update()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    play()