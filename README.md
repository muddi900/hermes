# Hermes

A virtual assistant in the vein Manus, but open source and able to run locally.

## Why?
In short, because I can.

In long, because the means of AI production(tkaddLink) need to be democratized. It seems needlessly grandiose and pretentious, but we all know what happened when we let the web to be centralized.

More people should have access to these tools using their own compute resources.


## Current State
Right now it is just visiting a web site on a chromium window and try to chat with it. I am using ollama and a tool-running variant of google's Gemma3(`PetrosStav/gemma3-tools:4b`). Mostly because of the large context window.

## How to run

I am running on python 3.13, but it should work on 3.10+. Navigate to the folder you want clone this repo:

```bash
git clone #url
cd hermes
python -m venv env
```
Activate the virtual environment. For macos/linux:

```bash
source env/bin/activate
```

For windows powershell:

```powershell
env/Scripts/activate
```