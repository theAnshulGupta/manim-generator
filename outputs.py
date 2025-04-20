from manim import *

##############################################################################
#  2.1 Vectors and Linear Equations – Manim Tutorial
#
#  This script produces a tutorial introducing:
#   • A simple 2×2 linear system
#   • The row picture (lines in the xy-plane intersecting)
#   • The column picture (vectors, scalar multiplication & addition)
#
#  Scenes are combined in a single "FullTutorial" class for easy manim execution.
##############################################################################

# Utility function to keep screen text from exceeding frame
FRAME_W, MARGIN = config.frame_width, 0.8
def shrink_to_fit(mobj, margin=MARGIN):
    if mobj.width > FRAME_W - margin:
        mobj.scale_to_fit_width(FRAME_W - margin)
    return mobj

def play_title(scene):
    title = Text("2.1 Vectors and Linear Equations", font_size=60, weight=BOLD)
    st = Text("Solving a system of linear equations in two ways", font_size=36, slant=ITALIC)
    shrink_to_fit(title)
    shrink_to_fit(st)
    st.next_to(title, DOWN, buff=0.5)

    scene.play(Write(title, run_time=2))
    scene.play(FadeIn(st, shift=UP))
    scene.wait(1)
    scene.play(FadeOut(title), FadeOut(st))

def play_two_equations(scene):
    # Show the system:
    #   1) x - 2y = 1
    #   2) 3x + 2y = 11
    eq_title = Text("1) Two equations, two unknowns", font_size=48, weight=BOLD)
    shrink_to_fit(eq_title)
    eq_title.to_edge(UP)

    eqs = VGroup(
        MathTex(r"x - 2y &= 1", font_size=48),
        MathTex(r"3x + 2y &= 11", font_size=48),
    ).arrange(DOWN, buff=0.5)
    eqs.next_to(eq_title, DOWN, buff=0.8)
    for eq in eqs:
        shrink_to_fit(eq)

    scene.play(Write(eq_title))
    scene.play(LaggedStart(*[Write(eq) for eq in eqs], lag_ratio=0.4))
    scene.wait(2)
    scene.play(FadeOut(VGroup(eq_title, eqs)))

def play_row_picture(scene):
    # The "row picture" is the intersection of two lines:
    #   L1: y = (x - 1)/2
    #   L2: y = (11 - 3x)/2
    row_title = Text("2) Row Picture: Lines in the xy-plane", font_size=48, weight=BOLD)
    shrink_to_fit(row_title)
    row_title.to_edge(UP)

    scene.play(Write(row_title))

    # Set up axes
    axes = Axes(
        x_range=[0,6,1],
        y_range=[0,4,1],
        x_length=6,
        y_length=4,
        axis_config={"include_numbers": True}
    ).shift(DOWN*0.5+LEFT*1.5)

    # L1: x - 2y = 1 => y = (x-1)/2
    line1 = axes.plot(lambda x: (x - 1)/2, x_range=[0,5], color=BLUE)
    label1 = MathTex(r"x - 2y = 1", font_size=36, color=BLUE).next_to(line1, UP*0.4)

    # L2: 3x + 2y = 11 => y = (11-3x)/2
    line2 = axes.plot(lambda x: (11 - 3*x)/2, x_range=[0,5], color=GREEN)
    label2 = MathTex(r"3x + 2y = 11", font_size=36, color=GREEN).next_to(line2, DOWN*0.4)

    # Intersection point: Solve system => x=3, y=1
    intersect_dot = Dot(axes.c2p(3,1), color=RED)
    intersect_lbl = Text("(3, 1)", font_size=30, color=RED).next_to(intersect_dot, RIGHT*0.4)

    scene.play(Create(axes))
    scene.play(Create(line1), FadeIn(label1, shift=UP))
    scene.play(Create(line2), FadeIn(label2, shift=DOWN))
    scene.wait(1)
    scene.play(FadeIn(intersect_dot, scale=0.5))
    scene.play(Write(intersect_lbl))
    scene.wait(2)
    scene.play(FadeOut(VGroup(row_title, axes, line1, line2, label1, label2, intersect_dot, intersect_lbl)))

def play_column_equation(scene):
    # Column equation:
    #   [1  -2][x] = [1]
    #   [3   2][y]   [11]
    # Or equivalently: x*(1,3) + y*(-2,2) = (1,11)
    col_title = Text("3) Column Picture: Vector equation", font_size=48, weight=BOLD)
    col_title.to_edge(UP)
    shrink_to_fit(col_title)

    eq = MathTex(
        r"x \begin{bmatrix} 1 \\ 3 \end{bmatrix} \;+\;"
        r"y \begin{bmatrix} -2 \\ 2 \end{bmatrix} \;=\;"
        r"\begin{bmatrix} 1 \\ 11 \end{bmatrix},",
        font_size=42
    ).next_to(col_title, DOWN, buff=0.5)
    scene.play(Write(col_title))
    scene.play(FadeIn(eq, shift=UP))
    scene.wait(2)
    scene.play(FadeOut(VGroup(col_title, eq)))

