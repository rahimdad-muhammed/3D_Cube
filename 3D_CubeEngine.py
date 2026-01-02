import pygame
from sys import exit
import numpy as np

class Engine:
	def __init__(self, origin_x, origin_y, origin_z):

		self.origin_x, self.origin_y, self.origin_z = origin_x, origin_y, origin_z

	def convert(self, three_D):
		"""
		Gets an np.array as an input which stores 3Dimensional coordinates of the shape inside of it and converts it to 2D coordinates

		Equation: display_X = (x*300) / (z+300)
				  display_Y = (y*300) / (z+300)
		"""

		copy_three_D = three_D.copy()

		# (x * 300)
		copy_three_D[... , 0] *= 300

		# (y * 300)
		copy_three_D[... , 1] *= 300

		# (z+300)
		copy_three_D[... , 2] += 300

		# dividing part
		copy_three_D[... , 0] /= copy_three_D[... , 2]
		copy_three_D[... , 1] /= copy_three_D[... , 2]

		copy_three_D = np.delete(copy_three_D, 2, axis= 2)


		return copy_three_D.copy()





	

	def perspective(self, points):
		"""
		Gets the 2D coordinates of the shape and converts it to normal pygame coordinates for drawing
		"""
		
		copy_coordinates = points.copy()


		
		# accessing every y-value and multiplying with -1 to draw the shape correctly on pygame map
		copy_coordinates[... , 1] *= -1

		copy_coordinates[... , 0] += self.origin_x
		copy_coordinates[... , 1] += self.origin_y

		
		return copy_coordinates.copy()



		




