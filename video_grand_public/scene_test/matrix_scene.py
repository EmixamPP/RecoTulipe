from manim import *
from numpy import *
from PIL import *

class Animate(Scene):

	def construct(self):
		file_name = "empty"

		image = Image.open("pixel_flower.png")
		data = asarray(image)

		for line in data:
			square_line = []
			width = 0
			for pixel in line:
				hex_color = '#%02x%02x%02x' % tuple(pixel)
				square = Square(fill_opacity = 1 , color = hex_color).scale(square_scale)
				square_line.append(square)
				width += 1
			height+= 1
			square_matrix.append(square_line)

		for i in range(height):
			for j in range(width):
				if j>=1:
					square_matrix[i][j].next_to(square_matrix[i][j-1] , square_scale*RIGHT)
				elif i>=1:
					square_matrix[i][j].next_to(square_matrix[i-1][j] , square_scale *DOWN)
				else:
					square_matrix[i][j].move_to(LEFT*width*square_scale + UP*height*square_scale)

				self.add(square_matrix[i][j])
		self.wait(5)