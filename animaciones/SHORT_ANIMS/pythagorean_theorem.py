from manim import *
config.disable_caching = True

class MainScene(Scene):
  def construct(self):
    H = 3
    X = 1.5
    Y = np.sqrt(H**2 - X**2)

    theta1 = np.arccos(X / H)
    theta2 = PI / 2 - theta1

    l1 = Line(ORIGIN, RIGHT * H)
    l2 = Line(ORIGIN, RIGHT * X)
    l2.set_angle(theta1)

    t = Polygon(
      l1.get_start(),
      l1.get_end(),
      l2.get_end(),
      joint_type=LineJointType.BEVEL
    ).move_to(ORIGIN)

    sl = Square(X)\
      .next_to(t.get_corner(DL), UR, buff=0)\
      .rotate(theta1, about_point=t.get_corner(DL))
    sr = Square(Y)\
      .next_to(t.get_corner(DR), UL, buff=0)\
      .rotate(-theta2, about_point=t.get_corner(DR))
    sd = Square(H)\
      .next_to(t, DOWN, buff=0)\

    A = Line(t.get_corner(DR), t.get_corner(DR) + LEFT * X)\
      .rotate(-theta2, about_point=t.get_corner(DR)).get_end()
    B = Line(t.get_corner(DL), t.get_corner(DL) + RIGHT * Y)\
      .set_angle(theta1).get_end()

    L1, L2, L3, L4 = sl.get_vertices()
    R1, R2, R3, R4 = sr.get_vertices()
    D1, D2, D3, D4 = sd.get_vertices()

    l1.next_to(t, DOWN, buff=0)
    l3 = l1.copy().next_to(sd, DOWN, buff=0)

    C = l1.get_projection(L4)
    D = l3.get_projection(L4)


    s_style = lambda c: {
      "stroke_width": 0, 
      "fill_opacity": 0.6,
      "fill_color": c,
      "z_index": 10,
    }
    sl_style = s_style(RED)
    sr_style = s_style(BLUE)

    slt = Polygon(A, L2, L3, R4, **sl_style)
    srt = Polygon(R1, B, L3, R4, **sr_style)

    slc = sl.copy().match_style(slt).set_z_index(10)
    src = sr.copy().match_style(srt).set_z_index(10)

    self.add(t, sl, sr, sd, slc, src)
    self.wait(0.5)
    self.play(
      Transform(slc, slt),
      Transform(src, srt),
      run_time=3,
      rate_func=linear
    )
    self.wait()
    #
    self.play(
      Rotate(slc, -PI/2, about_point=L3),
      Rotate(src, PI/2, about_point=R4),
      run_time=3,
      rate_func=linear
    )
    self.wait()
    #
    slt = Polygon(D, C, D2, D3, **sl_style)
    srt = Polygon(C, D, D4, D1, **sr_style)

    self.play(
      Transform(slc, slt),
      Transform(src, srt),
      run_time=3,
      rate_func=linear
    )
    self.wait()
