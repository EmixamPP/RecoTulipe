import itertools as it
import random

from manim import *
from creature import *
from creature_animation import *

from manim.utils.family import extract_mobject_family_members

# Constantes utiles
ASPECT_RATIO = 16.0 / 9.0
FRAME_HEIGHT = 8.0
FRAME_WIDTH = FRAME_HEIGHT * ASPECT_RATIO
FRAME_Y_RADIUS = FRAME_HEIGHT / 2
FRAME_X_RADIUS = FRAME_WIDTH / 2

class CreatureScene(Scene):
    DEFAULT_ROOT_CONFIG = {
        "total_wait_time": 0,
        "seconds_to_blink": 3,
        "creatures_start_on_screen": True,
        "default_creature_kwargs": {
            "color": BLUE,
            "flip_at_start": False,
        },
        "default_creature_start_corner": DL,
    }

    DEFAULT_CONFIG = {}

    def construct(self, **kwargs):
        kwargs=extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)
        kwargs=extract_kwargs(self, self.DEFAULT_ROOT_CONFIG, **kwargs)
        self.creatures = VGroup(*self.create_creatures())
        self.creature = self.get_primary_creature()
        if self.creatures_start_on_screen:
            self.add(*self.creatures)

    def create_creatures(self):
        """
        Likely updated for subclasses
        """
        return VGroup(self.create_creature())

    def create_creature(self):
        creature = Creature(**self.default_creature_kwargs)
        creature.to_corner(self.default_creature_start_corner)
        return creature

    def get_creatures(self):
        return self.creatures

    def get_primary_creature(self):
        return self.creatures[0]

    def any_creatures_on_screen(self):
        return len(self.get_on_screen_creatures()) > 0

    def get_on_screen_creatures(self):
        mobjects = self.get_mobject_family_members()
        return VGroup(*[
            pi for pi in self.get_creatures()
            if pi in mobjects
        ])

    def introduce_bubble(self, *args, **kwargs):
        if isinstance(args[0], Creature):
            creature = args[0]
            content = args[1:]
        else:
            creature = self.get_primary_creature()
            content = args

        bubble_class = kwargs.pop("bubble_class", SpeechBubble)
        target_mode = kwargs.pop(
            "target_mode",
            "thinking" if bubble_class is ThoughtBubble else "speaking"
        )
        bubble_kwargs = kwargs.pop("bubble_kwargs", {})
        bubble_removal_kwargs = kwargs.pop("bubble_removal_kwargs", {})
        added_anims = kwargs.pop("added_anims", [])

        anims = []
        on_screen_mobjects = extract_mobject_family_members(
            self.get_mobject_family_members()
        )

        def has_bubble(pi):
            return hasattr(pi, "bubble") and \
                pi.bubble is not None and \
                pi.bubble in on_screen_mobjects

        creatures_with_bubbles = list(filter(has_bubble, self.get_creatures()))
        if creature in creatures_with_bubbles:
            creatures_with_bubbles.remove(creature)
            old_bubble = creature.bubble
            bubble = creature.get_bubble(
                *content,
                bubble_class=bubble_class,
                **bubble_kwargs
            )
            anims += [
                ReplacementTransform(old_bubble, bubble),
                creature.change_mode, target_mode
            ]

            if "content" in old_bubcreate_creaturesble.__dic__:
                anims += [ReplacementTransform(old_bubcreate_creaturesble.content, bubble.content)]
        else:
            anims.append(CreatureBubbleIntroduction(
                creature,
                *content,
                bubble_class=bubble_class,
                bubble_kwargs=bubble_kwargs,
                target_mode=target_mode,
                **kwargs
            ))
        anims += [
            RemoveCreatureBubble(pi, **bubble_removal_kwargs)
            for pi in creatures_with_bubbles
        ]
        anims += added_anims

        self.play(*anims, **kwargs)

    def creature_says(self, *args, **kwargs):
        self.introduce_bubble(
            *args,
            bubble_class=SpeechBubble,
            **kwargs
        )

    def creature_thinks(self, *args, **kwargs):
        self.introduce_bubble(
            *args,
            bubble_class=ThoughtBubble,
            **kwargs
        )

    def say(self, *content, **kwargs):
        self.creature_says(
            self.get_primary_creature(), *content, **kwargs)

    def think(self, *content, **kwargs):
        self.creature_thinks(
            self.get_primary_creature(), *content, **kwargs)

    def compile_play_args_to_animation_list(self, *args, **kwargs):
        """
        Add animations so that all pi creatures look at the
        first mobject being animated with each .play call
        """
        animations = Scene.compile_play_args_to_animation_list(self, *args, **kwargs)
        anim_mobjects = Group(*[a.mobject for a in animations])
        all_movers = anim_mobjects.get_family()
        if not self.any_creatures_on_screen():
            return animations

        creatures = self.get_on_screen_creatures()
        non_creature_anims = [
            anim
            for anim in animations
            if len(set(anim.mobject.get_family()).interscreate_creaturesection(creatures)) == 0
        ]
        if len(non_creature_anims) == 0:
            return animations
        # Get pi creatures to look at whatever
        # is being animated
        first_anim = non_creature_anims[0]
        main_mobject = first_anim.mobject
        for creature in creatures:
            if creature not in all_movers:
                animations.append(ApplyMethod(
                    creature.look_at,
                    main_mobject,
                ))
        return animations

    def blink(self):
        self.play(Blink(random.choice(self.get_on_screen_creatures())))

    def joint_blink(self, creatures=None, shuffle=True, **kwargs):
        if creatures is None:
            creatures = self.get_on_screen_creatures()
        creatures_list = list(creatures)
        if shuffle:
            random.shuffle(creatures_list)

        def get_rate_func(pi):
            index = creatures_list.index(pi)
            proportion = float(index) / len(creatures_list)
            start_time = 0.8 * proportion
            return squish_rate_func(
                there_and_back,
                start_time, start_time + 0.2
            )

        self.play(*[
            Blink(pi, rate_func=get_rate_func(pi), **kwargs)
            for pi in creatures_list
        ])
        return self

    def wait(self, time=1, blink=True, **kwargs):
        if "stop_condition" in kwargs:
            self.non_blink_wait(time, **kwargs)
            return
        while time >= 1:
            time_to_blink = self.total_wait_time % self.seconds_to_blink == 0
            if blink and self.any_creatures_on_screen() and time_to_blink:
                self.blink()
            else:
                self.non_blink_wait(**kwargs)
            time -= 1
            self.total_wait_time += 1
        if time > 0:
            self.non_blink_wait(time, **kwargs)
        return self

    def non_blink_wait(self, time=1, **kwargs):
        Scene.wait(self, time, **kwargs)
        return self

    def change_mode(self, mode):
        self.play(self.get_primary_creature().change_mode, mode)

    def look_at(self, thing_to_look_at, creatures=None, **kwargs):
        if creatures is None:
            creatures = self.get_creatures()
        args = list(it.chain(*[
            [pi.look_at, thing_to_look_at]
            for pi in creatures
        ]))
        self.play(*args, **kwargs)




