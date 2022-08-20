import time

import numpy as np
import os
from math import *
# Import and initialize the pygame library
import pygame, sys

''' These are the names of the input files the program will read '''
initState_name = "input_initState1.json"
parameters_name = "input_parameters1.json"

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
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 50)


class Osc:
    def __init__(self, pos, osc_num, radius=10, fill_color=RED, line_color=WHITE):
        self.pos = pos
        self.osc_num = osc_num
        self.previous_pos = pos.copy()
        self.radius = radius
        self.fill_color = fill_color
        self.line_color = line_color
        self.vel = 0

    def updateVel(self):
        self.vel = abs(self.pos[0] - self.previous_pos[0])

    def colorByVel(self, max_vel):
        # This method colors the circle according to the size of its velocity
        if self.vel > 10**(-6):
            color_scale = (abs(self.vel)/max_vel)
            if color_scale > 1:
                color_scale = 1
            self.fill_color = ((1 - color_scale) * 255, 0*color_scale * 255, color_scale * 255)
        else:
            self.fill_color = RED

    def drawCircle(self, win):
        pygame.draw.circle(win, self.line_color, self.pos, self.radius*1.1)
        pygame.draw.circle(win, self.fill_color, self.pos, self.radius)


class ButtonOfStates:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, pos, click_states, font=50, colors=None):
        if colors is None:
            colors = [COLOR1, COLOR2, COLOR3, COLOR4]
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.click_states = click_states
        self.click_state = self.click_states[0]
        self.ind = 0
        self.colors = colors
        self.text = self.font.render("", 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.change_text(str(self.click_states[0]), colors[0])

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, win):
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


class ButtonsZoom:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, pos, font=50, colors=None):
        if colors is None:
            colors = [COLOR3, COLOR4]
        self.font = pygame.font.SysFont("Arial", font)
        self.colors = colors
        self.text_p = self.font.render("+", 1, pygame.Color("White"))
        self.text_m = self.font.render("-", 1, pygame.Color("White"))
        self.size_p = [40, 60]
        self.size_m = [40, 60]
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
        self.scale_occur = 0

    def show(self, win):
        win.blit(self.surface_p, (self.x_p, self.y_p))
        win.blit(self.surface_m, (self.x_m, self.y_m))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect_p.collidepoint(x, y):
                    self.pressed_p = 1
                elif self.rect_m.collidepoint(x, y):
                    self.pressed_m = 1
        elif pygame.key.get_pressed()[pygame.K_KP_PLUS]:
            self.pressed_p = 1
        elif pygame.key.get_pressed()[pygame.K_KP_MINUS]:
            self.pressed_m = 1


class KeyBoard:
    def __init__(self):
        self.keyboard_input = ''


class Text:
    def __init__(self, pos, text="default_text", font=50, color=WHITE):
        self.pos = pos
        self.text = text
        self.font = pygame.font.SysFont("Arial", font)
        self.color = color

    def print_to(self, win):
        text_img = self.font.render(self.text, True, self.color)
        win.blit(text_img, self.pos)


class Run:
    def __init__(self, isRunning, ticking=10, scale=1):
        self.isRunning = isRunning
        self.ticking = ticking
        self.scale = scale


def cyclic_index(i, N):
    if i == N:
        return 0
    else:
        return i


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def find_default(paths):
    found, file_dir, files_or_file = False, None, None

    if os.path.isfile(paths[0]):
        print(0)
        if os.path.isfile("frame1.txt"):
            files_or_file = "files"
        else:
            files_or_file = "file"
        file_dir = ""
        found = True

    elif os.path.isfile(paths[2]):
        print(2)
        if os.path.isfile("frames/frame1.txt"):
            files_or_file = "files"
        else:
            files_or_file = "file"
        file_dir = "frames/"
        found = True

    elif os.path.isfile(paths[1]):
        print(1)
        file_dir = ""
        files_or_file = "file"
        found = True

    elif os.path.isfile(paths[3]):
        print(3)
        file_dir = "frames/"
        files_or_file = "file"
        found = True
    return found, file_dir, files_or_file


