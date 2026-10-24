from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    N_LINES = 30
    c = Circle(3.5, stroke_color=WHITE, stroke_width=2)
    d = Dot(fill_color="#00C4FF")

    offset = 0
    def d_updater(mob:Dot, dt):
      nonlocal offset
      mob.move_to(
        c.point_at_angle(60 * DEGREES * offset)
      )
      offset += dt

    d.add_updater(d_updater)
    self.add(c, d)

    for n_lines in range(2, N_LINES+1):
      lines = VGroup(*[
        Line(LEFT, RIGHT)
          .set_length(c.width)
          .rotate(PI * i / n_lines)
          .set_stroke(width=2)
        for i in range(n_lines)
      ]).move_to(c.get_center())

      def closure(i=0):
        def proj_updater(mob):
          l = lines[i]
          mob.move_to(
            l.get_projection(d.get_center())
          )
        return proj_updater

      dots = VGroup(*[
        Dot(fill_color="#A100FF")
          .add_updater(closure(i), call_updater=True)
        for i in range(n_lines)
      ])

      self.add(lines, *dots)
      self.wait(2)
      if n_lines < N_LINES:
        self.remove(lines, *dots)