class Main:

	def __init__(self):
		super().__init__()

		pygame.init()
		self.screen = pygame.display.set_mode((0,0,),pygame.FULLSCREEN)
		pygame.display.set_caption("3D_CubeEngine")
		self.clock = pygame.time.Clock()

		self.screen_w, self.screen_h = self.screen.get_size()

		self.origin_x, self.origin_y, self.origin_z = self.screen_w/2, self.screen_h/2, 0

		self.engine = Engine(self.origin_x, self.origin_y, self.origin_z)

		self.cube_coordinates = np.array([ # [depth, rows, columns]
			[[-100,100,200],[100,100,200],[100,-100,200],[-100,-100,200]], # white face
			[[-100,100,400],[-100,100,200],[-100,-100,200],[-100,-100,400]], # blue face
			[[100,100,200],[100,100,400],[100,-100,400],[100,-100,200]], # green face
			[[100,100,400],[-100,100,400],[-100,-100,400],[100,-100,400]], # yellow face
			[[-100,100,400],[100,100,400],[100,100,200],[-100,100,200]], # red face
			[[-100,-100,200],[100,-100,200],[100,-100,400],[-100,-100,400]] # orange face
		], dtype = float)
		
		# Getting the 2D coordinates of the cube
		
		self.draw_cube = self.engine.convert(self.cube_coordinates)
		self.draw_cube = self.engine.perspective(self.draw_cube)




		# x,y axis Line
		self.y_axis = np.array([[0,-1000],[0,1000]], dtype = float)
		self.x_axis = np.array([[-1000,0],[1000,0]], dtype = float)

		self.draw_y_axis = self.engine.perspective(self.y_axis)
		self.draw_x_axis = self.engine.perspective(self.x_axis)


	


	def game_loop(self):

		while True:
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					
					pygame.quit()
					exit()

				if event.type == pygame.MOUSEWHEEL:

					if event.x < 0: # left


						# if z smaller than 100 or if x larger than 0 and z equals to 100 then reduce x value
						x_reduce = (
							(self.cube_coordinates[:,:,2] < 300) | (
								(self.cube_coordinates[:,:,0] > 0) & (self.cube_coordinates[:,:,2] == 300)
							))

						# if z larger than 100 or if x smaller than 0 and z equals to 100 then increase x value
						x_increase = (
							(self.cube_coordinates[:,:,2] > 300) | (
								(self.cube_coordinates[:,:,0] < 0) & (self.cube_coordinates[:,:,2] == 300)
								)
							)


						# if x smaller than 0 or if x equals to 0 and z smaller_equals to 0 then increase z
						z_increase = (
							(self.cube_coordinates[:,:,0] < 0) |
							((self.cube_coordinates[:,:,0] == 0) & (self.cube_coordinates[:,:,2] <= 200))
							)

						# if x larger than 0 or if x equals to 0 and z larger_equals to 200 then decrease z
						z_decrease = (
							(self.cube_coordinates[:,:,0] > 0) |
							((self.cube_coordinates[:,:,0] == 0) & (self.cube_coordinates[:,:,2] >= 400))
							)

						

						
						

						# reduce x
						self.cube_coordinates[x_reduce, 0] -= 5


						# increase x
						self.cube_coordinates[x_increase, 0] += 5

						# increase z
						self.cube_coordinates[z_increase, 2] += 5

						# decrease z
						self.cube_coordinates[z_decrease, 2] -= 5


						

						# Getting the drawing coordinates of the cube
						self.draw_cube = self.engine.convert(self.cube_coordinates)
						self.draw_cube = self.engine.perspective(self.draw_cube)
					
									

					if event.x > 0: # right

						# if z smaller than 100 or if x smaller than 0 and z equals to 100 then increase x value
						x_increase = (
							(self.cube_coordinates[:,:,2] < 300) | (
								(self.cube_coordinates[:,:,0] < 0) & (self.cube_coordinates[:,:,2] == 300)
							))

						# if z larger than 100 or if x larger than 0 and z equals to 100 then decrease x value
						x_reduce = (
							(self.cube_coordinates[:,:,2] > 300) | (
								(self.cube_coordinates[:,:,0] > 0) & (self.cube_coordinates[:,:,2] == 300)
								)
							)

						# if x smaller than 0 or if x equals to 0 and z larger_equals to 200 then decrease z
						z_decrease = (
							(self.cube_coordinates[:,:,0] < 0) |
							((self.cube_coordinates[:,:,0] == 0) & (self.cube_coordinates[:,:,2] >= 400))
							)

						# if x larger than 0 or if x equals to 0 and z smaller_equals to 0 then increase z
						z_increase = (
							(self.cube_coordinates[:,:,0] > 0) |
							((self.cube_coordinates[:,:,0] == 0) & (self.cube_coordinates[:,:,2] <= 200))
							)

						

						
						

						# reduce x
						self.cube_coordinates[x_reduce, 0] -= 5


						# increase x
						self.cube_coordinates[x_increase, 0] += 5

						# increase z
						self.cube_coordinates[z_increase, 2] += 5

						# decrease z
						self.cube_coordinates[z_decrease, 2] -= 5

						# Getting the drawing coordinates of the cube
						self.draw_cube = self.engine.convert(self.cube_coordinates)
						self.draw_cube = self.engine.perspective(self.draw_cube)
						

					if event.y < 0: # down

						# if z larger than 100 or if y smaller than 0 and z equals to 100 then increase y value
						y_increase = (
							(self.cube_coordinates[:,:,2] > 300) | (
								(self.cube_coordinates[:,:,1] < 0) & (self.cube_coordinates[:,:,2] == 300)
							))

						# if z smaller than 100 or if y larger than 0 and z equals to 100 then decrease y value
						y_reduce = (
							(self.cube_coordinates[:,:,2] < 300) | (
								(self.cube_coordinates[:,:,1] > 0) & (self.cube_coordinates[:,:,2] == 300)
								)
							)

						# if y smaller than 0 or if y equals to 0 and z smaller_equals to 0 then increase z
						z_increase = (
							(self.cube_coordinates[:,:,1] < 0) |
							((self.cube_coordinates[:,:,1] == 0) & (self.cube_coordinates[:,:,2] <= 200))
							)

						# if y larger than 0 or if y equals to 0 and z larger_equals to 200 then decrease z
						z_decrease = (
							(self.cube_coordinates[:,:,1] > 0) |
							((self.cube_coordinates[:,:,1] == 0) & (self.cube_coordinates[:,:,2] >= 400))
							)

						

						
						

						# reduce y
						self.cube_coordinates[y_reduce, 1] -= 5


						# increase y
						self.cube_coordinates[y_increase, 1] += 5

						# increase z
						self.cube_coordinates[z_increase, 2] += 5

						# decrease z
						self.cube_coordinates[z_decrease, 2] -= 5

				
						# Getting the drawing coordinates of the cube
						self.draw_cube = self.engine.convert(self.cube_coordinates)
						self.draw_cube = self.engine.perspective(self.draw_cube)

					if event.y > 0: # up

						# if z smaller than 100 or if y smaller than 0 and z equals to 100 then increase y value
						y_increase = (
							(self.cube_coordinates[:,:,2] < 300) | (
								(self.cube_coordinates[:,:,1] < 0) & (self.cube_coordinates[:,:,2] == 300)
							))

						# if z larger than 100 or if y larger than 0 and z equals to 100 then decrease y value
						y_reduce = (
							(self.cube_coordinates[:,:,2] > 300) | (
								(self.cube_coordinates[:,:,1] > 0) & (self.cube_coordinates[:,:,2] == 300)
								)
							)

						# if y larger than 0 or if y equals to 0 and z smaller_equals to 0 then increase z
						z_increase = (
							(self.cube_coordinates[:,:,1] > 0) |
							((self.cube_coordinates[:,:,1] == 0) & (self.cube_coordinates[:,:,2] <= 200))
							)

						# if y smaller than 0 or if y equals to 0 and z larger_equals to 200 then decrease z
						z_decrease = (
							(self.cube_coordinates[:,:,1] < 0) |
							((self.cube_coordinates[:,:,1] == 0) & (self.cube_coordinates[:,:,2] >= 400))
							)

						

						
						

						# reduce y
						self.cube_coordinates[y_reduce, 1] -= 5


						# increase y
						self.cube_coordinates[y_increase, 1] += 5

						# increase z
						self.cube_coordinates[z_increase, 2] += 5

						# decrease z
						self.cube_coordinates[z_decrease, 2] -= 5

				
						# Getting the drawing coordinates of the cube
						self.draw_cube = self.engine.convert(self.cube_coordinates)
						self.draw_cube = self.engine.perspective(self.draw_cube)


					
		


			

			self.screen.fill((0,0,0))


			# width -> makes it blank
			pygame.draw.polygon(self.screen, (0,255,255), self.draw_cube[5], width = 2) # orange
			pygame.draw.polygon(self.screen, (255,0,0), self.draw_cube[4], width = 2) # red
			pygame.draw.polygon(self.screen, (255,255,0), self.draw_cube[3], width = 2) # yellow face
			pygame.draw.polygon(self.screen, (0,255,0), self.draw_cube[2], width = 2) # green
			pygame.draw.polygon(self.screen, (0,0,255), self.draw_cube[1], width = 2) # blue face
			pygame.draw.polygon(self.screen, (255,255,255), self.draw_cube[0], width = 2) # white face



			pygame.draw.line(self.screen, (255,0,0), self.draw_y_axis[0], self.draw_y_axis[1], 2)
			pygame.draw.line(self.screen, (0,255,0), self.draw_x_axis[0], self.draw_x_axis[1], 2)





			

			pygame.display.flip()
			self.clock.tick(60)



if __name__ == '__main__':
	Main().game_loop()















