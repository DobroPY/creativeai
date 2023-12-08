from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def generate_divided_scenario(client, base_prompt, num_scenes):
    """
    Generates a detailed scenario for the advertisement and divides it into segments.
    
    :param client: OpenAI client.
    :param base_prompt: Base description of the advertisement.
    :param num_scenes: Number of scenes to divide the scenario into.
    :return: List of divided scene descriptions.
    """
    response = client.completions.create(
            model="text-davinci-003", 
            prompt=f"Create a detailed advertisement scenario: {base_prompt}",
            max_tokens=500 
        )

    complete_scenario = response.choices[0].text.strip()
    divided_scenes = complete_scenario.split('\n\n')[:num_scenes]
    return divided_scenes


def generate_advertisement_collage(client, divided_scenario, scenes, collage_dimensions=(3, 1)):
    """
    Generates a collage of images for an advertisement based on a divided scenario.
    
    :param client: OpenAI client.
    :param divided_scenario: List of scene descriptions.
    :param scenes: Number of different scenes to generate.
    :param collage_dimensions: Dimensions of the collage (columns, rows).
    :return: Collage image.
    """
    images = []

    for i, scene_description in enumerate(divided_scenario):
        try:
            prompt = f"Scene {i + 1}: {scene_description}"
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            images.append(image)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    collage_width = collage_dimensions[0] * 1024
    collage_height = collage_dimensions[1] * 1024
    collage = Image.new('RGB', (collage_width, collage_height))

    for i, image in enumerate(images):
        x = i % collage_dimensions[0] * 1024
        y = i // collage_dimensions[0] * 1024
        collage.paste(image, (x, y))

    return collage