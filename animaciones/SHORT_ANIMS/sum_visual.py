from manim import *
from random import shuffle
config.disable_caching = True

def piramyd(n):
  return VGroup(*[
    VGroup(Square() for _ in range(j))\
      .arrange(RIGHT,buff=0)
    for j in range(1, n+1)
  ]).arrange(DOWN,buff=0)

class MainScene(Scene):
  def construct(self):
    p = piramyd(7)
    p.set(height=config.frame_height-3)
    down_brace1 = Brace(p,DOWN)
    down_brace1_label = down_brace1.get_tex("n")
    left_brace1 = Brace(p,LEFT)
    left_brace2_label = left_brace1.get_tex("n")
    mobs = [subsubmob for submob in p for subsubmob in submob]
    shuffle(mobs)

    self.play(LaggedStartMap(Create, mobs))
    self.play(
      GrowFromCenter(down_brace1),
      GrowFromCenter(left_brace1),
      Write(down_brace1_label),
      Write(left_brace2_label),
    )
    self.wait(0.5)
    self.play(p.animate.arrange(DOWN,buff=0,aligned_edge=LEFT))
    p_ = p.copy()
    self.add(p_)
    self.play(
      p.animate.to_edge(LEFT,buff=2).set_fill(color=RED,opacity=1),
      p_.animate.to_edge(RIGHT,buff=2).set_fill(color=BLUE,opacity=1),
      FadeOut(down_brace1),
      FadeOut(down_brace1_label),
      FadeOut(left_brace1),
      FadeOut(left_brace2_label),
    )
    del down_brace1, down_brace1_label, left_brace1, left_brace2_label
    self.wait(0.5)
    self.play(
      Rotate(p_,PI,about_point=p_.get_center()),
      run_time=1.7
    )
    self.wait(0.5)
    self.play(
      p.animate.move_to(ORIGIN+LEFT*p[0].width/2),
      p_.animate.move_to(ORIGIN+RIGHT*p[0].width/2),
    )
    down_brace1 = Brace(VGroup(p,p_),DOWN)
    down_brace1_label = down_brace1.get_tex("n+1")
    left_brace1 = Brace(VGroup(p,p_),LEFT)
    left_brace2_label = left_brace1.get_tex("n")
    self.play(
      GrowFromCenter(down_brace1),
      GrowFromCenter(left_brace1),
      Write(down_brace1_label),
      Write(left_brace2_label),
    )
    all_mobs = VGroup(
      vmob
      for vmob in self.mobjects 
      if isinstance(vmob, VMobject)
    )
    self.wait(0.5)
    self.play(all_mobs.animate.to_edge(LEFT))
    formula = MathTex("\\sum_{i=1}^{n}i={","n","(","n+1",")","\\over 2}")
    formula.scale(1.2)
    formula.to_edge(RIGHT,buff=2)
    self.wait(0.5)
    self.play(
      Write(formula[0]),
      Write(formula[2]),
      Write(formula[4:]),
      TransformFromCopy(left_brace2_label[0], formula[1]),
      TransformFromCopy(down_brace1_label[0], formula[3]),
      run_time=4
    )
    self.wait(2)
