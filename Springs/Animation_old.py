import time

import numpy as np
import os
from math import *
# Import and initialize the pygame library
import pygame, sys

# colors
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
ref_win = pygame.display.set_mode([WIN_WID, WIN_HIG])
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
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        ref_win.blit(self.surface, (self.x, self.y))

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


class ButtonsZoom:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, pos, font=FONT, colors=[COLOR3, COLOR4]):
        self.font = pygame.font.SysFont("Arial", font)
        self.colors = colors
        self.text_p = self.font.render("+", 1, pygame.Color("White"))
        self.text_m = self.font.render("-", 1, pygame.Color("White"))
        self.size_p = self.text_p.get_size()
        self.size_m = self.text_m.get_size()
        self.surface_p = pygame.Surface(self.size_p)
        self.surface_m = pygame.Surface(self.size_m)

        self.surface_p.fill(self.colors[0])
        self.surface_m.fill(self.colors[1])
        self.surface_p.blit(self.text_p, (0, 0))
        self.surface_m.blit(self.text_m, (0, 0))
        self.x_p, self.y_p = pos
        self.x_m, self.y_m = [pos[0], pos[1] + self.size_p[1]]
        self.rect_p = pygame.Rect(self.x_p, self.y_p, self.size_p[0], self.size_p[1])
        self.rect_m = pygame.Rect(self.x_m, self.y_m, self.size_m[0], self.size_m[1])
        self.pressed_p = 0
        self.pressed_m = 0

    def show(self):
        ref_win.blit(self.surface_p, (self.x_p, self.y_p))
        ref_win.blit(self.surface_m, (self.x_m, self.y_m))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect_p.collidepoint(x, y):
                    self.pressed_p = 1
                elif self.rect_m.collidepoint(x, y):
                    self.pressed_m = 1


def cyclic_index(i, N):
    if i == N:
        return 0
    else:
        return i


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def find_default(paths):
    found, file_dir, files_or_file = False, None, None
    # if os.path.isfile("frame0.txt"):
    if os.path.isfile(paths[0]):
        print(0)
        if os.path.isfile(f"frame1.txt"):
            files_or_file = "files"
        else:
            files_or_file = "file"
        file_dir = ""
        found = True

    # elif os.path.isfile("frames/frame0.txt"):
    elif os.path.isfile(paths[2]):
        print(2)
        if os.path.isfile("frames/frame1.txt"):
            files_or_file = "files"
        else:
            files_or_file = "file"
        file_dir = "frames/"
        found = True

    # elif os.path.isfile("frames.txt"):
    elif os.path.isfile(paths[1]):
        print(1)
        file_dir = ""
        files_or_file = "file"
        found = True
    # elif os.path.isfile("frames/frames.txt"):
    elif os.path.isfile(paths[3]):
        print(3)
        file_dir = "frames/"
        files_or_file = "file"
        found = True
    return found, file_dir, files_or_file


