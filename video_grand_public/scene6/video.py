import sys
from manim import *
import random

sys.path.insert(1, "ressource")

from image_loader import *
from generate_title import *

TRAINING_FLOWERS= "ressource/images/fleur_apprentissage"
COMPUTER_PATH = "ressource/images/moniteur.svg"
GEAR_PATH = "ressource/images/gear.png"
FLOWERS_NAMES = ["tournesol", "tulipe", "paquerette"]


run_time = 0.7

random.seed(121210)
class Scene6(Scene):

	def draw_network_change(self , gears):
		speed = 0.3
		label = Tex("Modification des connaissances")
		label.shift(3.5*DOWN)

		for i in range(2):
			self.play(FadeIn(label, run_time = 0.30),*[Rotating(gear,angle=360,run_time=speed)for gear in gears])
			self.play(FadeOut(label, run_time = 0.30),*[Rotating(gear,angle=360,run_time=speed)for gear in gears])

	def draw_is_correct(self , text , _color , speed):

		label = Tex(text , color=_color).scale(2)
		label.shift(RIGHT*0.25)

		self.play(FadeIn(label),run_time=speed)
		self.play(FadeOut(label) , run_time =speed)

	def construct(self):

		ANIMATION_SPEED = 0.45

		#pré traitement
		data = load_flower(TRAINING_FLOWERS , FLOWERS_NAMES , 3)
		random.shuffle(data)
		flowers = []
		names = []
		computer_guesses = []
		answers = []

		for t in data:
			flower = t[0]
			name = Tex(t[1]).scale(1)
			guess = Tex(t[1] + " ?").scale(1)
			answer = Tex(t[1] + " !")

			flower.shift(4*RIGHT,DOWN*0.5)
			flower.scale(2.5)
			name.next_to(flower , UP)
			name.scale(1.5)
			guess.shift(1.25*UP , 4*LEFT)
			answer.shift(1.25*UP , 4*LEFT)

			flowers.append(flower)
			names.append(name)
			computer_guesses.append(guess)
			answers.append(answer)

		random.shuffle(computer_guesses)
		computer = SVGMobject(COMPUTER_PATH).scale(2.5)
		computer[0].set_color(GRAY)
		computer.shift(LEFT*4)

		gear1 = ImageMobject(GEAR_PATH).scale(0.5)
		gear2 = ImageMobject(GEAR_PATH).scale(0.75)
		gear1.shift(LEFT*3.5)
		gear2.next_to(gear1, 0.25*LEFT)

		#animation
		title = generate_title(self ,"Comment un ordinateur apprend ?")
		sub_title1 = Tex("1.Apprentissage").next_to(title,RIGHT)
		sub_title2 = Tex("2.Vérification").next_to(title,RIGHT)
		self.play(Write(sub_title1), run_time=run_time)
		self.play(ShowCreation(computer),FadeIn(gear1),FadeIn(gear2), run_time=run_time)

		apprentissage = True

		for i in range(len(flowers)):
			if i == int(len(flowers)/2):
				apprentissage = False
				ANIMATION_SPEED = 0.3
				self.play(FadeOut(gear1),FadeOut(gear2), run_time=run_time)
				self.play(Transform(sub_title1, sub_title2), run_time=run_time)

			self.play(FadeIn(flowers[i]),FadeIn(names[i]),run_time=ANIMATION_SPEED)
			if not apprentissage:
				computer_guesses[i] = answers[i]
			self.play(Write(computer_guesses[i]),run_time=ANIMATION_SPEED)

			if computer_guesses[i].get_tex_string()[:-2] == names[i].get_tex_string():
				self.draw_is_correct("OUI" , GREEN , ANIMATION_SPEED)
			else:
				self.draw_is_correct("NON" , RED , ANIMATION_SPEED)

			if apprentissage:
				self.draw_network_change([gear1 , gear2])
			self.play(FadeOut(flowers[i]),FadeOut(computer_guesses[i]),FadeOut(names[i]), run_time=ANIMATION_SPEED)

		self.wait()
		self.play(*[FadeOut(mob)for mob in self.mobjects], run_time=run_time)
