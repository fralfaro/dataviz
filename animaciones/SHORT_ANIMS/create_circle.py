from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    RADIUS = 3.5
    c = Circle(radius=RADIUS)
    d = Dot()
    l = Line(ORIGIN, RIGHT*RADIUS)

    self.play(GrowFromCenter(d))
    self.play(Create(l))
    self.play(
      Rotate(l, TAU, about_point=ORIGIN),
      Create(c),
      run_time=3,
    )
    self.play(ShrinkToCenter(d), Uncreate(l))
    self.wait()
