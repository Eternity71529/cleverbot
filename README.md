# **NOTE: THIS PROJECT IS DEPRECATED AND SHOULD NOT BE USED**

# Cleverbot
A basic wrapper for the Cleverbot.io API with Asynchronous Support

Cleverbot.io : [Link](https://cleverbot.io/)

API Documentation: [Cleverbot.io API](https://docs.cleverbot.io)

## Installing

To install the wrapper, just run the following command:

```
python3 -m pip install -U https://github.com/Eternity71529/cleverbot/archive/master.zip
```
## Usage
(Note: actual reply may vary, and will probably make fun of you. This *is* Cleverbot, after all.)
### Non-Async Client
 #### Parameters:
   - api_key = Your API Key
   - user_id = Your API User ID
   - nick(Optional) = The nickname you give to the instance
## Quick Example
```py
>>> from cleverbot import Client
>>> bot = Client(api_key = "Key Here", user_id = "ID Here", nick = "Optional")
>>> bot.ask("Hi. How are you?")
"I'm good, thanks. How are you?"
```
### Async-Client
 #### Parameters:
   - api_key = Your API Key
   - user_id = Your API User ID
   - nick(Optional) = The nickname you give to the instance
   - loop(Optional) = Specify the asynchronous loop
## Quick Example
```py
>>> from cleverbot import AsyncClient
>>> import asyncio
>>> loop = asyncio.get_event_loop()
>>> bot = AsyncClient(api_key = "Key Here", user_id = "ID Here", nick = "Optional", loop = loop)
>>> loop.run_until_complete(bot.ask("Hi. How are you?"))
"I'm good, thanks. How are you?"
```

## Requirements
 - Python 3.4.2+
 - `requests` library
 - `aiohttp` library

       
