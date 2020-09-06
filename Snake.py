import math
import random
import pygame
import os

SQ_WIDTH = 60
SQ_HEIGHT = 60
SNAKE_INTX = 200
SNAKE_INTY = 200
GAP = 10
VEL = 10
SNAKE_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs","Snake_head.png")), (SQ_WIDTH, SQ_HEIGHT) ),
			  pygame.transform.scale(pygame.image.load(os.path.join("imgs","Snake_tail.png")), (SQ_WIDTH, SQ_HEIGHT) ),
			  pygame.transform.scale(pygame.image.load(os.path.join("imgs","Snake_body.png")), (SQ_WIDTH, SQ_HEIGHT) ),]
class Snake:

	def restart(self, condition):
		if condition:
			self.head.dx = 0
			self.head.dy = 0
			self.head.x = SNAKE_INTX
			self.head.y = SNAKE_INTY
			self.body.body_num = 0
			self.Snake_body = [self.tail]
			self.body_num = 0
			self.body_x = [0]
			self.body_y = [0]
			self.sign_x = 1
			self.sign_y = 0

	class body:
		def __init__(self):
			self.tail = SNAKE_IMGS[1]
			self.body = SNAKE_IMGS[2]
			self.Snake_body = [self.tail]
			self.body_num = 0
			self.body_x = [0]
			self.body_y = [0]
			self.sign_x = 1
			self.sign_y = 0

	class head:
		def __init__(self):
			self.x = SNAKE_INTX
			self.y = SNAKE_INTY
			self.dx = VEL
			self.dy = 0
			self.tick_count = 0
			self.vel = 0
			self.img_count = 0
			self.tilt = 0
			self.head = SNAKE_IMGS[0]

		
		def moveLeft(self):
			self.dx = -VEL
			self.dy = 0
			#self.x -= self.dx

		def moveRight(self):
			self.dx = VEL
			self.dy = 0
			#self.x += self.dx
			
		def moveUp(self):
			self.dy = -VEL
			self.dx = 0
			#self.y -= self.dy

		def moveDown(self):
			self.dy = VEL
			self.dx = 0
			#self.y += self.dy

		def add_body(self,score):
			self.body_num += 1
			self.Snake_body.insert(0, self.body)
			self.body_x.insert(0,self.x)
			self.body_y.insert(0,self.y)
			score += 1
			return score

		def get_mask(self):
			return pygame.mask.from_surface(self.head)

		def get_direction(self):
			if self.dx < 0:
				self.sign_x = 1
				self.sign_y = 0
			
			if self.dx > 0:
				self.sign_x = -1
				self.sign_y = 0
			
			if self.dy < 0:
				self.sign_x = 0
				self.sign_y = 1
			
			if self.dy > 0:
				self.sign_x = 0
				self.sign_y = -1
		
		def draw(self, win):
			self.img_count += 1
			self.get_direction()
			temp_x = self.x
			temp_y = self.y

			d = 0
			for body in self.Snake_body:
				temp_x += self.sign_x*d*(SQ_WIDTH + GAP)
				temp_y += self.sign_y*d*(SQ_WIDTH + GAP)
				self.body_x[d] = temp_x
				self.body_y[d] = temp_y

				#body = pygame.transform.flip(body,False, True)
				win.blit(self.head, (self.x , self.y))
				win.blit(body, (self.body_x[d], self.body_y[d]))
				d+=1
				
			self.x += self.dx
			self.y += self.dy
			pygame.display.update()




	'''
			if self.dx == 0 and self.dy < 0 :
				win.blit(self.tail, (self.x, self.y + SQ_HEIGHT - GAP))
				win.blit(self.head, (self.x,self.y))
			
			if self.dx == 0 and self.dy > 0 :
				fliped_head = pygame.transform.flip(self.head,False, True)
				win.blit(fliped_head,(self.x,self.y))

				if True:

					d = 0
					for body in self.Snake_body:
						body = pygame.transform.flip(body,False, True)
						win.blit(body, (self.x, self.y - (d+1)*(SQ_HEIGHT - GAP)))
						d += 1

			if self.dy == 0 and self.dx > 0 :
				self.tilt = -90
				rotated_head = pygame.transform.rotate(self.head, self.tilt)
				rotated_tail = pygame.transform.rotate(self.tail, self.tilt)
				win.blit(rotated_tail, (self.x - SQ_WIDTH + GAP, self.y))
				win.blit(rotated_head,(self.x,self.y))
			
			if self.dy == 0 and self.dx < 0 :
				self.tilt = 90
				rotated_head = pygame.transform.rotate(self.head, self.tilt)
				rotated_tail = pygame.transform.rotate(self.tail, self.tilt)
				win.blit(rotated_tail, (self.x + SQ_WIDTH - GAP, self.y))
				win.blit(rotated_head,(self.x,self.y))
			
	'''		
			