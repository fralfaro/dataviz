from manim import *
from math import comb
config.disable_caching = True

class Cell(VGroup):
  def __init__(self, tex, size=0.7, fade=0.5, height_buff=0.15):
    s = Square(size).fade(fade)
    t = MathTex(tex)\
      .set(height=s.height-height_buff).move_to(s)
    super().__init__(s, t)

class Example(Scene):
  def construct(self):
    ROWS = 9
    pyramid = VGroup(*[
      VGroup(*[
        Cell(str(comb(row, col)), height_buff=0.33, fade=1)
        for col in range(row+1)
      ]).arrange(RIGHT, buff=0)
      for row in range(ROWS)
    ]).arrange(DOWN, buff=0).set(height=config.frame_height-1)

    extremes = VGroup(*[
      VGroup(row[0], row[-1])
      for row in pyramid
    ])
    hig = SurroundingRectangle(pyramid[1], buff=0)

    self.play(Write(extremes))
    self.play(Create(hig))
    self.play(
      FadeTransform(VGroup(pyramid[1], hig).copy(), pyramid[2][1])
    )
    for row_up, row_down in zip(pyramid[2:-1], pyramid[3:]):
      for i in range(len(row_up)-1):
        act_row = row_up[i:i+2]
        self.play(
          Transform(hig, SurroundingRectangle(act_row, buff=0))
        )
        self.play(
          FadeTransform(VGroup(act_row, hig).copy(), row_down[i+1])
        )
    self.play(Uncreate(hig))
    self.wait()

class CellFill(VGroup):
  def __init__(self, tex, size=0.7, fade=0.5, height_buff=0.15, color=BLUE):
    s = Square(size, stroke_width=1, fill_opacity=1, color=color).fade(fade)
    t = MathTex(tex)\
      .set(height=s.height-height_buff).move_to(s)
    super().__init__(s, t)

class Thumb(Scene):
  def construct(self):
    ROWS = 6
    c_list = [TEAL_E, YELLOW_E, RED_E]
    colors_start = color_gradient(c_list, ROWS)
    colors_end = color_gradient([TEAL_A, YELLOW_A, RED_A], ROWS)
    pyramid = VGroup(*[
      VGroup(*[
        CellFill(
          str(comb(row, col)),
          height_buff=0.33,
          fade=0,
          color=colors_start[row].interpolate(colors_end[row], col/(row+1))
        )
        for col in range(row+1)
      ]).arrange(RIGHT, buff=0)
      for row in range(ROWS)
    ]).arrange(DOWN, buff=0).set(height=config.frame_height-1)
    pyramid.to_edge(LEFT)
    t = Tex(r"Pascal\\Triangle\\with\\Manim")[0].set(height=config.frame_height-1).to_edge(RIGHT)
    t.set_color_by_gradient(*c_list)
    t[-5:].set_stroke(width=3)

    self.add(pyramid, t)
