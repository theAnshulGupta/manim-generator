from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

class GradientDescentTutorial(VoiceoverScene):
    def construct(self):
        # Set up the speech service - using Google TTS for reliability
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        
        # SECTION 1: Introduction
        with self.voiceover("Welcome to this tutorial on gradient descent, a fundamental algorithm in optimization and machine learning."):
            title = Text("Gradient Descent", font_size=72)
            self.play(Write(title))
            self.wait(1)
        
        with self.voiceover("Gradient descent is an iterative optimization algorithm used to find the parameter set that minimizes an objective function."):
            formula = MathTex(r"\Theta^* = \arg\min_{\Theta} J(\Theta)")
            formula.next_to(title, DOWN, buff=0.75)
            self.play(FadeTransform(title, formula))
            self.wait(0.5)
        
        with self.voiceover("Intuitively, imagine a terrain with valleys and hills. Gradient descent starts from a point, looks for the steepest downward direction, and takes a step in that direction."):
            # Clear the screen
            self.play(FadeOut(formula))
            
            # Create a 3D-like terrain visualization (using 2D for simplicity)
            axes = Axes(
                x_range=[-3, 3, 1],
                y_range=[-1, 8, 1],
                axis_config={"include_tip": False},
            )
            
            # Define a function with multiple local minima
            def func(x):
                return 1 + 2 * np.sin(x) + 3 * np.cos(x / 2) + x**2 / 10
            
            graph = axes.plot(func, color=BLUE)
            
            # Add labels
            x_label = axes.get_x_axis_label(r"\Theta")
            y_label = axes.get_y_axis_label(r"J(\Theta)")
            labels = VGroup(x_label, y_label)
            
            surface = VGroup(axes, graph, labels)
            self.play(Create(surface))
            self.wait(0.5)
            
            # Add a dot that will move down the gradient
            dot = Dot(color=RED)
            dot.move_to(axes.c2p(-2, func(-2)))
            self.play(FadeIn(dot))
            
            # Show gradient descent steps
            path = TracedPath(dot.get_center, stroke_width=3, stroke_color=RED)
            self.add(path)
            
            # Create animation for several steps of gradient descent
            for x in [-1.7, -1.4, -1.1, -0.8, -0.5, -0.2, 0.1]:
                target_point = axes.c2p(x, func(x))
                self.play(dot.animate.move_to(target_point), run_time=0.5)
            
            self.wait(0.5)
        
        # SECTION 2: 1D Gradient Descent
        with self.voiceover("Let's start with gradient descent in one dimension. We need an objective function f(θ), its derivative f'(θ), and three hyper-parameters: an initial value, a step size or learning rate η, and an accuracy threshold ε."):
            # Clear screen
            self.play(FadeOut(surface), FadeOut(dot), FadeOut(path))
            
            # Show algorithm parameters
            params_text = VGroup(
                Text("1D Gradient Descent Hyperparameters:", font_size=40),
                Text("• Initial value θ_init", font_size=36),
                Text("• Step size (learning rate) η", font_size=36),
                Text("• Accuracy threshold ε", font_size=36)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            
            self.play(Write(params_text), run_time=2)
            self.wait(0.5)
        
        # SECTION 3: 1D GD Algorithm
        with self.voiceover("The algorithm is simple. We start at our initial position and take steps in the negative direction of the derivative, scaled by our learning rate. This continues until we reach a point where the absolute value of the derivative is less than our accuracy threshold."):
            # Clear screen
            self.play(FadeOut(params_text))
            
            # Create pseudocode for the algorithm
            code = Code(
                code="""
1D-Gradient-Descent(θ_init, η, f, f', ε):
    θ^(0) ← θ_init, t ← 0
    Repeat:
        t ← t + 1
        θ^(t) ← θ^(t-1) - η·f'(θ^(t-1))
    Until |f'(θ^(t))| < ε
    Return θ^(t)
                """,
                language="text",
                font="Monospace",
                font_size=28,
                line_spacing=0.7,
                background_stroke_width=0,
                background="rectangle",
                background_stroke_color=WHITE,
            )
            
            self.play(Write(code))
            self.wait(1)
        
        # SECTION 4: Gradient Descent Example
        with self.voiceover("Let's see gradient descent in action for a simple quadratic function. Here, f(x) = (x - 2)², which has its minimum at x = 2."):
            # Transform the code to the side
            self.play(code.animate.scale(0.8).to_edge(LEFT))
            
            # Create axes for the quadratic function
            axes = Axes(
                x_range=[-1, 5, 1],
                y_range=[0, 10, 1],
                axis_config={"include_tip": False},
                x_length=6,
                y_length=4
            ).shift(RIGHT * 3)
            
            # Define and plot the quadratic function
            def quadratic(x):
                return (x - 2) ** 2
            
            graph = axes.plot(quadratic, color=BLUE)
            
            # Add labels
            x_label = axes.get_x_axis_label("x").shift(RIGHT * 3)
            y_label = axes.get_y_axis_label("f(x)").shift(RIGHT * 3)
            function_label = MathTex("f(x) = (x - 2)^2").scale(0.8).next_to(axes, UP)
            
            graph_group = VGroup(axes, graph, x_label, y_label, function_label)
            self.play(Create(graph_group))
            
            # Add a dot at x=4 (starting point)
            dot = Dot(color=RED)
            dot.move_to(axes.c2p(4, quadratic(4)))
            self.play(FadeIn(dot))
            
            # Create label for dot's position
            x_value = 4.0
            position_label = MathTex(f"x = {x_value:.1f}")
            position_label.next_to(dot, UR, buff=0.1).scale(0.7)
            self.play(FadeIn(position_label))
        
        with self.voiceover("Starting at x = 4 with a learning rate of 0.5, we compute the derivative of our function, which is 2(x - 2), and update our position. Watch as the algorithm converges to the minimum."):
            # Add a derivative label
            derivative_label = MathTex(r"f'(x) = 2(x - 2)").scale(0.8)
            derivative_label.next_to(function_label, DOWN)
            self.play(FadeIn(derivative_label))
            
            # Add a path to trace the dot's movement
            path = TracedPath(dot.get_center, stroke_width=3, stroke_color=RED)
            self.add(path)
            
            # Perform gradient descent steps
            learning_rate = 0.5
            steps = []
            
            for i in range(5):  # 5 steps of gradient descent
                # Calculate gradient
                gradient = 2 * (x_value - 2)
                # Update x
                x_value = x_value - learning_rate * gradient
                # Create target point
                target_point = axes.c2p(x_value, quadratic(x_value))
                # Move dot to target point
                steps.append(dot.animate.move_to(target_point))
                # Update position label
                new_label = MathTex(f"x = {x_value:.3f}")
                new_label.next_to(target_point, UR, buff=0.1).scale(0.7)
                steps.append(Transform(position_label, new_label))
            
            # Animate all steps
            for step in steps:
                self.play(step, run_time=0.8)
            
            # Highlight minimum point
            minimum_dot = Dot(color=GREEN)
            minimum_dot.move_to(axes.c2p(2, 0))
            minimum_label = MathTex("x^* = 2").next_to(minimum_dot, DOWN, buff=0.1).scale(0.7)
            self.play(FadeIn(minimum_dot), FadeIn(minimum_label))
            self.wait(1)
        
        # SECTION 5: Multidimensional Gradient Descent
        with self.voiceover("In multiple dimensions, gradient descent works similarly. Instead of using the derivative, we use the gradient vector, which points in the direction of steepest increase."):
            # Clear everything
            self.play(
                FadeOut(VGroup(code, graph_group, dot, position_label, path, 
                              derivative_label, minimum_dot, minimum_label))
            )
            
            # Show multidimensional gradient formula
            gradient_formula = MathTex(r"\nabla_\Theta f(\Theta) = \begin{bmatrix} \frac{\partial f}{\partial \Theta_1} \\ \vdots \\ \frac{\partial f}{\partial \Theta_m} \end{bmatrix}")
            
            self.play(Write(gradient_formula))
            self.wait(1)
            
            # Show update rule
            update_rule = MathTex(r"\Theta^{(t)} = \Theta^{(t-1)} - \eta \nabla_\Theta f(\Theta^{(t-1)})")
            update_rule.next_to(gradient_formula, DOWN, buff=0.75)
            
            self.play(Write(update_rule))
            self.wait(1)
        
        # SECTION 6: 2D Contour Plot with Gradient Descent
        with self.voiceover("Let's visualize gradient descent in 2D. Imagine a surface where we want to find the lowest point. The gradient at each point tells us the direction of steepest ascent, so we move in the opposite direction."):
            # Clear formulas
            self.play(FadeOut(gradient_formula), FadeOut(update_rule))
            
            # Create a number plane for contour plot
            plane = NumberPlane(
                x_range=[-3, 3, 1],
                y_range=[-3, 3, 1],
                axis_config={"include_tip": False},
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_width": 1,
                    "stroke_opacity": 0.6
                }
            )
            
            # Define a 2D function with a minimum
            def func_2d(x, y):
                return (x**2 + y**2) / 2 + np.sin(x) + np.sin(y)
            
            # Create contour plot (approximated with colors)
            contour = VGroup()
            resolution = 20
            for i in range(-resolution, resolution+1):
                for j in range(-resolution, resolution+1):
                    x, y = i/resolution*3, j/resolution*3
                    z = func_2d(x, y)
                    square = Square(
                        side_length=3/resolution,
                        stroke_width=0,
                        fill_opacity=0.7,
                        fill_color=interpolate_color(BLUE, RED, z/5)
                    )
                    square.move_to(plane.c2p(x, y))
                    contour.add(square)
            
            # Add axes on top for clarity
            axes = NumberPlane(
                x_range=[-3, 3, 1],
                y_range=[-3, 3, 1],
                axis_config={"include_tip": False},
                background_line_style={
                    "stroke_opacity": 0
                }
            )
            
            # Add labels
            x_label = axes.get_x_axis_label(r"\theta_1").shift(RIGHT*0.5)
            y_label = axes.get_y_axis_label(r"\theta_2").shift(UP*0.5)
            title = Text("Contour Plot of Objective Function", font_size=36).to_edge(UP)
            
            self.play(
                FadeIn(contour),
                Create(axes),
                FadeIn(x_label),
                FadeIn(y_label),
                Write(title)
            )
            self.wait(0.5)
        
        with self.voiceover("Let's run gradient descent starting from different points. Watch how the algorithm follows the negative gradient towards the minimum of the function."):
            # Add starting points for gradient descent
            start_points = [
                [-2, 2],
                [2, 2],
                [-2, -2]
            ]
            
            dots = VGroup()
            paths = VGroup()
            
            for start_point in start_points:
                # Create dot at starting position
                dot = Dot(color=YELLOW)
                dot.move_to(axes.c2p(start_point[0], start_point[1]))
                dots.add(dot)
                
                # Create path to trace the dot's movement
                path = TracedPath(dot.get_center, stroke_width=3, stroke_color=YELLOW)
                paths.add(path)
            
            self.play(FadeIn(dots))
            self.add(paths)
            
            # Perform gradient descent
            learning_rate = 0.1
            positions = [[p[0], p[1]] for p in start_points]
            
            for _ in range(20):  # 20 steps
                # Create animations for all dots
                animations = []
                
                for i, pos in enumerate(positions):
                    # Calculate gradients
                    x, y = pos
                    dx = x + np.cos(x)
                    dy = y + np.cos(y)
                    
                    # Update positions
                    new_x = x - learning_rate * dx
                    new_y = y - learning_rate * dy
                    positions[i] = [new_x, new_y]
                    
                    # Create animation
                    target_point = axes.c2p(new_x, new_y)
                    animations.append(dots[i].animate.move_to(target_point))
                
                # Play all animations together
                self.play(*animations, run_time=0.3)
            
            self.wait(1)
        
        # SECTION 7: Stochastic Gradient Descent
        with self.voiceover("Finally, let's briefly touch on Stochastic Gradient Descent or SGD. When the objective function is a sum of many terms, computing the full gradient can be expensive."):
            # Clear everything
            self.play(
                FadeOut(VGroup(contour, axes, dots, paths, x_label, y_label, title))
            )
            
            sgd_title = Text("Stochastic Gradient Descent (SGD)", font_size=44)
            self.play(Write(sgd_title))
            self.wait(0.5)
        
        with self.voiceover("SGD updates with just one or a small batch of data points at each step, making it more computationally efficient for large datasets."):
            sgd_formula = MathTex(r"f(\Theta) = \frac{1}{n}\sum_{i=1}^n f_i(\Theta)")
            sgd_formula.next_to(sgd_title, DOWN, buff=0.75)
            self.play(Write(sgd_formula))
            
            # Show SGD update rule
            sgd_update = MathTex(r"\Theta^{(t)} \gets \Theta^{(t-1)} - \eta(t) \nabla f_i(\Theta^{(t-1)})")
            sgd_update.next_to(sgd_formula, DOWN, buff=0.75)
            self.play(Write(sgd_update))
            self.wait(0.5)
        
        with self.voiceover("SGD has several advantages: It's more efficient for large datasets, it can escape bad local minima due to its inherent noise, and it can sometimes provide better generalization."):
            advantages = VGroup(
                Text("• Efficiency for large datasets", font_size=36),
                Text("• Escaping bad local minima", font_size=36),
                Text("• Better generalization", font_size=36)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            
            advantages.next_to(sgd_update, DOWN, buff=0.75)
            self.play(Write(advantages))
            self.wait(1)
        
        # Conclusion
        with self.voiceover("In conclusion, gradient descent is a powerful optimization algorithm that finds the minimum of a function by iteratively moving in the direction of the steepest decrease. It forms the foundation of many machine learning algorithms and is essential for training complex models."):
            self.play(FadeOut(VGroup(sgd_title, sgd_formula, sgd_update, advantages)))
            
            final_title = Text("Gradient Descent", font_size=72)
            self.play(Write(final_title))
            self.wait(0.5)
            
            final_formula = MathTex(r"\Theta^* = \arg\min_{\Theta} J(\Theta)")
            final_formula.next_to(final_title, DOWN, buff=0.75)
            self.play(Write(final_formula))
            self.wait(2)
            
            self.play(FadeOut(VGroup(final_title, final_formula)))