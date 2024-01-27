import re
import logging
import requests
from PIL import Image
from openai import OpenAI


logging.basicConfig(
                    level=logging.INFO, 
                    format='[%(asctime)s] %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S'
                )

log = logging.getLogger(__name__)

openai = OpenAI()


def create_recipe_prompt(ingredients):
    prompt = f"Create a detailed recipe based on only the following ingredients: {', '.join(ingredients)}. \n"\
            +f"Additionally, assign a title starting with 'Recipe Title: ' to this recipe. "\

    return prompt


def create_recipe(ingredients):
    recipe_prompt = create_recipe_prompt(ingredients)
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': recipe_prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def get_recipe_title(recipe):
    return re.findall('^.*Recipe Title: .*$', recipe, re.MULTILINE)[0].strip().split('Recipe Title: ')[-1]


def create_image_prompt_from_recipe_title(recipe_title):
    return f"{recipe_title}, professional food photography, 15mm, studio lighting"


def create_image(recipe, image_size):
    recipe_title = get_recipe_title(recipe)
    image_prompt = create_image_prompt_from_recipe_title(recipe_title)
    response = openai.images.generate(
        prompt=image_prompt,
        n=1,
        size=image_size
    )

    return response.data[0].url


if __name__ == '__main__':
    ingredients_input = input("Enter your recipe ingredients as comma separated: ")
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]
    log.info(f'You have entered the following ingredients: {ingredients}')
    
    log.info('Wait! while we are preparing a delicious recipe for you... 🍳')
    recipe = create_recipe(ingredients)
    log.info(recipe)

    log.info('Wait! while we are preparing a stunning image for your recipe... 📷')
    image_size = '512x512'
    image_url = create_image(recipe, image_size)

    image_raw = requests.get(image_url, stream=True).raw
    img = Image.open(image_raw)
    img.show()
