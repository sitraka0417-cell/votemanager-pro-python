"""VoteManager Pro - version bureau Python (PyQt6)."""
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

DARK_STYLE = """
QMainWindow, QWidget { background-color: #0d0f14; color: #e8eaf2; font-family: Arial; font-size: 13px; }
QLineEdit { background:#1e2230; border:1px solid #2a2f42; border-radius:6px; padding:5px; color:#e8eaf2; }
QPushButton { background:#1e2230; border:1px solid #2a2f42; border-radius:6px; padding:6px 12px; color:#e8eaf2; }
QPushButton:hover { background:#2a2f42; }
QPushButton:checked { background:#4f8ef7; color:white; border-color:#4f8ef7; }
QSpinBox { background:#1e2230; border:1px solid #2a2f42; border-radius:5px; padding:3px; color:#e8eaf2; }
QScrollArea { border:none; }
QListWidget { background:#161921; border:1px solid #2a2f42; color:#e8eaf2; }
"""


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
