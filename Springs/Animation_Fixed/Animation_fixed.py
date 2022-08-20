
import time
import numpy as np
import os
from math import *
# Import and initialize the pygame library
import pygame, sys

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COLOR1 = (80, 100, 80)
COLOR2 = (120, 50, 80)
COLOR3 = (100, 0, 50)
COLOR4 = (120, 0, 20)

# Set up the drawing window
WIN_HIG = 800
WIN_WID = 1400

# Animation
pygame.init()
win = pygame.display.set_mode([WIN_WID, WIN_HIG])
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, pos, click_states, font=FONT, colors=[COLOR1, COLOR2, COLOR3, COLOR4]):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.click_states = click_states
        self.click_state = self.click_states[0]
        self.ind = 0
        self.colors = colors
        self.change_text(str(self.click_states[0]), colors[0])

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        # self.surface.fill(bg)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        win.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.next_state()

    def next_state(self):
        N = len(self.click_states)
        self.ind = cyclic_index(self.ind + 1, N)
        self.click_state = self.click_states[self.ind]
        self.change_text(str(self.click_state), bg=self.colors[self.ind])

    def set_state(self, state_name):
        self.ind = self.click_states.index(state_name)
        self.click_state = self.click_states[self.ind]
        self.change_text(str(self.click_state), bg=self.colors[self.ind])


def cyclic_index(i, N):
    if i == N:
        return 0
    else:
        return i


def sigmoid(x):
    return 1/(1 + np.exp(-x))


def find_files():
    if os.path.isfile("frame1.txt"):
        file_dir = ""
        files_or_file = "files"
    elif os.path.isfile("frames/frame1.txt"):
        file_dir = "frames/"
        files_or_file = "files"
    elif os.path.isfile("frames.txt"):
        file_dir = ""
        files_or_file = "file"
    else:
        print('\n\n!!! No "frame_.txt or frames.txt were find in this directory. !!!')
        print('Make sure your "frames" files are located at the same directory as this code of the animation.\n\n')
        files_or_file, file_dir = None, None
    return files_or_file, file_dir


def check_files_num(file_dir):
    done = False
    i = 0
    while not done:
        file_name = file_dir + "frame" + str(i) + ".txt"
        if os.path.isfile(file_name):
            i += 1
        else:
            done = True

    return i


def read_files():
    files_or_file, file_dir = find_files()
    if files_or_file == "files":
        frames_n = check_files_num(file_dir)
        done = False
        i = 0
        while not done:
            file_name = file_dir + "frame" + str(i) + ".txt"
            if os.path.isfile(file_name):
                with open(file_name, "r") as file:
                    for count, line in enumerate(file):
                        line = line.split("\t")
                        line.remove("")
                        osc_n = len(line)
                        frame = np.array(line, dtype=float)
                    if i == 0:
                        frames = np.array([frame])
                    else:
                        frames = np.append(frames, [frame], axis=0)
                if i % 1000 == 0:
                    text = f"{i}/{frames_n} files have been read"
                    font = pygame.font.SysFont(None, 72)
                    text_img = font.render(text, True, WHITE)
                    win.fill(BLACK)
                    win.blit(text_img, (int(WIN_WID/4), int(WIN_HIG/2)))
                    print(text)
                i += 1
                pygame.display.update()
            else:
                text = "Done!"
                done = True
                ont = pygame.font.SysFont(None, 72)
                text_img = font.render(text, True, WHITE)
                win.fill(BLACK)
                win.blit(text_img, (int(WIN_WID / 4), int(WIN_HIG / 2)))
                print(text)

    elif files_or_file == "file":
        file_name = file_dir + "frames.txt"
        i = 0
        if os.path.isfile(file_name):
            with open(file_name, "r") as file:
                for count, line in enumerate(file):
                    line = line.split("\t")
                    line.remove("")
                    osc_n = len(line)
                    frame = np.array(line, dtype=float)
                    if count == 0:
                        frames = np.array([frame])
                    else:
                        frames = np.append(frames, [frame], axis=0)
    else:
        frames, frames_n, osc_n = None, None, None

    return frames, frames_n, osc_n


def began_movement(x, x_prev):
    began_moving = False
    if x-x_prev != 0:
        began_moving = True
    return began_moving


def color_circles(i, j, frames, RADIUS):
    line_color = WHITE
    fill_color = BLUE
    radius = RADIUS
    osc_n = len(frames.T[:])
    if osc_n >= 20:
        # If a particle begins to move it becomes red
        # THIS IS TO DEBUG THE BROKEN CODE  
        #print ("j:",j)
        #print ("i:",i)
        #sys.stdin.read(1)
        if j > 0 and began_movement(frames[j][i], frames[j - 1][i]):
            line_color = WHITE
            fill_color = RED
            if osc_n >= 200:
                radius = RADIUS * 1.1
    return line_color, fill_color, radius


