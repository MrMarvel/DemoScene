"""
Подобие некой Демо-сцены
"""
import time
# noinspection PyCompatibility
from curses import wrapper
from curses import resize_term, window, cbreak, noecho
from fps_limiter import FPSCounter, LimitFPS
import cursor
import numpy as np


def app(std: window) -> None:
    """
    Основная функция программы.
    :param std: Окно программы
    """
    cursor.hide()
    resize_term(60, 90)
    fps_counter = FPSCounter()
    fps_limiter = LimitFPS(fps=30)
    std.clear()
    std.addstr("Application started!")
    # max_y, max_x = std.getmaxyx()
    std.refresh()
    noecho()
    cbreak()
    std.nodelay(True)
    frame = 1
    d = Donut()
    ch = std.getch()
    while True:
        if ch >= 0:
            if chr(ch).lower() == 'q':
                break
        if not fps_limiter():
            continue
        std.addstr(1, 0, str())
        std.addstr(f"Frame #{frame} FPS {fps_counter()}")
        # pad = curses.newpad(100, 100)
        # d.draw(pad)
        # pad.refresh(1, 0, 0, 0, max_y - 1, max_x - 1)
        d.draw(std)
        std.refresh()
        time.sleep(0.01)
        frame += 1
        ch = std.getch()
    cursor.show()


class Donut:
    """
    Класс Доната, точнее пончика)
    """
    def __init__(self):
        self.screen_size = 40
        self.theta_spacing = 0.07
        self.phi_spacing = 0.02
        self.illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

        self.A = 1
        self.B = 1
        self.R1 = 1
        self.R2 = 2
        self.K2 = 5
        self.K1 = self.screen_size * self.K2 * 3 / (8 * (self.R1 + self.R2))

    def render_frame(self) -> np.ndarray:
        """
        Рендер модели.
        В основу взял: https://www.a1k0n.net/2011/07/20/donut-math.html
        :rtype: np.ndarray
        """
        cos_A = np.cos(self.A)
        sin_A = np.sin(self.A)
        cos_B = np.cos(self.B)
        sin_B = np.sin(self.B)

        output = np.full((self.screen_size, self.screen_size), " ")  # (40, 40)
        zbuffer = np.zeros((self.screen_size, self.screen_size))  # (40, 40)

        cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, self.phi_spacing))  # (315,)
        sin_phi = np.sin(phi)  # (315,)
        cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, self.theta_spacing))  # (90,)
        sin_theta = np.sin(theta)  # (90,)
        circle_x = self.R2 + self.R1 * cos_theta  # (90,)
        circle_y = self.R1 * sin_theta  # (90,)

        x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T  # (90, 315)
        y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T  # (90, 315)
        z = ((self.K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T  # (90, 315)
        ooz = np.reciprocal(z)  # Calculates 1/z
        xp = (self.screen_size / 2 + self.K1 * ooz * x).astype(int)  # (90, 315)
        yp = (self.screen_size / 2 - self.K1 * ooz * y).astype(int)  # (90, 315)
        L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi,
                                                                         cos_theta)) - sin_A * sin_theta)  # (315, 90)
        L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))  # (315, 90)
        L = np.around(((L1 + L2) * 8)).astype(int).T  # (90, 315)
        mask_L = L >= 0  # (90, 315)
        chars = self.illumination[L]  # (90, 315)

        for i in range(90):
            mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  # (315,)

            zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
            output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

        return output

    @staticmethod
    def print(array: np.ndarray, std: window) -> None:
        """Pretty print the frame."""
        for i, row in enumerate([" ".join(row) for row in array]):
            std.addstr(i + 2, 0, row)
        # print(*[" ".join(row) for row in array], sep="\n")

    def draw(self, std: window) -> None:
        """
        Рисует кадр.
        :param std: Окно, в которое рисовать
        """
        # for _ in range(self.screen_size * self.screen_size):
        self.A += self.theta_spacing
        self.B += self.phi_spacing
        self.print(self.render_frame(), std)


if __name__ == "__main__":
    wrapper(app)
