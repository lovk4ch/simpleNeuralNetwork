import random

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QLabel


class QGlitchLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.full_text = text
        self.setTextFormat(Qt.TextFormat.RichText)
        self.timers = [QTimer() for _ in range(5)]
        for timer in self.timers:
            timer.timeout.connect(self.glitch)
            timer.start(random.randint(1500, 2500))
        self.restore_text()

    def glitch(self):
        chars = list(self.full_text)
        indices_for_random = [0, 1, 2, 6, 7, 8, 11, 13, 14, 15, 16, 17, 18, 19]
        indices_for_glitch = random.sample(indices_for_random, 1)
        for i in indices_for_glitch:
            chars[i] = f'<span style="color: rgb(155, 155, 155)">{chars[i]}</span>'
        self.setText("".join(chars))
        QTimer.singleShot(250, self.restore_text)

    def restore_text(self):
        self.setText(self.full_text)