def find_files():
    """ This function finds the file/files of the frame within current directory """

    # Set default options
    file_names = ["frame0.txt", "frames.txt"]
    default_paths = [file_names[0], file_names[1], f"frames/{file_names[0]}", f"frames/{file_names[1]}"]
    options = [os.path.isfile(path) for path in default_paths]

    # Set default parameters (the names are self explanatory)
    files_or_file, file_dir, file_name = None, None, None
    found = False

    # Consider some options, and print error messages accordingly
    if options.count(True) > 1:
        print('\n!!! There are more than one "frame_.txt" files in this directory and/or its subdirectories !!!\n')
    elif options.count(True) == 1:
        found, file_dir, files_or_file = find_default(default_paths)
        if files_or_file == "files":
            file_name = file_names[0]
        elif files_or_file == "file":
            file_name = file_names[1]
    else:
        print('\n!!! No "frame_.txt or frames.txt were find in this directory. !!!')
        print('Make sure your "frames" files are located at the same directory as this code of the animation.\n')

    tries = 0
    while not found:
        if tries > 1:
            print(f"\nNo frame file/directory was found. Name of directory given is:  {file_dir}\n")

        file_name = input('\nWrite name of the "frames" file (or stop the program and fix the issue): ')
        if ".txt" not in file_name:
            file_name += ".txt"

        if file_name != "":
            if os.path.isfile(file_name):
                files_or_file = "file"
                file_dir = ""
                break
            else:
                print('\nFile not found in current directory.')
                answer = input('\nIs the file located in another directory? (y/n): ')
                yes_options = ["y", "Y", "yes", "Yes"]
                no_options = ["n", "N", "n", "No"]
                if answer in yes_options:
                    file_dir = input('\nWrite name of the "frames" directory: ')
                elif answer in no_options:
                    print("\nFix file's name (or stop the program and fix the issue).")
                else:
                    print("\nInvalid answer.")

                if (answer in yes_options) and (file_dir != ""):
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
                elif (answer in yes_options) and (file_dir == ""):
                    print('\nNo input was given')
                else:
                    pass
        else:
            print('\nNo input was given')

    return files_or_file, file_dir, file_name


def check_files_num(file_dir):
    done = False
    i = 0
    while not done:
        file_path = f"{file_dir}frame{i}.txt"
        if os.path.isfile(file_path):
            i += 1
        else:
            done = True

    return i


def read_files(win):
    files_or_file, file_dir, file_name = find_files()
    if file_dir == "":
        print(f"Method: {files_or_file}\n", f"Directory: Current dir\n", f"Name of file/first file: {file_name}\n")
    else:
        print(f"Method: {files_or_file}\n", f"Directory: {file_dir}\n", f"Name of file/first file: {file_name}\n")

    if files_or_file == "files":
        frames_n = check_files_num(file_dir)
        done = False
        i = 0
        while not done:
            file_path = f"{file_dir}frame{i}.txt"
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
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

                massage = Text([int(WIN_WID / 4), int(WIN_HIG / 2)], f"0/{frames_n} files have been read")
                if i % 1000 == 0:
                    massage.text = f"{i}/{frames_n} files have been read"
                    win.fill(BLACK)
                    massage.print_to(win)
                    print(massage.text)
                i += 1
                pygame.display.update()

            else:
                massage.text = "Done!"
                massage.print_to(win)
                print(massage.text)
                done = True

    elif files_or_file == "file":
        file_path = f"{file_dir}{file_name}"
        i = 0
        if not os.path.isfile(file_path):
            file_path = file_dir + "frame1.txt"
            if not os.path.isfile(file_path):
                print("File's name is invalid.\n Read the instruction or mail the instructor.")
                frames, frames_n, osc_n = None, None, None
        else:
            massage = Text([int(WIN_WID / 4), int(WIN_HIG / 2)], "")
            with open(file_path, "r") as file:
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

                    # Print massage while waiting for upload
                    if count % 100 == 0:
                        massage.text = f"{count} lines have been read"
                        win.fill(BLACK)
                        massage.print_to(win)
                        print(massage.text)
                    pygame.display.update()

                massage.text = "Done!"
                massage.print_to(win)
                print(massage.text)
                frames_n = count + 1

    else:
        frames, frames_n, osc_n = None, None, None

    return frames, frames_n, osc_n


