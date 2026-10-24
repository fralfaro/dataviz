from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    plane = NumberPlane()
    v1 = Vector([2, 3], color=RED)
    v2 = Vector([-5, -2], color=BLUE)
    v3 = Arrow(
      ORIGIN,
      v1.get_vector() + v2.get_vector(),
      buff=0,
      color=YELLOW
    )

    self.add(plane)
    self.play(GrowArrow(v1))
    self.play(GrowArrow(v2))
    self.play(v1.animate.shift(v2.get_vector()))
    self.play(GrowArrow(v3))
    self.wait()
