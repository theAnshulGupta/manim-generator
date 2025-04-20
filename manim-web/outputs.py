from manim import *

class FullTutorial(Scene):
    def construct(self):
        ###################################
        # INTRO
        ###################################
        title = Text("Transformer Blocks & Layer Normalization", font_size=48)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        ###################################
        # SECTION 1: Transformer Block Equations
        ###################################
        section1_title = Text("1) Intermediate Output Then Layer Norm", font_size=36)
        eq_zprime = MathTex(
            r"z'^{(i)} = W_2^T \,\text{ReLU}\bigl(W_1^T\,u^{(i)}\bigr)",
            font_size=36
        ).next_to(section1_title, DOWN, buff=0.5)
        eq_z = MathTex(
            r"z^{(i)} = \text{LayerNorm}\Bigl(u^{(i)} + z'^{(i)}; \gamma_2, \beta_2\Bigr)",
            font_size=36
        ).next_to(eq_zprime, DOWN, buff=0.5)
        
        self.play(FadeIn(section1_title))
        self.wait(1)
        self.play(Write(eq_zprime))
        self.wait(2)
        self.play(Write(eq_z))
        self.wait(2)
        
        # Fade out first section
        self.play(FadeOut(section1_title), FadeOut(eq_zprime), FadeOut(eq_z))
        
        ###################################
        # SECTION 2: Layer Norm
        ###################################
        section2_title = Text("2) Layer Normalization", font_size=36)
        eq_ln = MathTex(
            r"\text{LayerNorm}(z; \gamma, \beta) \;=\; \gamma\,\frac{z - \mu_z}{\sigma_z} \;+\; \beta",
            font_size=36
        ).next_to(section2_title, DOWN, buff=0.5)
        eq_mu = MathTex(
            r"\mu_z \;=\; \frac{1}{d}\sum_{i=1}^{d}z_i,\quad",
            r"\sigma_z \;=\;\sqrt{\frac{1}{d}\sum_{i=1}^{d}(z_i - \mu_z)^2}\,.",
            font_size=34
        ).next_to(eq_ln, DOWN, buff=0.5)
        
        self.play(FadeIn(section2_title))
        self.wait(1)
        self.play(Write(eq_ln))
        self.wait(2)
        self.play(Write(eq_mu))
        self.wait(2)
        
        # Simple diagram to represent normalization
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=4,
            y_length=3.0,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN, buff=1)
        self.play(Create(axes), run_time=2)
        
        # Some points representing data before normalization
        points_before = VGroup(
            Dot(axes.coords_to_point(1, 3), color=BLUE),
            Dot(axes.coords_to_point(2, 4), color=BLUE),
            Dot(axes.coords_to_point(4, 2), color=BLUE)
        )
        self.play(FadeIn(points_before))
        self.wait(1)
        
        text_mean = Text("Mean & Std. Dev. Adjust", font_size=28).next_to(axes, UP)
        
        self.play(Write(text_mean))
        self.wait(2)
        
        # Transform the points to represent normalized data
        # We'll just shift them closer to the origin for demonstration
        points_after = VGroup(
            Dot(axes.coords_to_point(2, 2), color=YELLOW),
            Dot(axes.coords_to_point(2.5, 2.5), color=YELLOW),
            Dot(axes.coords_to_point(3, 2), color=YELLOW)
        )
        
        self.play(ReplacementTransform(points_before, points_after))
        self.wait(2)
        
        # Fade out
        self.play(FadeOut(section2_title), FadeOut(eq_ln), FadeOut(eq_mu), 
                  FadeOut(axes), FadeOut(points_after), FadeOut(text_mean))
        
        ###################################
        # SECTION 3: Learned Embedding
        ###################################
        section3_title = Text("3) Learned Embedding", font_size=36)
        eq_qkv = MathTex(
            r"Q = XW_q,\quad K = XW_k,\quad V = XW_v",
            font_size=36
        ).next_to(section3_title, DOWN, buff=0.5)
        
        self.play(FadeIn(section3_title))
        self.wait(1)
        self.play(Write(eq_qkv))
        self.wait(2)
        
        # Simple 2D illustration for Q, K, V
        arrow_q = Arrow(LEFT, RIGHT, buff=0.1, color=GREEN).shift(UP*1)
        text_q = Text("Q", font_size=30, color=GREEN).next_to(arrow_q, UP)
        arrow_k = Arrow(LEFT, RIGHT, buff=0.1, color=RED)
        text_k = Text("K", font_size=30, color=RED).next_to(arrow_k, UP)
        arrow_v = Arrow(LEFT, RIGHT, buff=0.1, color=BLUE).shift(DOWN*1)
        text_v = Text("V", font_size=30, color=BLUE).next_to(arrow_v, UP)
        
        group_qkv = VGroup(arrow_q, text_q, arrow_k, text_k, arrow_v, text_v).next_to(eq_qkv, DOWN, buff=0.5)
        self.play(FadeIn(group_qkv))
        self.wait(2)
        
        self.play(
            FadeOut(section3_title),
            FadeOut(eq_qkv),
            FadeOut(group_qkv)
        )

        ###################################
        # SECTION 4: Multi-Head Attention
        ###################################
        section4_title = Text("4) Multi-Head Attention", font_size=36)
        eq_mha = MathTex(
            r"u^{(i)} = W_{h,c}\sum_{h=1}^{H}\sum_{j=1}^{n} \alpha_{ij}^{(h)}\,V_{j}^{(h)}",
            font_size=36
        ).next_to(section4_title, DOWN, buff=0.5)
        eq_ln2 = MathTex(
            r"u^{(i)} = \text{LayerNorm}\Bigl(x^{(i)} + u^{(i)}; \gamma_1, \beta_1\Bigr)",
            font_size=36
        ).next_to(eq_mha, DOWN, buff=0.5)
        
        self.play(FadeIn(section4_title))
        self.wait(1)
        self.play(Write(eq_mha))
        self.wait(2)
        self.play(Write(eq_ln2))
        self.wait(2)
        
        # Quick example "plot"
        # We'll create dots for tokens and highlight one token i
        dot_group = VGroup()
        for i in range(5):
            dot_group.add(Dot(RIGHT*0.8*i, color=WHITE))
        dot_group.move_to(ORIGIN)
        highlight_dot = Dot(dot_group[2].get_center(), color=YELLOW, radius=0.15)
        
        self.play(FadeIn(dot_group))
        self.play(Transform(dot_group[2], highlight_dot))
        self.wait(2)
        
        self.play(
            FadeOut(dot_group),
            FadeOut(section4_title),
            FadeOut(eq_mha),
            FadeOut(eq_ln2)
        )
        
        ###################################
        # SUMMARY
        ###################################
        summary_title = Text("Summary", font_size=44).shift(UP*2)
        summary_text = (
            "• A Transformer block produces an intermediate output.\n"
            "• That output is combined with the original input and normalized.\n"
            "• Parameters (W1, W2, γ, β, etc.) are learned.\n"
            "• Self-attention breaks into Q, K, V for each token.\n"
            "• Multi-head attention gathers weighted sums from each head.\n"
            "• Finally, the result is normalized and fed forward."
        )
        summary_paragraph = Text(summary_text, font_size=28)
        summary_group = VGroup(summary_title, summary_paragraph).arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(summary_group))
        self.wait(6)  # keep on screen for a bit
        self.play(FadeOut(summary_group))
        
        # End
        end_text = Text("End of Tutorial", font_size=40, color=BLUE)
        self.play(FadeIn(end_text))
        self.wait(2)
        self.play(FadeOut(end_text))