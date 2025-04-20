import os
from tqdm import tqdm
import anthropic
from bs4 import BeautifulSoup
import re
from manim import * 

# -------------------------------------------------------------------------------------------

client = anthropic.Anthropic()

INPUT_DIR = "documentation/page_content"
EXAMPLE_DIR = "documentation/examples"
SUMMARY_DIR = "documentation/summary"
MEDIA_OUTPUT_DIR = "documentation/downloaded_media"
VOICEOVER_FILE_NAME = "documentation/voiceover_doc.txt"

SYSTEM = """
You are an agent that is an expert at Manim, a Python library that can be compiled to create video tutorials for educational materials. Your task is to take in a textbook chapter covering some material and create an educational tutorial using Manim, detailing technical parts of the textbook to make it intuitive. Feel free to create a voice over with the manim voiceover feature and explore the documentation. Ensure the absolute highest accuracy possible by using the documentation in order to prevent any mistakes.

First, understand the topic at hand. If there are multiple, focus on the first one and then iterate through the rest. Then, understand how the textbook conveys material and equations. If there is a lot of material to cover, break it up into sections, processing each section at a time. Make it such that a beginner new to this field understands it.

Ensure that your Manim tutorial goes in depth to each of these topics, creating a detailed video of at least a minute explaining the topic, having an example, and ending in a summary. Compile all the events in a term called FullTutorial. Additionally, if you need to include equations, ensure that you write it in LaTeX that can be compiled accurately. It is essential that you write safe LaTeX that only uses valid characters and formatting such that there are no issues with it. Use other materials like graphs or plots as well. When writing the steps of each topic using the Manim Community library in Python, ensuring that your code works correctly. Output a valid solution that can be run, producing a correct video without any errors whatsoever. Ensure that the text all fits in the screen and does not overlap with one another. I will provide several example input outputs to you as well initially.
"""

# -------------------------------------------------------------------------------------------

# Examples
SYSTEM += "\n\n===\nBelow are a few examples\n\n"

for file_name in os.listdir(EXAMPLE_DIR):
    path = os.path.join(EXAMPLE_DIR, file_name)
    
    with open(path, "rb") as f:
        if "in" in file_name:
            SYSTEM += "Input:\n"
        else:
            SYSTEM += "Output:\n"
        
        SYSTEM += str(f.read()) + "\n\n"

# -------------------------------------------------------------------------------------------

# Documentation
SYSTEM += "\n===\nYou will be provided the full documentation of the Manim. You can find the full set of page links and associated summary of the given page of documentation below. To view the actual details of some given documentation, feel free to call the function aivailable to you. Don't be afraid to do tthis as accuracy is your highest priority!\n\n"

for file_name in tqdm(os.listdir(INPUT_DIR)):
    path_html = os.path.join(INPUT_DIR, file_name)
    path_summ = os.path.join(SUMMARY_DIR, file_name.replace("html", "txt"))

    with open(path_html, "rb") as f:
        url = f.readline().decode('utf-8').strip()
    
    with open(path_summ, "rb") as f:
        SYSTEM += f"{url}\n{f.read()}\n\n"

# -------------------------------------------------------------------------------------------

# Voiceover (seperate from rest of documentation so include it fully here)
SYSTEM += "\n\nThe documentation for voiceover is seperate so will be fully included below (no need to look specific voiceover stuff up that's included here)\n\n"

with open(VOICEOVER_FILE_NAME, "rb") as f:
    SYSTEM += str(f.read())

# -------------------------------------------------------------------------------------------

# Helper functions for extracting data
def link_to_file_name(link):
    return link[39:].replace('/', '.')

def extract_text_and_media(path):
    with open(path, "rb") as f:
        data = f.read()
    soup = BeautifulSoup(data, "html.parser")
    media_tags = soup.find_all(["img", "video"])
    marker = "<<<MEDIA>>>"
    media_list = []

    # Get images and replace all of them with marker
    for tag in media_tags:
        if tag.name == "img":
            src = tag.get("src") or tag.get("data‑src")
            media_list.append(("image", src))
        else:
            src = tag.get("src")
            if not src and tag.find("source"):
                src = tag.find("source").get("src")
            media_list.append(("video", src))
        tag.replace_with(marker)

    # Get all the texts and split based on marker
    full_text = soup.get_text()
    parts = [piece.strip() for piece in full_text.split(marker)]

    # Interleave
    result = []
    for i, media in enumerate(media_list):
        if parts[i]:
            result.append(("text", parts[i]))
        result.append(media)
    if len(parts) > len(media_list) and parts[-1]:
        result.append(("text", parts[-1]))

    return result