def find_files():
    paths = ["frame0.txt", "frames.txt", "frames/frame0.txt", "frames/frames.txt"]
    options = [os.path.isfile(path) for path in paths]
    files_or_file, file_dir = None, None
    found = False

    if options.count(True) > 1:
        print('\n!!! There are more than one "frame_.txt" files in this directory and/or its subdirectories !!!\n')
    elif options.count(True) == 1:
        found, file_dir, files_or_file = find_default(paths)
    else:
        print('\n!!! No "frame_.txt or frames.txt were find in this directory. !!!')
        print('Make sure your "frames" files are located at the same directory as this code of the animation.\n')

    tries = 0
    while not found:
        if tries > 1:
            print(f"\nNo frame file/directory was found. Name of directory given is:  {file_dir}\n")
        file_dir = input('\nWrite name of the "frames" directory (or stop the program and fix the issue): ')
        if "/" not in file_dir and file_dir != "":
            file_dir += "/"
        tries += 1

        if os.path.isfile(f"{file_dir}frame1.txt"):
            if os.path.isfile(f"{file_dir}frame2.txt"):
                files_or_file = "files"
            else:
                files_or_file = "file"
            found = True

        elif os.path.isfile(f"{file_dir}frames.txt"):
            files_or_file = "file"
            found = True

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
    print(files_or_file, file_dir)
    if files_or_file == "files":
        frames_n = check_files_num(file_dir)
        done = False
        i = 0
        while not done:
            file_name = file_dir + "frame" + str(i) + ".txt"
            if os.path.isfile(file_name):
                with open(file_name, "r") as file:
                    for count, line in enumerate(file):
                        found_space = ""
                        for space in ["\t", " "]:
                            if space in line:
                                line = line.split(space)
                                found_space = space
                                break

                        if not found_space:
                            print("files format is invalid. Read the instruction or mail the instructor.")
                            frames, frames_n, osc_n = None, None, None
                            break

                        for k in range(len(line)):
                            line[k] = line[k].strip()

                        while '' in line:
                            line.remove('')

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
                    ref_win.fill(BLACK)
                    ref_win.blit(text_img, (int(WIN_WID / 4), int(WIN_HIG / 2)))
                    print(text)
                i += 1
                pygame.display.update()

            else:
                text = "Done!"
                done = True
                ont = pygame.font.SysFont(None, 72)
                text_img = font.render(text, True, WHITE)
                ref_win.fill(BLACK)
                ref_win.blit(text_img, (int(WIN_WID / 4), int(WIN_HIG / 2)))
                print(text)

    elif files_or_file == "file":
        file_name = file_dir + "frames.txt"
        i = 0
        if not os.path.isfile(file_name):
            file_name = file_dir + "frame1.txt"
            if not os.path.isfile(file_name):
                print("File's name is invalid.\n Read the instruction or mail the instructor.")
                frames, frames_n, osc_n = None, None, None

        with open(file_name, "r") as file:
            for count, line in enumerate(file):
                found_space = ""
                for space in ["\t", " "]:
                    if space in line:
                        line = line.split(space)
                        found_space = space
                        break

                if not found_space:
                    print("files format is invalid. Read the instruction or mail the instructor.")
                    frames, frames_n, osc_n = None, None, None
                    break

                for i in range(len(line)):
                    line[i] = line[i].strip()

                while '' in line:
                    line.remove('')
                osc_n = len(line)
                frame = np.array(line, dtype=float)
                if count == 0:
                    frames = np.array([frame])
                else:
                    frames = np.append(frames, [frame], axis=0)
            frames_n = count + 1

    else:
        frames, frames_n, osc_n = None, None, None

    return frames, frames_n, osc_n


def began_movement(x, x_prev):
    began_moving = False
    if x - x_prev != 0:
        began_moving = True
    return began_moving


def color_circles(i, j, frames, RADIUS):
    # This function colors the circle in red if its moving, and blue otherwise
    line_color = WHITE
    fill_color = RED
    radius = RADIUS
    osc_n = len(frames.T[:])

    # If a particle begins to move it becomes red
    frame_now = frames[j][i]
    frame_previous = frames[j - 1][i]
    if j > 0 and began_movement(frame_now, frame_previous):
        vel = 0.5 * abs(frame_now - frame_previous) + 0.5
        if vel > 1:
            vel = 1
        line_color = WHITE
        fill_color = ((1 - vel) * 255, 0, vel * 255)
        if osc_n >= 200:
            radius = RADIUS * 1.1
    return line_color, fill_color, radius


