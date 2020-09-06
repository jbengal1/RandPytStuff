import math
import random
import pygame
import os

SQ_WIDTH = 60
SQ_HEIGHT = 60
SNAKE_INTX = 200
SNAKE_INTY = 200
GAP = 20
VEL = 10
SNAKE_TALE_INTX = SNAKE_INTX - GAP
SNAKE_TALE_INTY = SNAKE_INTY
SAFE = 5

SNAKE_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs","Snake_head.png")), (SQ_WIDTH, SQ_HEIGHT) ),
			  pygame.transform.scale(pygame.image.load(os.path.join("imgs","Snake_tail.png")), (SQ_WIDTH, SQ_HEIGHT) ),
			  pygame.transform.scale(pygame.image.load(os.path.join("imgs","Snake_body.png")), (SQ_WIDTH, SQ_HEIGHT) ),]

def restart(object, res_condition, type_condition):
	if res_condition:
		
		if type_condition == 'head':
			object.dx = VEL
			object.dy = 0
			object.x = SNAKE_INTX
			object.y = SNAKE_INTY

		if type_condition == 'body':
			object.dx = VEL
			object.dy = 0
			object.x = SNAKE_INTX
			object.y = SNAKE_INTY
			object.sign_x = 1
			object.sign_y = 0

def flip_img(sign_x,sign_y,object_img):
	if sign_x == 0 and sign_y < 0:
		new_img = object_img
	
	if sign_x == 0 and sign_y > 0:
		new_img = pygame.transform.flip(object_img, False, True)
	
	if sign_x > 0 and sign_y == 0:
		new_img = pygame.transform.rotate(object_img, -90)
	
	if sign_x < 0 and sign_y == 0:
		new_img = pygame.transform.rotate(object_img, 90)
	
	return new_img

class Body:
	def __init__(self,name,head):
		
		if name == 'tail':
			self.img = SNAKE_IMGS[1]
		if name == 'body':
			self.img = SNAKE_IMGS[2]

		self.sign_x = head.sign_x
		self.sign_y = head.sign_y
		self.x = head.x - (SQ_WIDTH - GAP)*self.sign_x
		self.y = head.y - (SQ_HEIGHT - GAP)*self.sign_y
		self.dx = head.dx 
		self.dy = head.dy
		self.TurnPointX = []
		self.TurnPointY = []
		self.TurnPointSignX = []
		self.TurnPointSignY = []	
		self.img_count = 0

	def TurnPoint(self, head):
		self.TurnPointX.append(head.x)
		self.TurnPointY.append(head.y)
		self.TurnPointSignX.append(head.sign_x)
		self.TurnPointSignY.append(head.sign_y)

	def goBack(self):
		self.x -= (SQ_WIDTH - GAP)*self.sign_x
		self.y -= (SQ_HEIGHT - GAP)*self.sign_y
	#def moveLeft(self):
	#	self.dx = -VEL
	#	self.dy = 0
	
	#def moveRight(self):
	#	self.dx = VEL
	#	self.dy = 0
		
	#def moveUp(self):
	#	self.dy = -VEL
	#	self.dx = 0
		
	#def moveDown(self):
	#	self.dy = VEL
	#	self.dx = 0
		

	def draw(self, win):
		self.img_count += 1
		new_img = self.img
		if len(self.TurnPointX) != 0:
			if self.x <= (self.TurnPointX[0] + SAFE) and self.x >= (self.TurnPointX[0] - SAFE) and self.y <= (self.TurnPointY[0] + SAFE) and self.y >= (self.TurnPointY[0] - SAFE):
					self.sign_x = self.TurnPointSignX[0]
					self.sign_y = self.TurnPointSignY[0]
					del self.TurnPointSignX[0]
					del self.TurnPointSignY[0]
					del self.TurnPointX[0]
					del self.TurnPointY[0]
		
		new_img = flip_img(self.sign_x, self.sign_y, self.img)
		self.x += self.sign_x*VEL
		self.y += self.sign_y*VEL
		win.blit(new_img, (self.x, self.y))


class Head:
	def __init__(self):
		self.x = SNAKE_INTX
		self.y = SNAKE_INTY
		self.dx = VEL
		self.dy = 0
		self.tick_count = 0
		self.vel = 0
		self.img_count = 0
		self.tilt = 0
		self.img = SNAKE_IMGS[0]
		self.sign_x = 1
		self.sign_y = 0
		
	def moveLeft(self):
		self.sign_x = -1
		self.sign_y = 0
	
	def moveRight(self):
		self.sign_x = 1
		self.sign_y = 0
		
	def moveUp(self):
		self.sign_x = 0
		self.sign_y = -1
		
	def moveDown(self):
		self.sign_x = 0
		self.sign_y = 1
		
	def get_mask(self):
		return pygame.mask.from_surface(self.img)


	def collide(self, sneakBody):
		for body in sneakBody:
			dx = math.fabs(self.x - body.x)
			dy = math.fabs(self.y - body.y)
			
			dr = math.sqrt(dx*dx + dy*dy)
			if dr<2:
				return True

	def draw(self, win):
		self.img_count += 1
		new_img = flip_img(self.sign_x, self.sign_y, self.img)
		self.x += self.sign_x*VEL
		self.y += self.sign_y*VEL
		win.blit(new_img, (self.x, self.y))