def construct_message_without_media(content):
    message_content = []
    for t, info in content:
        if t == "image" or t == "video":
            continue
        else:
            message_content.append({ "type": "text", "text": info })

    return { "role": "user", "content": message_content }

# -------------------------------------------------------------------------------------------

def send_query(url):
    path = os.path.join(INPUT_DIR, link_to_file_name(url))

    if not os.path.exists(path):
        return "Provided url {url} does not exist. Please provide an existitng one"
    
    content = extract_text_and_media(path)

    return str(construct_message_without_media(content))

def extract_python_block(text):
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def get_code(prompt):
    caches = 0
    messages = [{
        "role": "user",
        "content": f"""{prompt}

Instructions:
1) Create manim code for a video that facilitates understanding -- try to name the single overarching class "FullTutorial".
2) Please use voiceover if you deem that it will be helpful.
3) Feel free to include a lot of visuals to make the animation look nice. In fact, a shorter video with a bunch of cool visuals is definitely preferred over a longer one with just text.
4) Make sure to reference the documentation (when you are even slightly confused) via the available function in order to maximize accuracy. Avoiding errors is a MUST here!

Here are some extremely important things that you must make sure to follow:
1) AVOID LATEX ERRORS AT ALL COSTS (don't do anything even slightly risky) <-- we need the code to actually run
    a) DO NOT use ANY special unicode or greek characters that might even remotely have a chance of causing issues with some latex interpreters
    b) Be very careful about special characters like &
    c) Be very careful about line breaks and stuff
2) Make sure that you fade all text/images at the appropriate time so nothing lingers for longer than its supposed to. For example, we don't want to see some title or body from several scenes ago persist throughout the whole video. EVERYTHING should be temporary. Triple check this and ensure that NOTHING at all persists. This is one of the most important things.
3) Make sure that there are no run time errors and the code plays. If your task at hand is advanced, you may find it helpful to break it up and ensure each part is correct.
4) Avoid list index errors at all costs. Double and triple check your indexing everytime you access an index. Make sure that the array isn't empty and its not out of bounds. This part is cruicial.
5) Make sure everything stays in frame -- we don't want things like the title or some image being cut out!
6) Make sure that there are no common python syntactical / runtime errors!
7) Make sure that audio is properly integrated with the mp4
"""
}]
    while True:
        # 1) Keep using tool calling until code is generated
        while True:
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=19999,
                temperature=1,
                system=SYSTEM,
                tools = [
                    {
                        "name": "get_specific_documentatino_info",
                        "description": "Gets specific documentation info from provided url",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "URL whose documentation info you want returned."
                                },
                            },
                            "required": ["url"]
                        }
                    }
                ],
                messages=messages
            )

            has_tool_call = False
            
            for info in message.content:
                if info.type == "tool_use":
                    print("[query]\n" + str(info.input["url"]) + "\n")
                    result = send_query(info.input["url"])
                    has_tool_call = True

                    messages.append({
                        "role": "assistant",
                        "content": [info],
                    })
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": info.id,
                            "content": result,
                            # "citations": {"enabled": True}
                        }]
                    })
                    # Update and see if we can cache
                    caches += 1

                    if caches <= 4:
                        messages[-1]["content"][0]["cache_control"] = {"type": "ephemeral"}
                
                else:
                    print("[content]\n" + str(info) + "\n")
                    messages.append({
                        "role": "assistant",
                        "content": [info],
                    })
            
            if not has_tool_call:
                break
        
        # 2) Check the code
        try:
            print("[running code]\n")

            def run_manim(code: str, quality="low_quality"):
                ns = {}
                exec(code, ns)

                # Grab the class we expect
                scene_cls = ns.get("FullTutorial")
                if scene_cls is None:
                    raise ValueError("The provided code did not define a class 'FullTutorial'.")

                with tempconfig({"quality": quality}):
                    scene_cls().render()

            run_manim(extract_python_block(messages[-1]["content"][0].text))

        except Exception as e:
            print("[error]\n" + str(e) + "\n")
            messages.append({ "role": "user", "content": f"Code gave the following error:\n{str(e)}" })
            continue

        break

    return extract_python_block(messages[-1]["content"][0].text)
