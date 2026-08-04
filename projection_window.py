"""Fenetre de projection : affichage plein ecran des resultats sur le 2eme moniteur."""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class ProjectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projection - VoteManager Pro")
        self.setStyleSheet("background-color:#0d0f14; color:#e8eaf2;")
        self.filter_mode = "all"

        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 20, 30, 20)

        self.title_label = QLabel("Vote")
        self.title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color:#4f8ef7;")
        outer.addWidget(self.title_label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.scroll.setWidget(self.content)
        outer.addWidget(self.scroll)

    def set_filter(self, mode):
        self.filter_mode = mode

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.showNormal()
        super().keyPressEvent(event)

    def refresh(self, project):
        self.title_label.setText(project.name or "Vote")

        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        for s in project.sections:
            ranked = s.ranked()
            total = s.total()

            box = QFrame()
            box.setStyleSheet(
                "background:#161921; border:1px solid #2a2f42; border-radius:10px;"
            )
            box_layout = QVBoxLayout(box)

            header = QLabel(f"{s.title or 'Section'}   ·   {total} votes   ·   Top {s.threshold}")
            header.setFont(QFont("Arial", 17, QFont.Weight.Bold))
            header.setStyleSheet("color:#f7c34f; border: none;")
            box_layout.addWidget(header)

            grid = QGridLayout()
            row, col = 0, 0
            shown = 0
            for i, c in enumerate(ranked):
                elected = total > 0 and s.threshold > 0 and i < s.threshold
                if self.filter_mode == "elected" and not elected:
                    continue
                pct = round(c.score / total * 100) if total > 0 else 0
                card = QLabel(
                    f"{i + 1}. {c.name or 'Sans nom'}\n{c.score} voix   ·   {pct}%"
                    + ("   ★ ELU" if elected else "")
                )
                color = "#f7c34f" if elected else "#4f8ef7"
                card.setStyleSheet(
                    f"background:#0d0f14; border:2px solid {color}; "
                    "border-radius:8px; padding:10px; color:#e8eaf2;"
                )
                card.setFont(QFont("Arial", 13))
                grid.addWidget(card, row, col)
                col += 1
                shown += 1
                if col >= 3:
                    col = 0
                    row += 1
            box_layout.addLayout(grid)
            self.content_layout.addWidget(box)

        self.content_layout.addStretch()

    def show_on_secondary(self, app):
        screens = app.screens()
        primary = app.primaryScreen()
        secondary = next((s for s in screens if s != primary), None)
        if secondary:
            geo = secondary.geometry()
            self.setGeometry(geo)
            self.showFullScreen()
            return True
        self.resize(1000, 700)
        self.show()
        return False
