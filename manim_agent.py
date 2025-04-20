import os
import subprocess
import re
import time
import base64
from pathlib import Path
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OAI_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def llm(prompt_chain):
    response = client.chat.completions.create(
        model="o1",
        messages=prompt_chain
    )
    return response.choices[0].message.content


def xml_parser(text, tags):
    pattern = rf"<{tags}>(.*?)</{tags}>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[0].strip() if matches else text

def generate_initial_manim_code():
    """Generate initial Manim code based on input screenshots"""
    system = """
    You are an agent that is an expert at Manim, a Python library that can be compiled to create video tutorials for educational materials. Your task is to take in a textbook chapter covering some material and create an educational tutorial using Manim, detailing technical parts of the textbook to make it intuitive. The idea is to have different sections covering the topic, with visualizations of mathematical concepts and explanatory text as needed. 

    First, understand the topic at hand. If there are multiple, focus on the first one and then iterate through the rest. Then, understand how the textbook conveys material and equations. If there is a lot of material to cover, break it up into sections, processing each section at a time. Make it such that a beginner new to this field understands it.

    Ensure that your Manim tutorial goes in depth to each of these topics, creating a detailed video of at least a minute explaining the topic, having an example, and ending in a summary. Compile all the events in a term called FullTutorial. Additionally, if you need to include equations, ensure that you write it in LaTeX that can be compiled accurately. It is essential that you write safe LaTeX that only uses valid characters and formatting such that there are no issues with it. Use other materials like graphs, diagrams, or plots as well, don't just write bullet points. When writing the steps of each topic using the Manim Community library in Python, ensuring that your code works correctly. Output a valid solution that can be run, producing a correct video without any errors whatsoever. Ensure that the text all fits in the screen and does not overlap with one another.
    """

    prompt_chain = [{"role": "system", "content": system}]

    examples_dir = Path("examples")
    in_files = sorted([f for f in examples_dir.glob("*.in.txt")])
    
    for in_file in in_files:
        out_file = examples_dir / f"{in_file.stem.replace('.in', '.out')}.txt"
        
        if out_file.exists():
            with open(in_file, 'r') as f:
                input_text = f.read()
            with open(out_file, 'r') as f:
                output_text = f.read()
            
            prompt_chain.append({"role": "user", "content": input_text})
            prompt_chain.append({"role": "assistant", "content": output_text})

    inputs_dir = Path("input")
    image_files = sorted([f for f in inputs_dir.glob("*.png")])
    image_contents = []
    
    if image_files:
        for img_file in image_files:
            base64_image = encode_image(img_file)
            image_contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            })
    else:
        print("No input images found in input/ directory")
    
    prompt_chain.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "Based on these instructions and previous examples, generate a valid Manim tutorial using the content in these screenshots. Write your python output in <output></output> tags:"},
            *image_contents
        ]
    })

    output = xml_parser(llm(prompt_chain=prompt_chain), "output")
    print(output)
    
    # Write to outputs.py
    with open('outputs.py', 'w') as f:
        f.write(output)
    
    return output

def create_output_dir():
    """Create output directory if it doesn't exist"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def run_manim_compilation(output_file, max_attempts=5):
    """Run Manim compilation with error handling and automatic fixes"""
    output_dir = create_output_dir()
    attempts = 0
    
    while attempts < max_attempts:
        try:
            result = subprocess.run(
                ["/opt/homebrew/bin/manim", "-pql", output_file, "FullTutorial"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                media_dir = Path("media/videos/outputs/480p15")
                video_files = list(media_dir.glob("*.mp4"))
                
                if video_files:
                    latest_video = max(video_files, key=lambda x: x.stat().st_mtime)
                    
                    timestamp = int(time.time())
                    output_filename = f"tutorial_{timestamp}.mp4"
                    output_path = output_dir / output_filename
                    
                    # Move the video to output directory
                    latest_video.rename(output_path)
                    print(f"Successfully generated video: {output_path}")
                    return True
                else:
                    print("No video file found in media directory")
                    return False
            
            # If compilation failed
            else:
                print(f"Compilation attempt {attempts + 1} failed. Error:")
                print(result.stderr)
                
                with open(output_file, 'r') as f:
                    current_code = f.read()
                
                request = [ {"role": "system", "content": "You are an expert at fixing Manim compilation errors. Fix the code while maintaining its original functionality."},
                        {"role": "user", "content": f"Here is the Manim code that failed to compile:\n\n{current_code}\n\nError message:\n{result.stderr}\n\nPlease provide the fixed code that will compile successfully. Write your python output in <output></output> tags"}]
                fixed_code = xml_parser(llm(request),"output")
                
                with open(output_file, 'w') as f:
                    f.write(fixed_code)
                
                attempts += 1
                print(f"Attempting fix {attempts}/{max_attempts}")
                
        except Exception as e:
            print(f"Unexpected error during compilation: {str(e)}")
            attempts += 1
    
    print(f"Failed to compile after {max_attempts} attempts")
    return False

def main():
    print("Generating initial Manim code from input screenshots...")
    generate_initial_manim_code()
    
    output_file = "outputs.py"
    if not os.path.exists(output_file):
        print(f"Error: {output_file} not found")
        return
    
    success = run_manim_compilation(output_file)
    if success:
        print("Manim compilation completed successfully")
    else:
        print("Manim compilation failed after maximum attempts")

if __name__ == "__main__":
    main() 