def play():
    l_rest = 10
    frames, frames_num, osc_num = read_files()
    win = pygame.display.set_mode([WIN_WID, WIN_HIG])

    # The if condition checks if these variables are not None. If one of them is None, that means there was an issue.
    if frames_num and osc_num:
        print(f"Number of frames is: {frames_num}")
        print(f"Number of oscillators is: {osc_num}")
        scale_down = (WIN_WID / (osc_num * l_rest * 1.1)) * (1 + tanh(WIN_WID / 10000))
        RADIUS = (l_rest / 10) * scale_down * 2 * sigmoid(osc_num)

        # this is the location of the middle oscillator in t=0. Using it, we can center the "camera"
        mid_osc = frames[0][int(osc_num / 2)]
        mid_osc_even = (osc_num - 1) * l_rest / 2

        # Run until the user asks to quit
        running = True

        play_button = Button((100, 100), click_states=["play", "pause"], font=50)
        speed_button = Button((500, 100), click_states=[1, 2, 3, 4], font=50)
        zoom_buttons = ButtonsZoom([200, 600], font=50)
        restart_button = Button((700, 100), click_states=["play", "restart"], font=50)
        restart_button.change_text("restart", COLOR2)

        speeds1 = [500, 1000, 2000, 4000]
        speeds2 = [100, 200, 400, 800]

        # From here on I was very lazy :)
        # These are some calculations considering animating different cases of the chain

        # For greater numbers of oscillators drawing the full chain
        # inside of the animation window (properly) becomes a real issue.
        if osc_num >= 200 and osc_num < 300:
            extra_displacement = 0.2 * osc_num
            extra_length = 0.1 * (frames[0][1] - frames[0][0])
            RADIUS *= 2.5
        elif osc_num >= 300:
            extra_displacement = 0
            extra_length = 5 * (frames[0][1] - frames[0][0])
            RADIUS *= 20
        elif osc_num > 15:
            extra_displacement = 5 * osc_num
            extra_length = 0.1 * (frames[0][1] - frames[0][0])
            # extra_length = 0
        else:
            extra_displacement = 0
            extra_length = 0

        while running:
            j = 0
            while j < frames_num:
                # This is a specific frame, which is a list of all the oscillators coordinates
                oscillators = frames[j]

                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()
                    play_button.click(event)
                    speed_button.click(event)
                    restart_button.click(event)
                    zoom_buttons.click(event)
                if restart_button.click_state == "restart":
                    restart_button.set_state("play")
                    restart_button.change_text("restart", COLOR2)
                    j = 0

                elif zoom_buttons.pressed_p:
                    print("+")
                    print(win.get_rect().size)
                    pygame.transform.scale(ref_win, win.get_rect().size)
                    zoom_buttons.pressed_p = 0
                elif zoom_buttons.pressed_m:
                    print("-")
                    pygame.transform.scale(ref_win, win.get_rect().size)
                    zoom_buttons.pressed_m = 0

                if frames_num < 500:
                    speed = speeds1[speed_button.click_state - 1]
                else:
                    speed = speeds2[speed_button.click_state - 1]
                ticking = int(speed * (tanh(frames_num / 4000)))
                clock.tick(ticking)

                ref_win.fill(BLACK)
                for i in range(osc_num):
                    if osc_num % 2 == 0:
                        line_color, fill_color, radius = color_circles(i, j, frames, RADIUS)
                        # Draw lines as connecting springs
                        if i < osc_num - 1 and osc_num < 200:
                            pygame.draw.line(ref_win, WHITE,
                                             (extra_displacement + WIN_WID / 2 + scale_down * (
                                                         - mid_osc_even + oscillators[i]), WIN_HIG / 2),
                                             (extra_displacement + WIN_WID / 2 + scale_down * (
                                                         - mid_osc_even + oscillators[i + 1]) + i * extra_length,
                                              WIN_HIG / 2),
                                             1)

                        # Draw a solid circle
                        circle_pos = (extra_displacement + WIN_WID / 2 + scale_down * (
                                    - mid_osc_even + oscillators[i]) + i * extra_length, WIN_HIG / 2)
                        pygame.draw.circle(ref_win, line_color,
                                           circle_pos, radius * 1.1)
                        pygame.draw.circle(ref_win, fill_color,
                                           circle_pos, radius)
                        if i%10==0:
                            font = pygame.font.SysFont(None, int(400/sqrt(osc_num)))
                            text_img = font.render(f"{i}", True, WHITE)
                            ref_win.blit(text_img, (circle_pos[0], circle_pos[1] + 10))
                    else:
                        line_color, fill_color, radius = color_circles(i, j, frames, RADIUS)

                        if i < osc_num - 1 and osc_num < 200:
                            pygame.draw.line(ref_win, WHITE,
                                             (extra_displacement + WIN_WID / 2 + scale_down * (
                                                         -mid_osc + oscillators[i]), WIN_HIG / 2),
                                             (extra_displacement + WIN_WID / 2 + scale_down * (
                                                         -mid_osc + oscillators[i + 1]) + i * extra_length,
                                              WIN_HIG / 2),
                                             1)

                        # Draw a solid circle
                        circle_pos = (extra_displacement + WIN_WID / 2 + scale_down * (
                                      - mid_osc_even + oscillators[i]) + i * extra_length, WIN_HIG / 2)
                        pygame.draw.circle(ref_win, line_color,
                                           circle_pos, RADIUS * 1.1)

                        pygame.draw.circle(ref_win, fill_color,
                                           circle_pos, RADIUS)
                        if i%10==0:
                            font = pygame.font.SysFont(None, int(400/sqrt(osc_num)))
                            text_img = font.render(f"{i}", True, WHITE)
                            ref_win.blit(text_img, (circle_pos[0], circle_pos[1] + 10))

                # Draw text: number of the frame
                font = pygame.font.SysFont(None, 72)
                img = font.render('Frame: ' + str(j), True, WHITE)
                ref_win.blit(img, (20, 20))

                # Draw text: speed
                font = pygame.font.SysFont(None, 72)
                img = font.render('Speed: ', True, WHITE)
                ref_win.blit(img, (300, 100))

                play_button.show()
                speed_button.show()
                restart_button.show()
                zoom_buttons.show()

                win.blit(ref_win, (0, 0))
                pygame.display.update()

                while play_button.click_state == "pause":

                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        play_button.click(event)

                    pygame.display.update()
                    clock.tick(10)

                j += 1
    else:
        print("The program did not run.")

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    play()
