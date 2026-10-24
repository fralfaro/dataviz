from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    def parametric_function(t):
      x = 1.5 * np.sin(1.5 * t) * np.cos(t)
      y = 1.2 * np.sin(t) + 0.3 * np.sin(2 * t)
      return [x, y, 0]
    curve = ParametricFunction(
      parametric_function,
      t_range=[0.1, 4 * PI * 0.99, 0.1],
      color=BLUE
    ).scale(2.3)
    tr = Triangle(color=WHITE, fill_opacity=1)\
      .scale(0.1)\
      .rotate(PI/6-PI)\
      .move_to(curve.get_start())

    def tr_updater(mob:Triangle, alpha:float, da=0.0001):
      if hasattr(mob, "saved_state"):
        mob.restore()
      a1 = np.clip(alpha - da, 0, 1)
      a2 = np.clip(alpha + da, 0, 1)
      v  = (
          curve.point_from_proportion(a1)
        - curve.point_from_proportion(a2)
      )
      angle = angle_of_vector(v)
      mob.rotate(angle)
      mob.move_to(
        curve.point_from_proportion(alpha)
      )
    tr.save_state()
    tr_updater(tr, 0)

    self.add(curve, tr)
    self.wait(0.5)
    self.play(
      UpdateFromAlphaFunc(tr, tr_updater),
      run_time=12,
      rate_func=linear
    )
    self.wait()
