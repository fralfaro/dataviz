from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    N_ARROWS = 17*3-2
    ax = Axes(
      x_range=[-TAU, TAU, PI/4],
      y_range=[-2, 2, 1],
      x_length=12,
      y_length=5,
      tips=False,
    )
    vt  = ValueTracker(0)
    arr = VGroup(
      Arrow(ORIGIN, UP)
      for _ in range(N_ARROWS)
    )
    arr.arrange(
        RIGHT,
        buff=(ax.x_length-arr[0].width*(N_ARROWS-1))/(N_ARROWS-1)
      ).next_to(ax@(0,0), UP, buff=0)

    def arr_updater(grp:VMobject):
      f = lambda x: np.sin(x + vt.get_value())
      for a in grp:
        x,_ = ax.p2c(a.get_start())
        a.become(
          Arrow(
            a.get_start(),
            ax@(x, f(x)),
            buff=0,
            max_tip_length_to_length_ratio=0.15,
            max_stroke_width_to_length_ratio=4,
          )
        )
      grp.set_color(YELLOW)
    arr.add_updater(arr_updater, call_updater=True)
    self.add(ax, arr)
    self.play(
      vt.animate.set_value(TAU*2),
      run_time=15,
      rate_func=linear
    )
    self.wait()

