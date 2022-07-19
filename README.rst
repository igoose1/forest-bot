======================
A woodsman in Telegram
======================

  Don't want to hold back? Can't help yourself? Need to yell? Want to find
  limits when the bot bans?
  
  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaaaaaaaAAAAAAAAAAAAAAAA

  -- https://t.me/shouting_in_the_woods

This bot guards a chat and removes non-"AAAaaA" messages. The shout is defined
as a text message with "Aa"s in any language or a whitelisted sticker.

Run bot
=======

Don't want to mess with a Python dependency management? Then use Docker:
``docker-compose --build up``.

Otherwise get ``API_ID`` and ``API_HASH`` from https://my.telegram.org/, ask
`@BotFather <https://t.me/BotFather/>`_ for ``BOT_TOKEN``, find out
``FOREST_CHAT_ID`` yourself and follow these steps with Python 3.10 installed:

* ``pip install pip-tools``

* ``pip-sync``

* ``export API_ID=123 API_HASH=XYZ BOT_TOKEN=XYZ FOREST_CHAT_ID=-123``

* ``python -m forest-bot``

Run linter checks and tests
===========================

* ``pip-sync requirements.txt dev-requirements.txt``

* ``./codequality``

See license
===========

Code is licensed under the Apache License. You may obtain a copy of the license
at LICENSE file.