def play_column_picture(scene):
    # Illustrate vector addition: 3*(1,3) + 1*(-2,2) = (1,11)
    # We'll show axes, the column 1, column 2, and resultant b.

    picture_title = Text("4) Visualizing the column vectors", font_size=48, weight=BOLD)
    shrink_to_fit(picture_title)
    picture_title.to_edge(UP)
    scene.play(Write(picture_title))

    axes = Axes(
        x_range=[-3,5,1],
        y_range=[0,12,2],
        x_length=6,
        y_length=5,
        tips=False
    ).shift(DOWN*1.0 + LEFT*1.5)
    scene.play(Create(axes))

    # Column1 = (1, 3), scaled by 3 => (3, 9)
    # Column2 = (-2, 2)
    # b = (1, 11)
    col1 = np.array([1,3,0])
    col2 = np.array([-2,2,0])
    scale_x, scale_y = 3, 1  # from final solution (x=3,y=1)
    C1scaled = col1 * scale_x # => (3,9)
    C2scaled = col2 * scale_y # => (-2,2)
    bvector  = C1scaled + C2scaled  # => (1,11)

    # Arrows from origin
    arrow_col1 = always_redraw(
        lambda: Arrow(axes.c2p(0,0), axes.c2p(col1[0], col1[1]), color=BLUE, buff=0)
    )
    arrow_3col1 = always_redraw(
        lambda: Arrow(axes.c2p(0,0), axes.c2p(C1scaled[0],C1scaled[1]), color=BLUE, buff=0)
    )
    arrow_col2 = always_redraw(
        lambda: Arrow(axes.c2p(0,0), axes.c2p(col2[0], col2[1]), color=GREEN, buff=0)
    )
    arrow_2col2 = always_redraw(
        lambda: Arrow(axes.c2p(0,0), axes.c2p(C2scaled[0],C2scaled[1]), color=GREEN, buff=0)
    )
    arrow_b = always_redraw(
        lambda: Arrow(axes.c2p(0,0), axes.c2p(bvector[0],bvector[1]), color=RED, buff=0)
    )

    # Labels
    lbl_col1 = MathTex(r"(1,3)", font_size=30, color=BLUE).next_to(axes.c2p(1,3), LEFT)
    lbl_3col1= MathTex(r"3(1,3)=(3,9)", font_size=30, color=BLUE).next_to(axes.c2p(3,9), LEFT)
    lbl_col2 = MathTex(r"(-2,2)", font_size=30, color=GREEN).next_to(axes.c2p(-2,2), LEFT)
    lbl_2col2= MathTex(r"1(-2,2)=(-2,2)", font_size=30, color=GREEN).next_to(axes.c2p(-2,2), DOWN)
    lbl_b    = MathTex(r"(1,11)", font_size=30, color=RED).next_to(axes.c2p(1,11), RIGHT)

    # Animate the progression
    scene.play(Create(arrow_col1), Create(arrow_col2))
    scene.play(FadeIn(lbl_col1), FadeIn(lbl_col2))
    scene.wait(1)

    scene.play(Transform(arrow_col1, arrow_3col1), Transform(lbl_col1, lbl_3col1))
    scene.play(Transform(arrow_col2, arrow_2col2), Transform(lbl_col2, lbl_2col2))
    scene.wait(1)

    # Now the sum b
    scene.play(Create(arrow_b), FadeIn(lbl_b))
    scene.wait(2)

    # Clear
    scene.play(FadeOut(VGroup(
        picture_title, axes, arrow_col1, arrow_3col1, arrow_col2, arrow_2col2, arrow_b,
        lbl_col1, lbl_3col1, lbl_col2, lbl_2col2, lbl_b
    )))

def play_ops(scene):
    # Show "scalar multiplication" and "vector addition"
    # 3*(1,3) = (3,9)
    # (3,9) + (-2,2) = (1,11)

    ops_title = Text("5) Basic Operations in Linear Algebra", font_size=46, weight=BOLD)
    shrink_to_fit(ops_title)
    ops_title.to_edge(UP)
    scene.play(Write(ops_title))

    scal_mult = MathTex(
        r"\text{Scalar multiplication: } 3 \begin{bmatrix} 1 \\ 3 \end{bmatrix} = \begin{bmatrix} 3 \\ 9 \end{bmatrix}",
        font_size=36
    )
    vect_add = MathTex(
        r"\text{Vector addition: } \begin{bmatrix} 3 \\ 9 \end{bmatrix} + \begin{bmatrix} -2 \\ 2 \end{bmatrix} = \begin{bmatrix} 1 \\ 11 \end{bmatrix}",
        font_size=36
    )
    combo = MathTex(
        r"\text{Linear combination: } 3 \begin{bmatrix} 1 \\ 3 \end{bmatrix} + 1 \begin{bmatrix} -2 \\ 2 \end{bmatrix} = \begin{bmatrix} 1 \\ 11 \end{bmatrix}",
        font_size=36
    )

    slides = VGroup(scal_mult, vect_add, combo).arrange(DOWN, buff=0.5)
    shrink_to_fit(slides)
    slides.to_edge(LEFT)
    scene.play(FadeIn(scal_mult, shift=UP))
    scene.wait(1)
    scene.play(FadeIn(vect_add, shift=UP))
    scene.wait(1)
    scene.play(FadeIn(combo, shift=UP))
    scene.wait(2)
    scene.play(FadeOut(VGroup(ops_title, slides)))

def play_conclusion(scene):
    conc = Text("We solved the system using both the row picture and column picture.\nThe intersection is at (3,1), producing the vector (1,11).",
                font_size=36, slant=ITALIC)
    shrink_to_fit(conc)
    scene.play(Write(conc, run_time=5))
    scene.wait(3)
    scene.play(FadeOut(conc))

class FullTutorial(Scene):
    def construct(self):
        play_title(self)
        play_two_equations(self)
        play_row_picture(self)
        play_column_equation(self)
        play_column_picture(self)
        play_ops(self)
        play_conclusion(self)