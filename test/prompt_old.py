import os
from typing import List, Dict, Any
import base64
import anthropic
from dotenv import load_dotenv

load_dotenv()

def b64_local(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

class Anthropic:
    MODEL_TYPE = "gpt-4-vision-preview"  # Using GPT-4 Vision for image processing
    
    @staticmethod
    def create_message(messages, temperature=0.3, system=None):
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
        
        # Anthropic expects system message as a separate parameter
        messages_with_system = []
        if system:
            messages_with_system.append({"role": "system", "content": system})
        messages_with_system.extend(messages)
        
        response = client.chat.completions.create(
            model=Anthropic.MODEL_TYPE,
            max_tokens=4000,
            messages=messages_with_system,
            temperature=temperature
        )

        return response.choices[0].message.content

system = """
You are an agent that is an expert at Manim, a Python library that can be compiled to create video tutorials for educational materials. Your task is to take in a textbook chapter covering some material and create an educational tutorial using Manim, detailing technical parts of the textbook to make it intuitive. The idea is to have different sections covering the topic, with visualizations of mathematical concepts and explanatory text as needed. 

First, understand the topic at hand. If there are multiple, focus on the first one and then iterate through the rest. Then, understand how the textbook conveys material and equations. If there is a lot of material to cover, break it up into sections, processing each section at a time. Make it such that a beginner new to this field understands it.

Ensure that your Manim tutorial goes in depth to each of these topics, creating a detailed video of at least a minute explaining the topic, having an example, and ending in a summary. Compile all the events in a term called FullTutorial. Additionally, if you need to include equations, ensure that you write it in latex that can be compiled accurately. Use other materials like graphs or plots as well. When writing the steps of each topic using the Manim Community library in Python, ensuring that your code works correctly. Output a valid solution that can be run, producing a correct video without any errors whatsoever. Ensure that the text all fits in the screen and does not overlap with one another.
"""

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ""

# Process image if it exists
image_process = []
input_image = "input/screenshot.png"  # Update this path to your actual image
if os.path.exists(input_image):
    screenshot = b64_local(input_image)
    if screenshot:
        image_process.append({
            "role": "user",
            "content": [{
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": screenshot
                }
            }]
        })
        user_prompt = Anthropic.create_message(image_process)
    else:
        user_prompt = "Error processing image"
else:
    user_prompt = "No input image found"

# Build prompt chain
prompt_chain = []

# Add example conversations
examples_dir = "examples"
i = 1
while True:
    in_file = os.path.join(examples_dir, f"{i}.in.txt")
    out_file = os.path.join(examples_dir, f"{i}.out.txt")
    
    if not (os.path.exists(in_file) and os.path.exists(out_file)):
        break
        
    user_content = read_file_content(in_file)
    if user_content:
        prompt_chain.append({
            "role": "user",
            "content": [{"type": "text", "text": user_content}]
        })
    
    assistant_content = read_file_content(out_file)
    if assistant_content:
        prompt_chain.append({
            "role": "assistant",
            "content": [{"type": "text", "text": assistant_content}]
        })
    
    i += 1

# Add the current user prompt
print(user_prompt)
prompt_chain.append({"role": "user", "content": [{"type": "text", "text": user_prompt}]})

# Get final response
output = Anthropic.create_message(prompt_chain, system=system)
print(output)