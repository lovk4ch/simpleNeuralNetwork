from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow
from concurrent.futures import ThreadPoolExecutor
import sys

executor = ThreadPoolExecutor(max_workers=2)

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("resources/fonts/TT Supermolot Neue Trial DemiBold.ttf")
    window = MainWindow(executor)
    window.show()

    return app.exec()

if __name__ == "__main__":
    try:
        main()
    finally:
        executor.shutdown(wait=False)
        print("Application exited successfully.")