def get_input_arrows():
    left = pygame.key.get_pressed()[pygame.K_LEFT]
    right = pygame.key.get_pressed()[pygame.K_RIGHT]
    up = pygame.key.get_pressed()[pygame.K_UP]
    down = pygame.key.get_pressed()[pygame.K_DOWN]
    return left, right, up, down


def checkUserAction(run, play_button, speed_button, restart_button, zoom_buttons, keyboard):
    for event in pygame.event.get():
        # Did the user click the window close button?
        if event.type == pygame.QUIT:
            run.isRunning = False
            pygame.quit()
            sys.exit()
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            keyboard.keyboard_input = "left"
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            keyboard.keyboard_input = "right"
        elif pygame.key.get_pressed()[pygame.K_UP]:
            keyboard.keyboard_input = "up"
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            keyboard.keyboard_input = "down"

        # checks if user clicked on any of these keys
        play_button.click(event)
        speed_button.click(event)
        restart_button.click(event)
        zoom_buttons.click(event)


def screen_translations(win_position, keyboard):
    if keyboard.keyboard_input == 'left':
        win_position[0] -= 20
    elif keyboard.keyboard_input == 'right':
        win_position[0] += 20
    elif keyboard.keyboard_input == 'up':
        win_position[1] -= 20
    elif keyboard.keyboard_input == 'down':
        win_position[1] += 20
    keyboard.keyboard_input = ''


