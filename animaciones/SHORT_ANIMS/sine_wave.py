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
    vt   = ValueTracker(0)

    def plot_updater(mob:VMobject):
      mob.become(
        ax.plot(
          lambda x: np.sin(x + vt.get_value()),
          x_range=ax.x_range[:2]
        )
      )
    plot.add_updater(
      plot_updater,
      call_updater=True
    )

    self.add(ax, plot)
    self.wait()
    self.play(
      vt.animate.set_value(TAU),
      run_time=10,
      rate_func=linear,
    )
    self.wait()
