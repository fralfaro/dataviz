from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    ITERATIONS = 16

    angles = [
      np.arctan(1 / np.sqrt(i)) if i > 0 else 0
      for i in range(ITERATIONS)
    ]

    t_grp = VGroup(*[
      Polygon(
        ORIGIN,
        RIGHT * np.sqrt(i),
        RIGHT * np.sqrt(i) + UP,
        stroke_width=1,
        fill_opacity=1
      ).rotate(
        sum(angles[:i]),
        about_point=ORIGIN
      ).set_z_index(i)
      for i in range(1, ITERATIONS+1)
    ]).set_color_by_gradient(RED, YELLOW, TEAL)

    t_grp.set(height=config.frame_height-1)
    t_grp.move_to(ORIGIN)

    tex_grp = VGroup(*[
      MathTex("\\sqrt{%i}"%(i+2))
        .scale(0.3)
        .move_to(
          interpolate(t_grp[i].get_start(), t_grp[i].get_anchors()[-2], 0.5)
        )
        .add_background_rectangle(buff=0.05)
        .set_z_index(i+10)
      for i in range(ITERATIONS)
    ])

    # self.add(t_grp, tex_grp)
    for i in range(ITERATIONS):
      if i == 0:
        self.play(
          *map(FadeIn, [t_grp[i], tex_grp[i]])
        )
        self.wait()
        continue
      self.play(
        ReplacementTransform(
          t_grp[i-1].copy()
            .set_z_index(i+1), 
          t_grp[i],
          path_arc=angles[i]
        ),
        TransformFromCopy(tex_grp[i-1], tex_grp[i]),
      )
      self.wait()