def play():
    main_win = pygame.display.set_mode([WIN_WID, WIN_HIG])
    ref_win = pygame.display.set_mode([WIN_WID, WIN_HIG])
    ref_win_position = [0, 0]
    # Set initial window width and height
    win_wid = WIN_WID
    win_hig = WIN_HIG
    frames, frames_num, osc_num = read_files(ref_win)

    # The if condition checks if these variables are not None. If one of them is None, that means there was an issue.
    if frames_num and osc_num:
        print(f"Number of frames is: {frames_num}")
        print(f"Number of oscillators is: {osc_num}")

        # Calculate initial scale of the chain to the window
        l_rest = 10
        if osc_num*l_rest < WIN_WID:
            init_scaleUp = WIN_WID/(osc_num*l_rest) * sigmoid(osc_num)
            init_scaleDown = 0.95
            RADIUS = 1.2*init_scaleUp
        else:
            init_scaleUp = 20 * sigmoid(osc_num)
            init_scaleDown = 1
            RADIUS = 2*init_scaleUp

        frames = np.array(frames)

        # Scale to window
        frames *= init_scaleUp

        # Set the middle of the chain to be the center
        mid_chain = frames[0][int(osc_num/2 - 1)] + 0.5 * abs(frames[0][int(osc_num / 2)] - frames[0][int(osc_num / 2 - 1)])
        frames -= mid_chain - l_rest

        # Arbitrary scale down the chain a bit
        frames *= init_scaleDown

        #  Calculate MAX_DIFF
        frames_diff = [frames.T[int(osc_num / 2)][n + 1] - frames.T[int(osc_num / 2)][n] for n in range(frames_num-1)]
        MAX_DIFF = np.max(frames_diff)

        # Set oscillators objects
        oscillators = [Osc([frames[0][n], win_hig/2], n, radius=RADIUS) for n in range(osc_num)]

        # Set buttons objects
        play_button = ButtonOfStates((100, 100), click_states=["play", "pause"], font=50)
        speed_button = ButtonOfStates((500, 100), click_states=[1, 2, 3, 4], font=50)
        restart_button = ButtonOfStates((700, 100), click_states=["play", "restart"], font=50)
        restart_button.change_text("restart", COLOR2)
        zoom_buttons = ButtonsZoom([win_wid-100, win_hig-200], font=50)

        keyboard = KeyBoard()

        # set different speeds of the animation
        speeds1 = [500, 1000, 2000, 4000]
        speeds2 = [100, 200, 400, 800]

        # Set texts objects
        num_of_frame = Text([20, 20], "Frame: 0", font=50)
        speed_frame = Text([300, 100], f"Speed: ", font=50)
        arrows_text = Text([600, 700], f"Use the arrow keys to move the center", font=25)
        osc_nums_text = [Text([frames[0][n], win_hig/2+RADIUS*1.5], f"{n}", font=16) for n in range(osc_num)]

        # Run until the user asks to quit
        run = Run(isRunning=True)
        while run.isRunning:

            # Running on frame index.
            # (Used a while loop to be able to reset j back to 0 inside the loop)
            frame_i = 0
            while frame_i < frames_num:

                # At each frame we set the screen to completely black
                main_win.fill(BLACK)
                # main_win.fill(WHITE)
                ref_win.fill(BLACK)

                # Draw text
                num_of_frame.text = f"Frame: {frame_i}"
                num_of_frame.print_to(ref_win)
                speed_frame.print_to(ref_win)
                arrows_text.print_to(ref_win)

                # Show buttons on screen
                play_button.show(ref_win)
                speed_button.show(ref_win)
                restart_button.show(ref_win)
                zoom_buttons.show(ref_win)

                # Check the user action - quit or press a button
                checkUserAction(run, play_button, speed_button, restart_button, zoom_buttons, keyboard)

                if restart_button.click_state == "restart":
                    restart_button.set_state("play")
                    restart_button.change_text("restart", COLOR2)
                    frame_i = 0

                # Set speed of animation
                if frames_num < 500:
                    speed = speeds1[speed_button.click_state - 1]
                else:
                    speed = speeds2[speed_button.click_state - 1]

                run.ticking = int(speed * (tanh(frames_num / 4000)))
                clock.tick(run.ticking)

                # Set scale of animation
                if zoom_buttons.pressed_p:
                    zoom_buttons.pressed_p = 0
                    zoom_buttons.scale_occur = 1
                    run.scale = 1.1

                if zoom_buttons.pressed_m:
                    zoom_buttons.pressed_m = 0
                    zoom_buttons.scale_occur = 1
                    run.scale = 0.9

                if zoom_buttons.scale_occur:
                    zoom_buttons.scale_occur = 0
                    frames *= run.scale
                    RADIUS *= run.scale

                screen_translations(ref_win_position, keyboard)

                # Update the oscillators positions and draw them
                for n, osc in enumerate(oscillators):
                    # Calculate osc position
                    osc.pos[0] = win_wid/2 + frames[frame_i][n] + ref_win_position[0]
                    osc.pos[1] = win_hig / 2 + ref_win_position[1]
                    osc.radius = RADIUS

                    # Naive osc velocity calculation and color it by the size of the velocity
                    osc.updateVel()
                    osc.colorByVel(MAX_DIFF)

                    # Save the current position in previous_pos variable
                    osc.previous_pos[0] = osc.pos[0]
                    # Draw each oscillator
                    osc.drawCircle(ref_win)

                    # Draw text - number of osc bellow each osc

                    if osc_num > 20:
                        if n % 10 == 0:
                            osc_nums_text[n].pos[0] = osc.pos[0]
                            osc_nums_text[n].pos[1] = win_hig/2+RADIUS*1.5
                            osc_nums_text[n].print_to(ref_win)
                    else:
                        osc_nums_text[n].pos[0] = osc.pos[0]
                        osc_nums_text[n].pos[1] = osc.pos[1] + RADIUS * 1.5
                        osc_nums_text[n].print_to(ref_win)

                main_win.blit(ref_win, [0, 0])
                pygame.display.update()

                while play_button.click_state == "pause":
                    checkUserAction(run, play_button, speed_button, restart_button, zoom_buttons, keyboard)
                    pygame.display.update()
                    clock.tick(10)

                frame_i += 1
    else:
        print("The program did not run.")

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    play()