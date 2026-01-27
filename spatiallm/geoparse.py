from schema import ArticlePlaces
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def get_content():
    src = "/home/mxc/Projects/spatiallm/examples/pizza/food-wine-pizza.txt"
    with open(src, "r") as f:
        return f.read().strip()


def main():
    ARTICLE_TEXT = get_content()

    response = client.responses.parse(
        model="gpt-5-mini",
        text_format=ArticlePlaces,
        input=[
            {
                "role": "user",
                "content": (
                    "Extract the country, city, and pizza place names from the text.\n\n"
                    f"{ARTICLE_TEXT}"
                ),
            }
        ],
    )

    result: ArticlePlaces = response.output_parsed
    print(result.model_dump())


if __name__ == "__main__":
    main()

