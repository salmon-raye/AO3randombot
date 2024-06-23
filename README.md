# AO3 Random Fic Finder Telegram Bot

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/stockpic_bot) [![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)

This Telegram bot finds a random Archive of Our Own (AO3) story based on your chosen tags.

## Features

* **Tag-Based Search:** Easily set keywords to narrow down your search.
* **Random Selection:** Get a surprise AO3 story each time you use the bot.
* **Simple Commands:** Easy-to-remember commands for setting and retrieving your tags.

## Commands

* `/set`: Set your search criteria
* `/show`: Show your current search criteria
* `/random`: Get a random AO3 fic based on your tags

## How to Use

1. **Find the Bot:** Search for "@stockpic_bot" (disregard the weird bot username lol) on Telegram and start a chat.
2. **Set Your Tags:** Use the `/set` command followed by your comma-separated tags (e.g., `/set Harry Potter angst`).
3. **Get a Random Fic:** Use the `/random` command to get a randomly selected fic matching your tags.

## Caveats

* Uses a very old version of telegram-python-bot and modified ao3-api packages
* Can't handle much traffic because it is synchronous 
