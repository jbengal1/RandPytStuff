import Snake_1
import Apple
import os
import pygame, sys
import time
import random
pygame.init()
pygame.font.init()

WIN_WIDTH = 1400
WIN_HEIGHT = 800
SAFE = 15
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","BG.png")), (WIN_WIDTH, WIN_HEIGHT) )
STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(win, score):
	win.blit(BG_IMG, (8,8))
	text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
	pygame.display.update()

def draw_some(win, object1, object2, num_body):
	for i in range(num_body):
		if num_body>1:
			Snake_1.get_direction(object1[i-1], object1[i])
		else:
			Snake_1.get_direction(object1[i],object2)
		object1[i].draw(win)

def main():
	win = pygame.display.set_mode((WIN_WIDTH + SAFE, WIN_HEIGHT + SAFE))
	clock = pygame.time.Clock()
	snake = Snake_1
	snakeHead = Snake_1.Head()
	snakeBody = [Snake_1.Body('tail',snakeHead)] # the body object needs the snakeHead object. that's why it's guven to it as an input
	num_body = 0
	apple = Apple.Apple(random.randint(10,WIN_WIDTH - 10), random.randint(10,WIN_HEIGHT - 50)) #chose an initial random position of an apple (int) within the frame (that's WIN_WIDTH and WIN_HEIGHT)
	score = 0
	pause = True
	res_condition = False 
	
	while pause:
		clock.tick(200)
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT:
				pause = False
				pygame.quit()
				sys.exit()
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				pause = False
			if event.key == pygame.K_p:
				pause()

		if snakeHead.x > (WIN_WIDTH - SAFE) or snakeHead.x < SAFE or snakeHead.y > (WIN_HEIGHT- SAFE) or snakeHead.y < SAFE or snakeHead.collide(snakeBody):
			score = 0
			num_body = 0
			del snakeBody
			del snakeHead
			snakeHead = Snake_1.Head()
			snakeBody = [Snake_1.Body('tail', snakeHead)]
			res_condition = True
			apple.x = random.randint(10,WIN_WIDTH - 10)
			apple.y = random.randint(10,WIN_HEIGHT - 10)
		
		res_condition = False

		if apple.collide(snakeHead, WIN_WIDTH, WIN_HEIGHT): 
			for snake in snakeBody:
				snake.goBack()
			snakeBody.append(Snake_1.Body('body',snakeHead))
			score += 1
			num_body += 1
		
		if keys[pygame.K_d] and snakeHead.sign_x == 0:
			snakeHead.moveRight()
			for body in snakeBody:
				body.TurnPoint(snakeHead)
		if keys[pygame.K_a] and snakeHead.sign_x == 0:
			snakeHead.moveLeft()
			for body in snakeBody:
				body.TurnPoint(snakeHead)
		if keys[pygame.K_s] and snakeHead.sign_y == 0:
			snakeHead.moveDown()
			for body in snakeBody:
				body.TurnPoint(snakeHead)
		if keys[pygame.K_w] and snakeHead.sign_y == 0:
			snakeHead.moveUp()
			for body in snakeBody:
				body.TurnPoint(snakeHead)
		
		draw_window(win,score)
		snakeHead.draw(win)
		for body in snakeBody:
			body.draw(win)
		apple.draw(win)
		pygame.display.update()
main()