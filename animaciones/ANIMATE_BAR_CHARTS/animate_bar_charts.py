from manim import *
config.disable_caching = True

def get_hsl_color(h, s, l):
  v = l + s * min(l, 1-l)
  s = 0 if v == 0 else 2 * (1-l/v)
  return ManimColor.from_hsv([h, s, v])
# https://docs.manim.community/en/stable/reference/manim.mobject.graphing.probability.BarChart.html#manim.mobject.graphing.probability.BarChart.change_bar_values
class Example1(Scene):
  def construct(self):
    chart = BarChart(
      values=[50, 30, 10, 0, -20],
      bar_names=["one", "two", "three", "four", "five"],
      y_range=[-20, 50, 10],
      y_length=6,
      x_length=10, x_axis_config={"font_size": 36},
    )

    c_bar_lbls = chart.get_bar_labels(font_size=48)
    self.add(chart, c_bar_lbls)



class Example2(Scene):
  def construct(self):
    chart = BarChart(
      values=[50, 30, 10, 0, -20],
      # bar_names=["one", "two", "three", "four", "five"],
      y_range=[-20, 50, 10],
      y_length=6,
      x_length=10, x_axis_config={"font_size": 36},
    )

    self.add(chart)
    self.wait()
    chart.change_bar_values([-20, 0, 10, 30, 50])
    self.wait()


class AbstractScene(Scene):
  def setup(self):
    chart = BarChart(
      values=[0, 50, 50],
      y_range=[0, 100, 10],
      y_length=6.5,
      x_length=7,
      x_axis_config={"font_size": 40},
      bar_names=["H", "S", "L"],
      y_axis_config={
        "decimal_number_config":{
          "unit": "\\%",
          "num_decimal_places": 0
        }
      }
    ).to_edge(LEFT)

    h_lines = VGroup(*[
      Line(chart.c2p(0, x), chart.c2p(3, x), stroke_width=1)
      for x in range(0,110,10)
    ])

    sq = Square(3, fill_opacity=1).next_to(chart, RIGHT, buff=1.7)

    h_r, s_r, l_r = chart.bars
    s_r.set_color(RED)

    self.add(chart, h_lines, sq, *chart.bars)
    self.chart   = chart
    self.sq      = sq
    self.h_lines = h_lines

class Example(AbstractScene):
  def construct(self):
    chart = self.chart
    sq = self.sq
    
    hsl_variables = VGroup(
      DecimalNumber(0),
      DecimalNumber(50),
      DecimalNumber(50),
    )

    h_dn, s_dn, l_dn = hsl_variables

    sq.add_updater(
      lambda mob: mob.set_color(
        get_hsl_color(
          h_dn.get_value() / 100,
          s_dn.get_value() / 100,
          l_dn.get_value() / 100,
        )
      ),
      call_updater=True
    )

    def chart_updater(mob:BarChart):
      hb, sb, lb = mob.bars
      mob.change_bar_values([
        h_dn.get_value(), s_dn.get_value(), l_dn.get_value()
      ])
      h_dn.next_to(hb, UP, buff=0.1)
      s_dn.next_to(sb, UP, buff=0.1)
      l_dn.next_to(lb, UP, buff=0.1)
    
    chart.add_updater(chart_updater, call_updater=True)

    self.add(chart, sq, hsl_variables)
    self.play(
      ChangeDecimalToValue(h_dn, 100),
      # Don't use: h_dn.animate.set_value(100)
      run_time=4
    )
    self.wait()
    self.play(
      ChangeDecimalToValue(h_dn, 20),
      ChangeDecimalToValue(s_dn, 31),
      ChangeDecimalToValue(l_dn, 63),
      run_time=3
    )
    self.wait()

