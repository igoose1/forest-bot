==========
forest-bot
==========

Run bot
=======

Get ``API_ID`` and ``API_HASH`` from https://my.telegram.org/, ask `@BotFather
<https://t.me/BotFather/>`_ for ``BOT_TOKEN``, find out ``FOREST_CHAT_ID``
yourself.

* ``pip install pip-tools``

* ``pip-sync``

* ``export API_ID=123 API_HASH=XYZ BOT_TOKEN=XYZ FOREST_CHAT_ID=-123``

* ``python -m forest-bot``

Run linter checks and tests
===========================

* ``pip-sync requirements.txt dev-requirements.txt``

* ``./codequality``
