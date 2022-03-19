from .bot import bot

__all__ = ("run",)


def run() -> None:
    bot.run_until_disconnected()


if __name__ == "__main__":
    run()
