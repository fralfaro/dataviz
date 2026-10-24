from manim import *
config.disable_caching = True

def hsl_to_hsv(h, s, l):
    v = l + s * min(l, 1-l)
    s = 0 if v == 0 else 2*(1 - l/v)
    return ManimColor.from_hsv([h, s, v])

class MainScene(Scene):
  def construct(self):
    N_DOTS    = 6
    N_ARROWS  = 30
    arrow = Line(ORIGIN, LEFT*3.8, buff=0)\
      .add_tip(tip_width=0.2, tip_length=0.3)

    colors = [
      hsl_to_hsv(i/N_ARROWS, 1, 0.5)
      for i in range(N_ARROWS)
    ]

    dots = VGroup(*[
      Dot(stroke_width=3, fill_opacity=0)
        .move_to(arrow.point_from_proportion(i/N_DOTS))
        .scale(0.8)
      for i in range(1, N_DOTS)
    ])
    arrow.add(dots)

    arrows = VGroup(*[
      arrow.copy()
        .rotate(TAU * i / N_ARROWS, about_point=ORIGIN)
        .set_color(colors[i])
      for i in range(N_ARROWS)
    ]).fade(0.6)

    l1 = Line(ORIGIN, RIGHT * arrow.get_length() / 3)
    l2 = l1.copy()
    l3 = Line(ORIGIN, RIGHT * l1.get_length() * 2)

    def l1_updater(mob, dt):
      mob.rotate(40 * DEGREES * dt, about_point=ORIGIN)

    def l2_updater(mob, dt):
      mob.rotate(-50 * DEGREES * dt, about_point=ORIGIN)

    def l3_updater(mob:Line):
      mob.put_start_and_end_on(
        ORIGIN, l1.get_vector() + l2.get_vector()
      )

    def color_updater(mob:Line):
      angle = mob.get_angle()
      color = hsl_to_hsv((angle+PI)/TAU, 1, 0.5)
      mob.set_color(color)

    l1.add_updater(l1_updater)
    l2.add_updater(l2_updater)
    l3.add_updater(l3_updater)

    lines = [l1, l2, l3]
    dots  = VGroup(*[Dot(l.get_end()) for l in lines])

    for d,l in zip(dots, lines):
      l.add_updater(color_updater)
      d.add_updater(
        lambda m, l=l: m.move_to(l.get_end()).match_color(l)
      )

    self.add(arrows, l1, l2, l3, *dots)
    self.wait(30)
