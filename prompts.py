import anthropic
import os
import base64
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def llm(prompt_chain):
    response = client.chat.completions.create(
        model="claude-3-7-sonnet-20250219",
        messages=prompt_chain
    )
    return response.choices[0].message.content

system = """
You are an agent that is an expert at Manim, a Python library that can be compiled to create video tutorials for educational materials. Your task is to take in a textbook chapter covering some material and create an educational tutorial using Manim, detailing technical parts of the textbook to make it intuitive. The idea is to have different sections covering the topic, with visualizations of mathematical concepts and explanatory text as needed. 

First, understand the topic at hand. If there are multiple, focus on the first one and then iterate through the rest. Then, understand how the textbook conveys material and equations. If there is a lot of material to cover, break it up into sections, processing each section at a time. Make it such that a beginner new to this field understands it.

Ensure that your Manim tutorial goes in depth to each of these topics, creating a detailed video of at least a minute explaining the topic, having an example, and ending in a summary. Compile all the events in a term called FullTutorial. Additionally, if you need to include equations, ensure that you write it in LaTeX that can be compiled accurately. It is essential that you write safe LaTeX that only uses valid characters and formatting such that there are no issues with it. Use other materials like graphs, diagrams, or plots as well, don't just write bullet points. When writing the steps of each topic using the Manim Community library in Python, ensuring that your code works correctly. Output a valid solution that can be run, producing a correct video without any errors whatsoever. Ensure that the text all fits in the screen and does not overlap with one another. I will provide several example input outputs to you as well initially.
"""

prompt_chain = [
    {"role": "system", "content": system}
]

examples_dir = Path("examples")
inputs_dir = Path("input")
examples = []

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
        
        image_files = sorted([f for f in inputs_dir.glob("*.png")])
        if image_files:
            image_contents = []
            for img_file in image_files:
                base64_image = encode_image(img_file)
                image_contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                })
            
            prompt_chain.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "Based on these instructions and previous examples, generate a valid Manim tutorial using the content in these screenshots. Only include valid Python code as the output that can be compiled into manim (with accurate LaTeX), with no extra text:"},
                    *image_contents
                ]
            })

output = llm(prompt_chain=prompt_chain)
# print(prompt_chain)
print(output)

with open('outputs.py', 'w') as f:
    f.write(output)