def play():

    l_rest = 10
    frames, frames_num, osc_num = read_files()

    # The if condition checks if these variables are not None. If one of them is None, that means there was an issue.
    if frames_num and osc_num:
        print(f"Number of frames is: {frames_num}")
        print(f"Number of oscillators is: {osc_num}")
        scale_down = ( WIN_WID / (osc_num * l_rest * 1.1) )*(1 + tanh(WIN_WID/10000))
        RADIUS = (l_rest / 10) * scale_down * 2*sigmoid(osc_num)

        # this is the location of the middle oscillator in t=0. Using it, we can center the "camera"
        mid_osc = frames[0][int(osc_num / 2)]
        mid_osc_even = (osc_num-1)*l_rest/2

        # Run until the user asks to quit
        running = True

        play_button = Button((100, 100), click_states=["play", "pause"], font=50)
        speed_button = Button((500, 100), click_states=[1, 2, 3, 4], font=50)
        restart_button = Button((700, 100), click_states=["play", "restart"], font=50)
        restart_button.change_text("restart", COLOR2)

        speeds1 = [500, 1000, 2000, 4000]
        speeds2 = [100, 200, 400, 800]

        if osc_num > 200:
            extra_displacment = 0.5*osc_num
            extra_length = 0.1*(frames[0][1] - frames[0][0])
            RADIUS *= 2.5
        elif osc_num > 15:
            extra_displacment = 5*osc_num
            extra_length = 0.1 * (frames[0][1] - frames[0][0])
            # extra_length = 0
        else:
            extra_displacment = 0
            extra_length = 0
        print(extra_length)
        while running:
            j = 0
            while j < frames_num:
                frame = frames[j]
                # IS THIS INTENTIONAL BUG to FORCE ME TO DEBUG AND UNDERSTAND THE CODE??
                # j += 1
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    play_button.click(event)
                    speed_button.click(event)
                    restart_button.click(event)
                if restart_button.click_state == "restart":
                    restart_button.set_state("play")
                    restart_button.change_text("restart", COLOR2)
                    j = 0

                if frames_num < 500:
                    speed = speeds1[speed_button.click_state-1]
                else:
                    speed = speeds2[speed_button.click_state-1]
                ticking = int(speed * (tanh(frames_num / 4000)))
                clock.tick(ticking)

                win.fill(BLACK)
                # THIS IS TO DEBUG THE BROKEN CODE
                #print (osc_num)
                #print (frames)
                #sys.stdin.read(1)
                for i in range(osc_num):
                    if osc_num % 2 == 0:
                        line_color, fill_color, radius = color_circles(i, j, frames, RADIUS)

                        # Draw lines as connecting springs
                        if i < osc_num-1:
                            pygame.draw.line(win, WHITE,
                                             (extra_displacment + WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]), WIN_HIG / 2),
                                             (extra_displacment + WIN_WID/2 + scale_down*(- mid_osc_even + frame[i+1]) + i*extra_length, WIN_HIG / 2),
                                             1)

                        # Draw a solid circle
                        pygame.draw.circle(win, line_color,
                                        (extra_displacment + WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]) + i*extra_length, WIN_HIG / 2), radius*1.1)
                        pygame.draw.circle(win, fill_color,
                                        (extra_displacment + WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]) + i*extra_length, WIN_HIG / 2), radius)
                    else:
                        line_color, fill_color, radius = color_circles(i, j, frames, RADIUS)

                        if i < osc_num-1:
                            pygame.draw.line(win, WHITE,
                                             (extra_displacment + WIN_WID/2 + scale_down*(-mid_osc + frame[i]), WIN_HIG / 2),
                                             (extra_displacment + WIN_WID/2 + scale_down*(-mid_osc + frame[i+1]) + i*extra_length, WIN_HIG / 2),
                                             1)

                        # Draw a solid circle
                        pygame.draw.circle(win, line_color,
                                           (extra_displacment + WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]) + i*extra_length, WIN_HIG / 2), RADIUS*1.1)

                        pygame.draw.circle(win, fill_color,
                                           (extra_displacment + WIN_WID/2 + scale_down*(- mid_osc_even + frame[i]) + i*extra_length, WIN_HIG / 2), RADIUS)

                # Draw text: number of the frame
                font = pygame.font.SysFont(None, 72)
                img = font.render('Frame: ' + str(j), True, WHITE)
                win.blit(img, (20, 20))

                # Draw text: speed
                font = pygame.font.SysFont(None, 72)
                img = font.render('Speed: ', True, WHITE)
                win.blit(img, (300, 100))

                play_button.show()
                speed_button.show()
                restart_button.show()
                pygame.display.update()

                while play_button.click_state == "pause":

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        play_button.click(event)

                    pygame.display.update()
                    clock.tick(10)

                # j, the frame iterator, should be advanced at the end of the " while j < frames_num: " loop  
                j += 1
    else:
        print("The program did not run.")

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    play()
