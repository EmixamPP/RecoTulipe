from manim import *

def generate_title(scene, *names, **kwargs):
	"""
	Generate a title in the center , then after wait_time seconds , shift to a corner
	The size of the title is fixed to 1.5
	return Tex object title
	"""
	SPEED = 0.75

	if "wait_time" in kwargs:
		wait_time = kwargs["wait_time"]
	else:
		wait_time = 1

	if "corner" in kwargs:
		corner = kwargs["corner"]
	else:
		corner = UL

	title = Tex(*names).scale(1.5)
	scene.play(Write(title))
	scene.wait(wait_time)
	scene.play(ApplyMethod(title.scale,0.75),run_time=SPEED)
	scene.play(ApplyMethod(title.to_corner , corner),run_time=SPEED)

	return title
