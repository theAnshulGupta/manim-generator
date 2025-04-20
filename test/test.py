# manim -pqh test.py FullTutorial
# Gamma Distribution – an intuitive visual tutorial (~1‑min)

from manim import *
from math import gamma as Gamma, exp, factorial

FRAME_W = config.frame_width
MARGIN = 0.8

def shrink_to_fit(mobj: Mobject, margin: float = MARGIN):
    if mobj.width > FRAME_W - margin:
        mobj.scale_to_fit_width(FRAME_W - margin)
    return mobj

# ────────────────────────────────────────────────────────────────────────────
# Scene helpers
# ────────────────────────────────────────────────────────────────────────────

def play_title(sc: Scene):
    title = Text("The Gamma Distribution", font_size=64, weight=BOLD)
    subtitle = Text("Definition • Properties • Applications", font_size=36, slant=ITALIC)
    shrink_to_fit(title); shrink_to_fit(subtitle)
    subtitle.next_to(title, DOWN, buff=0.4)
    sc.play(Write(title, run_time=2.5))
    sc.play(FadeIn(subtitle, shift=UP, run_time=1.8))
    sc.wait(1)
    sc.play(FadeOut(VGroup(title, subtitle)))


def play_density_definition(sc: Scene):
    header = Text("1. Density Definition", font_size=48, weight=BOLD)
    shrink_to_fit(header).to_edge(UP)

    pdf_ok = MathTex(r"f(x;\alpha,\lambda)=\dfrac{\lambda e^{-\lambda x}(\lambda x)^{\alpha-1}}{\Gamma(\alpha)},\;x\ge0")
    pdf_zero = MathTex(r"f(x;\alpha,\lambda)=0,\;x<0")
    group = VGroup(pdf_ok, pdf_zero).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    group.next_to(header, DOWN, buff=0.6)
    shrink_to_fit(group)

    note = Text("α > 0 (shape)   λ > 0 (rate)", font_size=32, color=GRAY_D)
    note.next_to(group, DOWN, buff=0.5)
    shrink_to_fit(note)

    sc.play(Write(header))
    sc.play(Write(group))
    sc.play(FadeIn(note, shift=UP))
    sc.wait(2)
    sc.play(FadeOut(VGroup(header, group, note)))


def play_gamma_function(sc: Scene):
    header = Text("2. The Gamma Function Γ(α)", font_size=48, weight=BOLD)
    shrink_to_fit(header).to_edge(UP)
    integral = MathTex(r"\Gamma(\alpha)=\int_{0}^{\infty} e^{-y}y^{\alpha-1}\,dy")
    integral.next_to(header, DOWN, buff=0.6)
    sc.play(Write(header)); sc.play(Write(integral)); sc.wait(1)
    ibp = MathTex(r"\Gamma(\alpha)=(\alpha-1)\,\Gamma(\alpha-1)")
    ibp.next_to(integral, DOWN, buff=0.8)
    sc.play(TransformFromCopy(integral, ibp)); sc.wait(2)
    sc.play(FadeOut(VGroup(header, integral, ibp)))


def play_integer_case(sc: Scene):
    header = Text("3. Factorial Connection (α = n ∈ ℕ)", font_size=48, weight=BOLD)
    shrink_to_fit(header).to_edge(UP)
    chain = MathTex(r"\Gamma(n)=(n-1)\Gamma(n-1)=\cdots=(n-1)!")
    chain.next_to(header, DOWN, buff=0.6); shrink_to_fit(chain)
    sc.play(Write(header)); sc.play(Write(chain)); sc.wait(2.5)
    sc.play(FadeOut(VGroup(header, chain)))


def play_waiting_time(sc: Scene):
    header = Text("4. Waiting–Time Interpretation", font_size=48, weight=BOLD)
    shrink_to_fit(header).to_edge(UP)
    desc = Text("Time until n Poisson(λ) events occur is Gamma(n, λ).", font_size=32)
    desc.next_to(header, DOWN, buff=0.4); shrink_to_fit(desc)
    n, lam = 3, 1.0
    axes = Axes(x_range=[0, 12, 2], y_range=[0, 0.25, 0.05], x_length=10, y_length=3.5, axis_config={"include_tip": False}).shift(DOWN*0.4)
    gamma_pdf = lambda t: lam*(lam*t)**(n-1)*exp(-lam*t)/factorial(n-1)
    graph = axes.plot(gamma_pdf, x_range=[0, 12], color=GREEN)
    label = MathTex(rf"n={n},\;\lambda={lam}").next_to(graph, UP)
    sc.play(Write(header)); sc.play(FadeIn(desc, shift=DOWN))
    sc.play(Create(axes)); sc.play(Create(graph), FadeIn(label)); sc.wait(2.5)
    sc.play(FadeOut(VGroup(header, desc, axes, graph, label)))


def play_pdf_plot(sc: Scene):
    header = Text("5. Shape vs. α (λ = 1)", font_size=48, weight=BOLD)
    shrink_to_fit(header).to_edge(UP)

    y_max = 1.2  # ensures α=1 curve fits
    axes = Axes(
        x_range=[0, 15, 3],
        y_range=[0, y_max, 0.2],
        x_length=10,
        y_length=4,
        axis_config={"include_tip": False},
    ).shift(DOWN*0.3)

    colors = [BLUE, GREEN, RED, ORANGE]
    alphas = [1, 2, 3, 5]
    graphs = VGroup()
    for a, col in zip(alphas, colors):
        g = axes.plot(lambda x, a=a: exp(-x)*x**(a-1)/Gamma(a), x_range=[0, 15], color=col)
        graphs.add(g)

    legend_items = [VGroup(Dot(color=c, radius=0.07), Text(f"α = {a}", font_size=26)).arrange(RIGHT, buff=0.15) for a, c in zip(alphas, colors)]
    legend = VGroup(*legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    legend.next_to(axes, RIGHT, buff=0.5); shrink_to_fit(legend)

    sc.play(Write(header)); sc.play(Create(axes))
    for g in graphs: sc.play(Create(g), run_time=1)
    sc.play(FadeIn(legend)); sc.wait(2.5)
    sc.play(FadeOut(VGroup(header, axes, graphs, legend)))


def play_summary(sc: Scene):
    bullet_style = {"font_size": 34}
    line1 = MathTex(r"\bullet\;\text{Density }f(x;\alpha,\lambda)\text{ with shape }\alpha\text{ and rate }\lambda", **bullet_style)
    line2 = MathTex(r"\bullet\;\Gamma\text{-function links to factorial: }\Gamma(n)=(n-1)!", **bullet_style)
    line3 = MathTex(r"\bullet\;\text{Waiting time to }n\text{ Poisson events }\sim\,\text{Gamma}(n,\lambda)", **bullet_style)
    line4 = MathTex(r"\bullet\;\text{Special cases: Exponential }(\alpha=1)\text{, }\chi^{2}(\alpha=n/2,\,\lambda=\tfrac12)", **bullet_style)
    bullets = VGroup(line1, line2, line3, line4).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
    shrink_to_fit(bullets)
    sc.play(Write(bullets, run_time=6)); sc.wait(3); sc.play(FadeOut(bullets))


class FullTutorial(Scene):
    def construct(self):
        play_title(self)
        play_density_definition(self)
        play_gamma_function(self)
        play_integer_case(self)
        play_waiting_time(self)
        play_pdf_plot(self)
        play_summary(self)
