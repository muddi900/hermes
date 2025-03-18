import logging
import json
from typing import Iterator

from ollama import chat, ChatResponse
from playwright.sync_api import sync_playwright, Page


logging.basicConfig(level=logging.DEBUG)


p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

with open("./system_prompt.md") as f:
    messages: list[dict] = [{"role": "system", "content": f.read()}]


def go_to_url(url: str) -> Page:
    page = browser.new_page()
    page.goto(url)
    return page


func_dict = {"go_to_url": go_to_url}


init_prompt = ""


def initial_prompt():
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

    messages.append({"role": "user", "content": init_prompt})

    resp: ChatResponse = chat(
        model="PetrosStav/gemma3-tools:4b",
        messages=messages,
        tools=tools,
    )

    func = resp.message.tool_calls[0].function  # type:ignore
    page = func_dict[func.name](func.arguments["url"])

    site = str(page.inner_html("html"))

    messages.append(
        {
            "role": "tool",
            "content": "",
            "tool_calls": resp.message.model_dump()["tool_calls"],
        }
    )

    return send_site_data(site)


def send_site_data(site_data: str):
    content = f"""
Attached is the website data you need to analyze:

{site_data}

Please analyze the data as per user requirements and provide an output. the original user prompt: {init_prompt}
"""
    messages.append({"role": "user", "content": content})

    resp: Iterator[ChatResponse] = chat(
        model="PetrosStav/gemma3-tools:4b",
        messages=messages,
        stream=True,
    )

    for chunk in resp:
        yield chunk


def main():
    global init_prompt
    while True:
        if not init_prompt:
            init_prompt = input("Enter your prompt:\t")
            if init_prompt.lower() == "exit_prompt":
                break
            resp = initial_prompt()
        print("\n\n")
        for chunk in resp:
            print(chunk["message"]["content"], end="", flush=True)

    p.stop()


if __name__ == "__main__":
    main()
