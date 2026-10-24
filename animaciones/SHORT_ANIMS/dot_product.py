from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    l = Line(LEFT, RIGHT, stroke_width=2)\
      .scale(5)\
      .rotate(30*DEGREES)\
      .shift(DOWN)
    d1 = Dot(l.point_from_proportion(0.2))
    d2 = Dot(UP*3+RIGHT)
    d3 = Dot(l.get_projection(d2.get_center()))
    dl = DashedLine(d2.get_center(), d3.get_center())
    v1 = Arrow(d1.get_center(), d2.get_center(), buff=0)
    v2 = Arrow(d1.get_center(), d3.get_center(), buff=0)

    self.play(GrowFromCenter(l))
    self.play(
      LaggedStart(
        FadeIn(d1, scale=5),
        FadeIn(d2, scale=5),
        GrowArrow(v1),
        lag_ratio=0.3
      )
    )
    self.play(Create(dl))
    self.play(
      ReplacementTransform(v1.copy(), v2),
      ReplacementTransform(d2.copy(), d3),
      run_time=2.5
    )
    self.wait()
