from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    ax = Axes(
      x_range=[-TAU, TAU, PI/4],
      y_range=[-1.5, 1.5, 1],
      x_length=12,
      y_length=6,
    )
    plot = VMobject()
    vt_left  = ValueTracker(-PI)
    vt_right = ValueTracker(PI)

    bg_plot = ax.plot(np.sin, x_range=ax.x_range[:2], stroke_width=2)

    def plot_updater(mob:VMobject):
      mob.become(
        ax.plot(
          np.sin,
          x_range=[
            vt_left.get_value(),
            vt_right.get_value(),
          ],
          stroke_width=8,
          color=RED
        )
      )
    plot.add_updater(
      plot_updater,
      call_updater=True
    )

    self.add(ax, bg_plot, plot)
    self.wait()
    self.play(
      vt_left.animate.set_value(-PI/2),
      run_time=2,
    )
    self.wait()
    self.play(
      vt_right.animate.set_value(TAU * 0.8),
      run_time=2,
    )
    self.wait()
    self.play(
      vt_right.animate.set_value(PI),
      vt_left.animate.set_value(-PI),
      run_time=2,
    )
    self.wait()
