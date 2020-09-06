import math
import random
import pygame
import os

SQ_WIDTH = 60
SQ_HEIGHT = 60
ANIMATION_TIME = 10
APPLE_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs","apple_1.png")), (SQ_WIDTH, SQ_HEIGHT) ),
			  pygame.transform.scale(pygame.image.load(os.path.join("imgs","apple_2.png")), (SQ_WIDTH, SQ_HEIGHT) ),
			  pygame.transform.scale(pygame.image.load(os.path.join("imgs","apple_3.png")), (SQ_WIDTH, SQ_HEIGHT) ),]
class Apple:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.tick_count = 0
		self.img_count = 0
		self.img = APPLE_IMGS[0]

	def Change_position(self,x,y):
		self.x = x
		self.y = y

	def collide(self, sneakHead, WIN_WIDTH, WIN_HEIGHT):
		snake_mask = sneakHead.get_mask()
		mask = pygame.mask.from_surface(self.img)
		offset = (self.x - sneakHead.x, self.y - round(sneakHead.y))
		point = snake_mask.overlap(mask, offset)

		if point:
			self.x = random.randint(10,WIN_WIDTH - 10)
			self.y = random.randint(10,WIN_HEIGHT - 50)
			return True

		return False


	def draw(self, win):
		self.img_count += 1

		if self.img_count < ANIMATION_TIME:
			self.img = APPLE_IMGS[0]
		elif self.img_count < ANIMATION_TIME*2:
			self.img = APPLE_IMGS[1]
		elif self.img_count < ANIMATION_TIME*3:
			self.img = APPLE_IMGS[2]
		elif self.img_count < ANIMATION_TIME*4:
			self.img = APPLE_IMGS[1]
		elif self.img_count < ANIMATION_TIME*4 + 1:
			self.img = APPLE_IMGS[0]
			self.img_count = 0

		win.blit(self.img,(self.x,self.y))
			
		pygame.display.update()