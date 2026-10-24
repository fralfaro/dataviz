from manim import *
config.disable_caching = True

# from https://github.com/3b1b/videos/blob/master/_2019/diffyq/part2/shared_constructs.py
def temperature_to_color(temp, min_temp=-1, max_temp=1):
  colors = [A_COLOR, TEAL, GREEN, YELLOW, ManimColor("#ff0000")]

  alpha = inverse_interpolate(min_temp, max_temp, temp)
  index, sub_alpha = integer_interpolate(
    0, len(colors) - 1, alpha
  )
  return ManimColor.interpolate(
    colors[index], colors[index + 1], sub_alpha
  )
# ===========================================================

class MainScene(ThreeDScene):
  def setup(self):
    self.freq_amplitude_pairs = [
      (1, 0.5),
      (2, 1),
      (3, 0.5),
      (4, 0.3),
      (5, 0.3),
      (7, 0.2),
    ]
    self.surface_resolution = 20
    self.graph_slice_step = 10 / 20
    self.graph_x_min = 0
    self.graph_x_max = 10
    self.max_temp = 90
    self.min_temp = 10
    self.midpoint = 5
    self.default_n_rod_pieces = 20
    self.alpha = 0.1
    self.step_size = 0.05

  def get_graph(self, time=0):
    graph = self.axes.plot(
      lambda x: self.temp_func(x, time),
      x_range=[
        self.graph_x_min,
        self.graph_x_max,
        self.step_size
      ]
    )
    graph.time = time
    graph.color_using_background_image("VerticalTempGradient")
    return graph

  def setup_axes(self):
    self.axes = Axes(
      x_range=[-1, 11, 1],
      y_range=[-10, 100, 10],
      x_length=11,
      y_length=None,
      y_axis_config={
        "unit_size": 0.06,
      }
    )

  def setup_rod(self):
    self.rod = self.get_rod(
      self.graph_x_min,
      self.graph_x_max,
    )

  def construct(self):
    self.setup_axes()
    self.setup_graph()
    self.setup_rod()
    self.add(self.axes, self.graph, self.rod)
    self.show_surface()

  def setup_graph(self):
    self.graph = self.get_graph()

  def show_surface(self):
    axes = self.axes
    graph = self.graph
    t_min = 0
    t_max = 10

    axes_copy = axes.copy()
    self.original_axes = self.axes

    # Set rod final state
    final_graph = self.get_graph(t_max)
    curr_graph = self.graph
    self.graph = final_graph
    final_rod = self.rod.copy()
    final_rod.set_opacity(1)
    self.color_rod_by_graph(final_rod)
    self.graph = curr_graph

    # Time axis
    t_axis = NumberLine(x_range=[t_min, t_max, 1])
    origin = axes.c2p(0, 0)
    t_axis.shift(origin - t_axis.n2p(0))
    time_label = Tex("Time")
    time_label.scale(1.5)
    time_label.next_to(t_axis, UP)
    t_axis.time_label = time_label
    t_axis.add(time_label)
    t_axis.rotate(90 * DEGREES, UP, about_point=origin)

    # New parts of graph
    step = self.graph_slice_step
    graph_slices = VGroup(*[
      self.get_graph(time=t)
        .shift(t * IN)
      for t in np.arange(0, t_max + step, step)
    ])
    graph_slices.set_stroke(width=1)
    graph_slices.set_shade_in_3d(True)

    # Input plane
    x_axis = self.axes.x_axis
    y = axes.c2p(0, 0)[1]
    surface_config = {
      "u_range": (self.graph_x_min, self.graph_x_max),
      "v_range": (t_min, t_max),
      "resolution": self.surface_resolution,
    }
    input_plane = Surface(
      lambda x, t: np.array([
        x_axis.n2p(x)[0],
        y,
        t_axis.n2p(t)[2],
      ]),
      **surface_config,
    )
    input_plane.set_style(
      fill_opacity=0.5,
      fill_color=A_COLOR_B,
      stroke_width=0.5,
      stroke_color=WHITE,
    )

    # Surface
    y_axis = axes.y_axis
    surface = Surface(
      lambda x, t: np.array([
        x_axis.n2p(x)[0],
        y_axis.n2p(self.temp_func(x, t))[1],
        t_axis.n2p(t)[2],
      ]),
      **surface_config,
    )
    surface.set_style(
        fill_opacity=0.1,
        fill_color=GREY_B,
        stroke_width=0.5,
        stroke_color=WHITE,
        stroke_opacity=0.5,
    )

    # Rotate everything on screen and move camera
    # in such a way that it looks the same
    curr_group = Group(*self.get_mobjects())
    curr_group.clear_updaters()
    self.set_camera_orientation(phi=90 * DEGREES)
    mobs = [
      curr_group,
      graph_slices,
      t_axis,
      input_plane,
      surface,
    ]
    for mob in mobs:
      self.orient_mobject_for_3d(mob)

    self.move_camera(
      phi=80 * DEGREES,
      theta=-85 * DEGREES,
      added_anims=[
        Write(input_plane),
        Write(t_axis),
        # FadeOut(self.graph_label_group),
        # self.rod.set_opacity, 1,
        # self.rod.animate.set_opacity(1)
      ]
    )
    self.begin_ambient_camera_rotation()
    self.add(*graph_slices, *self.get_mobjects())
    self.play(
      FadeIn(surface),
      LaggedStart(*[
        TransformFromCopy(graph, graph_slice)
        for graph_slice in graph_slices
      ], lag_ratio=0.02)
    )
    self.wait()

    # Show slices
    self.axes = axes_copy  # So get_graph works...
    slicing_plane = Rectangle(
      stroke_width=0,
      fill_color=WHITE,
      fill_opacity=0.2,
    )
    slicing_plane.set_shade_in_3d(True)
    slicing_plane.replace(
      Line(axes_copy.c2p(0, 0), axes_copy.c2p(10, 100)),
      stretch=True
    )
    self.orient_mobject_for_3d(slicing_plane)

    def get_time_slice(t):
      new_slice = self.get_graph(t)
      new_slice.set_shade_in_3d(True)
      self.orient_mobject_for_3d(new_slice)
      new_slice.shift(t * UP)
      return new_slice

    graph.set_shade_in_3d(True)
    t_tracker = ValueTracker(0)
    graph.add_updater(lambda g: g.become(
      get_time_slice(t_tracker.get_value())
    ))

    self.orient_mobject_for_3d(final_rod)
    final_rod.shift(10 * UP)
    kw = {"run_time": 10, "rate_func": linear}
    self.rod.save_state()
    self.play(
      ApplyMethod(t_tracker.set_value, 10, **kw),
      Transform(self.rod, final_rod, **kw),
      ApplyMethod(slicing_plane.shift, 10 * UP, **kw),
    )
    self.wait()

  def orient_mobject_for_3d(self, mob):
    mob.rotate(
      90 * DEGREES,
      axis=RIGHT,
      about_point=ORIGIN
    )
    return mob

  def get_mbjects(self):
    return self.mobjects

  def temp_func(self, x, t):
    new_x = TAU * x / 10
    return 50 + 20 * np.sum([
      amp *np.sin(freq * new_x) *
      np.exp(-(self.alpha * freq**2) * t)
      for freq, amp in self.freq_amplitude_pairs
    ])

  def get_rod(self, x_min, x_max, n_pieces=None):
    if n_pieces is None:
      n_pieces = self.default_n_rod_pieces
    axes = self.axes
    line = Line(axes.c2p(x_min, 0), axes.c2p(x_max, 0))
    rod = VGroup(*[
      Square()
      for _ in range(n_pieces)
    ])
    rod.arrange(RIGHT, buff=0)
    rod.match_width(line)
    rod.stretch_to_fit_height(0.2)
    rod.move_to(axes.c2p(x_min, 0), LEFT)
    rod.set_fill(opacity=1)
    rod.set_stroke(width=1)
    rod.set_sheen_direction(RIGHT)
    self.color_rod_by_graph(rod)
    return rod


  def color_rod_by_graph(self, rod):
    for piece in rod:
      piece.set_color(color=[
        self.rod_point_to_color(piece.get_left()),
        self.rod_point_to_color(piece.get_right()),
      ])

  def rod_point_to_graph_y(self, point):
    axes = self.axes
    x = axes.x_axis.p2n(point)

    graph = self.graph
    alpha = inverse_interpolate(
      self.graph_x_min,
      self.graph_x_max,
      x,
    )
    return axes.y_axis.p2n(
      graph.point_from_proportion(alpha)
    )

  def y_to_color(self, y):
    y_max = self.max_temp
    y_min = self.min_temp
    alpha = inverse_interpolate(y_min, y_max, y)
    return temperature_to_color(interpolate(-0.8, 0.8, alpha))

  def rod_point_to_color(self, point):
    return self.y_to_color(
      self.rod_point_to_graph_y(point)
    )

  def get_mobjects(self):
    return self.mobjects
