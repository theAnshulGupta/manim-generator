from manim import *

class BinarySearch(Scene):
    def construct(self):
        # Create a sorted array
        arr = [1, 3, 5, 7, 9, 11, 13, 15]
        target = 11
        
        # Create array visualization
        squares = VGroup()
        numbers = VGroup()
        for i, num in enumerate(arr):
            square = Square(side_length=1)
            square.move_to(LEFT * 4 + RIGHT * i)
            squares.add(square)
            
            number = Text(str(num), font_size=24)
            number.move_to(square.get_center())
            numbers.add(number)
        
        # Create target text
        target_text = Text(f"Target: {target}", font_size=24)
        target_text.to_edge(UP)
        
        # Add everything to scene
        self.play(
            Create(squares),
            Write(numbers),
            Write(target_text)
        )
        self.wait(1)
        
        # Binary search visualization
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            
            # Highlight current search range
            range_rect = Rectangle(
                width=right-left+1,
                height=1.2,
                color=YELLOW
            )
            range_rect.move_to(squares[left:right+1].get_center())
            
            # Highlight middle element
            mid_square = squares[mid]
            mid_number = numbers[mid]
            
            self.play(
                Create(range_rect),
                mid_square.animate.set_fill(BLUE, opacity=0.5),
                mid_number.animate.set_color(BLUE)
            )
            self.wait(1)
            
            if arr[mid] == target:
                # Found the target
                self.play(
                    mid_square.animate.set_fill(GREEN, opacity=0.5),
                    mid_number.animate.set_color(GREEN)
                )
                self.wait(1)
                break
            elif arr[mid] < target:
                # Search right half
                left = mid + 1
                self.play(
                    FadeOut(range_rect),
                    squares[:mid+1].animate.set_fill(GRAY, opacity=0.3),
                    numbers[:mid+1].animate.set_color(GRAY)
                )
            else:
                # Search left half
                right = mid - 1
                self.play(
                    FadeOut(range_rect),
                    squares[mid:].animate.set_fill(GRAY, opacity=0.3),
                    numbers[mid:].animate.set_color(GRAY)
                )
            self.wait(1)
        
        self.wait(2) 