class MortyCreatureScene(CreatureScene):
    DEFAULT_CONFIG = {
        "default_creature_kwargs": {
            "color": GREY_BROWN,
            "flip_at_start": True,
        },
        "default_creature_start_corner": DR,
    }


class TeacherStudentsScene(CreatureScene):
    DEFAULT_CONFIG = {
        "student_colors": [BLUE_D, BLUE_E, BLUE_C],
        "teacher_color": GREY_BROWN,
        "student_scale_factor": 0.8,
        "seconds_to_blink": 2,
        "screen_height": 3,
        "camera_config": {
            "background_color": DARKER_GREY,
        },
    }

    def construct(self, **kwargs):
        super().construct()
        kwargs=extract_kwargs(self, self.DEFAULT_CONFIG, **kwargs)

        self.screen = ScreenRectangle(height=self.screen_height)
        self.screen.to_corner(UP + LEFT)
        self.hold_up_spot = self.teacher.get_corner(UP + LEFT) + MED_LARGE_BUFF * UP

    def create_creatures(self):

        self.teacher = Mortimer(color=self.teacher_color)
        self.teacher.to_corner(DOWN + RIGHT)
        self.teacher.look(DOWN + LEFT)
        self.students = VGroup(*[
            Randolph(color=c)
            for c in self.student_colors
        ])
        self.students.arrange(RIGHT)
        self.students.scale(self.student_scale_factor)
        self.students.to_corner(DOWN + LEFT)
        self.teacher.look_at(self.students[-1].eyes)
        for student in self.students:
            student.look_at(self.teacher.eyes)

        return [self.teacher] + list(self.students)

    def get_teacher(self):
        return self.teacher

    def get_students(self):
        return self.students

    def teacher_says(self, *content, **kwargs):
        if "bubble_kwargs" not in kwargs:
            kwargs["bubble_kwargs"] = {"direction": 1.4*RIGHT}

        return self.creature_says(
            self.get_teacher(), *content, **kwargs
        )

    def student_says(self, *content, **kwargs):
        if "target_mode" not in kwargs:
            target_mode = random.choice([
                "raise_right_hand",
                "raise_left_hand",
            ])
            kwargs["target_mode"] = target_mode
        if "bubble_kwargs" not in kwargs:
            kwargs["bubble_kwargs"] = {"direction": LEFT}
        student = self.get_students()[kwargs.get("student_index", 2)]
        return self.creature_says(
            student, *content, **kwargs
        )

    def teacher_thinks(self, *content, **kwargs):
        return self.creature_thinks(
            self.get_teacher(), *content, **kwargs
        )

    def student_thinks(self, *content, **kwargs):
        student = self.get_students()[kwargs.get("student_index", 2)]
        return self.creature_thinks(student, *content, **kwargs)

    def change_all_student_modes(self, mode, **kwargs):
        self.change_student_modes(*[mode] * len(self.students), **kwargs)

    def change_student_modes(self, *modes, **kwargs):
        added_anims = kwargs.pop("added_anims", [])
        self.play(
            self.get_student_changes(*modes, **kwargs),
            *added_anims
        )

    def get_student_changes(self, *modes, **kwargs):
        pairs = list(zip(self.get_students(), modes))
        pairs = [(s, m) for s, m in pairs if m is not None]
        start = VGroup(*[s for s, m in pairs])
        target = VGroup(*[s.copy().change_mode(m) for s, m in pairs])
        if "look_at_arg" in kwargs:
            for pi in target:
                pi.look_at(kwargs["look_at_arg"])
        anims = [
            Transform(s, t)
            for s, t in zip(start, target)
        ]
        return LaggedStart(
            *anims,
            lag_ratio=kwargs.get("lag_ratio", 0.5),
            run_time=1,
        )
        # return Transform(
        #     start, target,
        #     lag_ratio=lag_ratio,
        #     run_time=2
        # )

    def zoom_in_on_thought_bubble(self, bubble=None, radius=FRAME_Y_RADIUS + FRAME_X_RADIUS):
        if bubble is None:
            for pi in self.get_creatures():
                if hasattr(pi, "bubble") and isinstance(pi.bubble, ThoughtBubble):
                    bubble = pi.bubble
                    break
            if bubble is None:
                raise Exception("No pi creatures have a thought bubble")
        vect = -bubble.get_bubble_center()

        def func(point):
            centered = point + vect
            return radius * centered / get_norm(centered)
        self.play(*[
            ApplyPointwiseFunction(func, mob)
            for mob in self.get_mobjects()
        ])

    def teacher_holds_up(self, mobject, target_mode="raise_right_hand", added_anims=None, **kwargs):
        mobject.move_to(self.hold_up_spot, DOWN)
        mobject.shift_onto_screen()
        mobject_copy = mobject.copy()
        mobject_copy.shift(DOWN)
        mobject_copy.fade(1)
        added_anims = added_anims or []

        #    ApplyMethod(self.teacher.change, target_mode),

        self.play(
            ReplacementTransform(mobject_copy, mobject),
            *added_anims
        )
