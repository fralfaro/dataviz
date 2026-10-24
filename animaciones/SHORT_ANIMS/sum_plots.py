from manim import *
config.disable_caching = True

class MainScene(Scene):
  PLOT_RANGE = [0, TAU*2]
  def get_axes(self, **kwargs):
    default_config = dict(
      x_range=[*self.PLOT_RANGE, PI/2],
      y_range=[-1, 1, 1],
      x_length=10,
      y_length=1.7,
      axis_config=dict(include_numbers=False),
      tips=False,
    )
    return Axes(**(default_config | kwargs))

  def construct(self):
    ax1 = self.get_axes()
    ax2 = self.get_axes()
    ax3 = self.get_axes(y_range=[-2, 2, 1], y_length=1.7*2)

    f1 = lambda x: np.sin(x*2)
    f2 = np.cos
    f3 = lambda x: f1(x) + f2(x)

    axes = VGroup(ax1, ax2, ax3).arrange(DOWN)
    plots = VGroup(
      ax1.plot(f1, x_range=self.PLOT_RANGE, color=YELLOW),
      ax2.plot(f2, x_range=self.PLOT_RANGE, color=TEAL),
      ax3.plot(f3, x_range=self.PLOT_RANGE, color=RED),
    )
    self.add(axes)
    self.play(Create(plots[0]))
    self.play(Create(plots[1]))
    self.play(
      ReplacementTransform(plots[0].copy(), plots[2]),
      ReplacementTransform(plots[1].copy(), plots[2]),
    )
    self.wait()
