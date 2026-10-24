from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    ax = Axes(
      x_range=[-1, 7, 1], 
      y_range=[-1, 5, 1], 
      x_length=12,
      y_length=7,
    )
    plot = ax.plot(
      lambda x: 0.1 * (x-2) * (x-8) * (x-5) + 2,
      x_range=[1, 6, 0.01],
      color=RED
    )
    area = VMobject()
    
    def area_updater(mob:VMobject, alpha:float):
      dx = interpolate(3, 5, alpha)
      mob.become(
        ax.get_area(plot, [2, dx], opacity=1)
      )
    area_updater(area, 0)

    self.add(ax, plot, area)
    self.wait()
    self.play(
      UpdateFromAlphaFunc(area, area_updater),
      run_time=5
    )
    self.wait()
