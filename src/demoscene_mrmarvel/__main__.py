from .app import app
# noinspection PyCompatibility
from curses import wrapper

if __name__ == "__main__":
    wrapper(app)
