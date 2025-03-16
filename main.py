import logging

from ollama import chat, ChatResponse
from playwright.sync_api import sync_playwright, Page


logging.basicConfig(level=logging.DEBUG)

func_dict = {"go_to_url": go_to_url}

p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

with open("./system_prompt.md") as f:
    messages = [{"role": "system", "content": f.read()}]


def go_to_url(url: str) -> Page:
    page = browser.new_page()
    page.goto(url)
    return page


def initial_prompt(prompt: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "go_to_url",
                "description": "a function that takes a URL. The url is generated based on the users prompt",
                "parameters": {
                    "type": "object",
                    "url": {
                        "type": "string",
                        "decription": "a url generated based on the users prompt",
                    },
                },
                "required": ["url"],
            },
        }
    ]


def main():

    while True:
        prompt = input("Enter your prompt:\t")

    p.stop()


if __name__ == "__main__":
    main()
