from manim import *
from numpy import *
from PIL import *
import sys


sys.path.insert(1, "ressource")

from generate_title import *

class Scene3(Scene):

	def color_shift(self , color_vector , shift , numbers , lower_bound = []):
		"""for parameter numbers, its a list containing 0, 1 and/or 3 nothing else"""
		for i in numbers:
			color_vector[i] += shift
			if color_vector[i] > 255:
				color_vector[i] = 255
			elif color_vector[i] < 0:
				color_vector[i] = 0

			if lower_bound != []:
				for i in range(3):
					if color_vector[i] < lower_bound[i]:
						color_vector[i] = lower_bound[i]

			self.rouge.tracker.set_value(color_vector[0])
			self.vert.tracker.set_value(color_vector[1])
			self.bleu.tracker.set_value(color_vector[2])
		return (color_vector , '#%02x%02x%02x' % tuple(color_vector))

	def construct(self):

		color_vector = [251 , 158 , 54]
		self.rouge = Variable(color_vector[0] , "Rouge" , var_type = Integer)
		self.vert = Variable(color_vector[1] , "Vert" , var_type = Integer)
		self.bleu = Variable(color_vector[2] , "Bleu" , var_type = Integer)

		height = 0
		width = 0
		square_matrix = []
		square_scale = 0.05
		real_flower = ImageMobject("ressource/images/fleur_simple/une rose_3.jpg").scale(3)
		big_pixel = ImageMobject("ressource/images/big_pixel_flower.png").scale(0.1)
		frame = Square(color = LIGHT_GREY).scale(.75)
		pixel = Square(fill_opacity = 1 , color = '#%02x%02x%02x' % tuple(color_vector)).scale(.75)
		frame.shift(RIGHT*0.30 , DOWN*0.75)
		pixel.shift(RIGHT*0.30 , DOWN*0.75)

		title = generate_title(self ,"Comment un ordinateur voit une image?")
		self.play(FadeIn(real_flower))
		self.wait(9)
		self.play(FadeOut(real_flower),FadeOut(title))
		self.play(FadeIn(big_pixel))
		self.wait(0.5)
		self.play(ApplyMethod(big_pixel.scale , 20))
		self.wait(1)
		self.play(ApplyMethod(big_pixel.scale , 10))
		self.wait(1)
		self.play(ShowCreation(frame))
		self.wait(1)
		self.play(FadeOut(big_pixel) , FadeOut(frame) , FadeIn(pixel))
		self.play(ApplyMethod(pixel.move_to ,ORIGIN))
		self.play(ApplyMethod(pixel.scale , 2))

		label_0 = Tex("Un Pixel")
		label_0.next_to(pixel , 3*UP)
		self.rouge.shift(LEFT*4 , UP)
		self.vert.next_to(self.rouge , DOWN*2)
		self.bleu.next_to(self.vert , DOWN*2)

		self.play(ApplyMethod(pixel.shift , 2*RIGHT),Write(self.rouge), Write(self.vert),Write(self.bleu),Write(label_0))
		self.wait(2)

		#color shift

		for i in range(15):
			color_data = self.color_shift(color_vector , 10 , [2])
			color_vector = color_data[0]
			pixel.set_color(color_data[1])
			self.wait(0.15)

		for i in range(10):
			color_data = self.color_shift(color_vector , -10 , [1])
			color_vector = color_data[0]
			pixel.set_color(color_data[1])
			self.wait(0.15)

		for i in range(15):
			color_data = self.color_shift(color_vector , -10 , [0])
			color_vector = color_data[0]
			pixel.set_color(color_data[1])
			self.wait(0.15)

		for i in range(21):
			color_data = self.color_shift(color_vector , 10 , [0,1,2])
			color_vector = color_data[0]
			pixel.set_color(color_data[1])
			self.wait(0.15)

		while True:
			color_data = self.color_shift(color_vector , -10 , [0,1,2] ,[251 ,158 , 54])
			color_vector = color_data[0]
			pixel.set_color(color_data[1])
			print(color_vector)
			if color_vector[0] == 251 and color_vector[1] == 158 and color_vector[2] == 54:
				break
			#color_vector = color_data[0]
			#pixel.set_color(color_data[1])
			self.wait(0.15)

		self.wait(2)
		self.play(FadeOut(self.rouge),FadeOut(self.vert),FadeOut(self.bleu),FadeOut(label_0),ApplyMethod(pixel.move_to , ORIGIN))
		self.play(ApplyMethod(pixel.scale, 0.05))
		big_pixel.scale(0.1)
		self.play(FadeIn(big_pixel))
		self.wait(1)

		horizontale = Line(start = (-2.5 , 3 , 0) , end= (2.5 , 3 ,0))
		verticale = Line(start = (-3 , 2.5 , 0) , end= (-3 , -2.5 ,0))
		dimension = [32 , 32]
		label_1 = Tex("32")
		label_2 = Tex("32")
		label_3 = Tex("240")
		label_4 = Tex("240")
		label_1.next_to(horizontale , UP)
		label_3.next_to(horizontale , UP)
		label_2.next_to(verticale,LEFT*1.5)
		label_4.next_to(verticale,LEFT*1.5)
		text = Tex("57600 pixels \n en tout !")
		text.next_to(real_flower , DOWN)

		self.play(ShowCreation(horizontale) , ShowCreation(verticale))
		self.play(Write(label_1) , Write(label_2))
		self.wait(2)
		self.play(ApplyMethod(big_pixel.scale , 0.08))
		self.wait(1)
		self.play(FadeOut(big_pixel) , FadeIn(real_flower) , FadeOut(label_1) ,FadeOut(label_2) , Write(label_3) , Write(label_4))
		self.play(Write(text))

		self.wait(5)
