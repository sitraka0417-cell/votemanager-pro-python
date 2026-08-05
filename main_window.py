"""Fenetre principale de controle de VoteManager Pro."""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QSpinBox, QGridLayout, QFileDialog,
    QMessageBox, QInputDialog, QDialog, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from models import Project, Section, Candidate
import storage
from projection_window import ProjectionWindow


class LoadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Charger un projet")
        self.resize(340, 380)
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        for name in storage.list_projects():
            self.list_widget.addItem(QListWidgetItem(name))
        layout.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        open_btn = QPushButton("Ouvrir")
        del_btn = QPushButton("Supprimer")
        close_btn = QPushButton("Fermer")
        open_btn.clicked.connect(self.accept)
        del_btn.clicked.connect(self.delete_selected)
        close_btn.clicked.connect(self.reject)
        btn_row.addWidget(open_btn)
        btn_row.addWidget(del_btn)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def delete_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        storage.delete_project(item.text())
        self.list_widget.takeItem(self.list_widget.row(item))

    def selected_name(self):
        item = self.list_widget.currentItem()
        return item.text() if item else None


class CandidateCard(QFrame):
    def __init__(self, section, candidate, rank, total, elected, on_change):
        super().__init__()
        self.section = section
        self.candidate = candidate
        self.on_change = on_change

        border = "#f7c34f" if elected else "#2a2f42"
        bg = "#1a1500" if elected else "#161921"
        self.setStyleSheet(
            f"QFrame {{ background:{bg}; border:1px solid {border}; border-radius:8px; }}"
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)

        rank_color = "#f7c34f" if elected else "#7a80a0"
        rank_label = QLabel(str(rank))
        rank_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        rank_label.setStyleSheet(f"color:{rank_color}; border:none;")
        rank_label.setFixedWidth(26)
        layout.addWidget(rank_label)

        info_layout = QVBoxLayout()
        self.name_edit = QLineEdit(candidate.name)
        self.name_edit.setPlaceholderText("Nom du candidat")
        self.name_edit.setStyleSheet("background:transparent; border:none; color:#e8eaf2; font-size:13px;")
        self.name_edit.textChanged.connect(self.update_name)
        info_layout.addWidget(self.name_edit)

        pct = round(candidate.score / total * 100) if total > 0 else 0
        elu_tag = "  ★ ELU" if elected else ""
        pct_label = QLabel(f"{pct}%{elu_tag}")
        pct_label.setStyleSheet(f"color:{'#f7c34f' if elected else '#7a80a0'}; border:none; font-size:11px;")
        info_layout.addWidget(pct_label)
        layout.addLayout(info_layout, 1)

        minus_btn = QPushButton("-")
        minus_btn.setFixedSize(28, 28)
        minus_btn.setStyleSheet("background:#2a1010; color:#f76060; border:1px solid #f7606044; border-radius:6px; font-weight:bold;")
        minus_btn.clicked.connect(lambda: self.vote(-1))
        layout.addWidget(minus_btn)

        self.score_spin = QSpinBox()
        self.score_spin.setRange(0, 999999)
        self.score_spin.setValue(candidate.score)
        self.score_spin.setFixedWidth(60)
        self.score_spin.setStyleSheet("background:#0d0f14; color:#4f8ef7; border:1px solid #2a2f42; border-radius:5px; font-weight:bold;")
        self.score_spin.valueChanged.connect(self.set_score)
        layout.addWidget(self.score_spin)

        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(28, 28)
        plus_btn.setStyleSheet("background:#1a3020; color:#3ecf8e; border:1px solid #3ecf8e44; border-radius:6px; font-weight:bold;")
        plus_btn.clicked.connect(lambda: self.vote(1))
        layout.addWidget(plus_btn)

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(24, 24)
        del_btn.setStyleSheet("background:transparent; color:#7a80a0; border:none;")
        del_btn.clicked.connect(self.delete_self)
        layout.addWidget(del_btn)

    def update_name(self, text):
        self.candidate.name = text

    def vote(self, delta):
        self.candidate.score = max(0, self.candidate.score + delta)
        self.on_change()

    def set_score(self, val):
        if val != self.candidate.score:
            self.candidate.score = val
            self.on_change()

    def delete_self(self):
        self.section.candidates = [c for c in self.section.candidates if c.id != self.candidate.id]
        self.on_change()


class SectionWidget(QFrame):
    def __init__(self, section, filter_mode, on_change, on_delete):
        super().__init__()
        self.section = section
        self.on_change = on_change
        self.setStyleSheet("QFrame { background:#161921; border:1px solid #2a2f42; border-radius:10px; }")
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        title_edit = QLineEdit(section.title)
        title_edit.setPlaceholderText("Nom de la section")
        title_edit.setStyleSheet("background:transparent; border:none; color:#4f8ef7; font-size:18px; font-weight:bold;")
        title_edit.textChanged.connect(self.update_title)
        header.addWidget(title_edit, 1)

        header.addWidget(QLabel("Top elu(s) :"))
        threshold_spin = QSpinBox()
        threshold_spin.setRange(0, 999)
        threshold_spin.setValue(section.threshold)
        threshold_spin.valueChanged.connect(self.update_threshold)
        header.addWidget(threshold_spin)

        del_sec_btn = QPushButton("Supprimer section")
        del_sec_btn.setStyleSheet("background:#2a1010; color:#f76060; border:1px solid #f7606044; border-radius:6px; padding:4px 10px;")
        del_sec_btn.clicked.connect(lambda: on_delete(section))
        header.addWidget(del_sec_btn)
        layout.addLayout(header)

        total = section.total()
        stats = QLabel(f"{len(section.candidates)} candidat(s)  ·  {total} votes au total")
        stats.setStyleSheet("color:#7a80a0; font-size:12px;")
        layout.addWidget(stats)

        grid = QGridLayout()
        ranked = section.ranked()
        rank_map = {c.id: i + 1 for i, c in enumerate(ranked)}
        row, col = 0, 0
        for cand in section.candidates:
            rank = rank_map[cand.id]
            elected = total > 0 and section.threshold > 0 and rank <= section.threshold
            if filter_mode == "elected" and not elected:
                continue
            if filter_mode == "non_elected" and elected:
                continue
            card = CandidateCard(section, cand, rank, total, elected, on_change)
            grid.addWidget(card, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1
        layout.addLayout(grid)

        add_row = QHBoxLayout()
        self.add_edit = QLineEdit()
        self.add_edit.setPlaceholderText("+ Ajouter un candidat...")
        self.add_edit.setStyleSheet("background:#0d0f14; border:1px dashed #2a2f42; border-radius:7px; padding:6px; color:#e8eaf2;")
        self.add_edit.returnPressed.connect(self.add_candidate)
        add_row.addWidget(self.add_edit, 1)
        add_btn = QPushButton("Ajouter")
        add_btn.clicked.connect(self.add_candidate)
        add_row.addWidget(add_btn)
        layout.addLayout(add_row)

    def update_title(self, text):
        self.section.title = text

    def update_threshold(self, val):
        self.section.threshold = val
        self.on_change()

    def add_candidate(self):
        name = self.add_edit.text().strip()
        if not name:
            return
        self.section.candidates.append(Candidate(name=name))
        self.add_edit.clear()
        self.on_change()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VoteManager Pro")
        self.resize(1300, 850)
        self.project = Project()
        self.filter_mode = "all"
        self.projection = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # ---- Toolbar ----
        toolbar = QHBoxLayout()
        self.name_edit = QLineEdit(self.project.name)
        self.name_edit.setFixedWidth(200)
        self.name_edit.textChanged.connect(self.update_project_name)
        toolbar.addWidget(self.name_edit)

        add_sec_btn = QPushButton("+ Section")
        add_sec_btn.clicked.connect(self.add_section)
        toolbar.addWidget(add_sec_btn)

        save_btn = QPushButton("Sauvegarder")
        save_btn.clicked.connect(self.save_project)
        toolbar.addWidget(save_btn)

        load_btn = QPushButton("Charger")
        load_btn.clicked.connect(self.load_project)
        toolbar.addWidget(load_btn)

        export_btn = QPushButton("Exporter TXT")
        export_btn.clicked.connect(self.export_txt)
        toolbar.addWidget(export_btn)

        proj_btn = QPushButton("Projeter (2eme ecran)")
        proj_btn.setStyleSheet("background:#3ecf8e; color:#0d1a12; font-weight:bold; padding:6px 10px; border-radius:6px;")
        proj_btn.clicked.connect(self.launch_projection)
        toolbar.addWidget(proj_btn)
        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        # ---- Filter bar ----
        filter_bar = QHBoxLayout()
        filter_bar.addWidget(QLabel("Filtre :"))
        self.filter_buttons = {}
        for key, label in [("all", "Tous"), ("elected", "Elus"), ("non_elected", "Non elus")]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(key == "all")
            btn.clicked.connect(lambda checked, k=key: self.set_filter(k))
            filter_bar.addWidget(btn)
            self.filter_buttons[key] = btn
        filter_bar.addStretch()
        main_layout.addLayout(filter_bar)

        # ---- Scroll area with sections ----
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.sections_container = QWidget()
        self.sections_layout = QVBoxLayout(self.sections_container)
        self.sections_layout.addStretch()
        self.scroll.setWidget(self.sections_container)
        main_layout.addWidget(self.scroll)

        self.refresh_sections()

    # ---- Actions ----
    def update_project_name(self, text):
        self.project.name = text

    def add_section(self):
        self.project.sections.append(Section(title="Nouvelle section"))
        self.refresh_sections()

    def delete_section(self, section):
        reply = QMessageBox.question(self, "Confirmer", "Supprimer cette section ?")
        if reply == QMessageBox.StandardButton.Yes:
            self.project.sections = [s for s in self.project.sections if s.id != section.id]
            self.refresh_sections()

    def set_filter(self, key):
        self.filter_mode = key
        for k, btn in self.filter_buttons.items():
            btn.setChecked(k == key)
        self.refresh_sections()

    def refresh_sections(self):
        while self.sections_layout.count():
            item = self.sections_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        if not self.project.sections:
            empty = QLabel("Aucune section. Cliquez sur '+ Section' pour commencer.")
            empty.setStyleSheet("color:#7a80a0; padding:40px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.sections_layout.addWidget(empty)
        else:
            for section in self.project.sections:
                widget = SectionWidget(section, self.filter_mode, self.on_data_changed, self.delete_section)
                self.sections_layout.addWidget(widget)

        self.sections_layout.addStretch()
        self.sync_projection()

    def on_data_changed(self):
        self.refresh_sections()

    def save_project(self):
        path = storage.save_project(self.project)
        QMessageBox.information(self, "Sauvegarde", f"Projet enregistre :\n{path}")

    def load_project(self):
        dialog = LoadDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.selected_name()
            if name:
                self.project = storage.load_project(name)
                self.name_edit.setText(self.project.name)
                self.refresh_sections()

    def export_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, "Exporter en TXT", f"{self.project.name}.txt", "Texte (*.txt)")
        if not path:
            return
        content = storage.export_txt(self.project, self.filter_mode)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        QMessageBox.information(self, "Export", f"Fichier exporte :\n{path}")

    def launch_projection(self):
        app = QApplication.instance()
        if self.projection is None:
            self.projection = ProjectionWindow()
        self.projection.set_filter(self.filter_mode)
        found = self.projection.show_on_secondary(app)
        self.projection.refresh(self.project)
        msg = "Projection lancee sur le 2eme ecran !" if found else "Projection lancee (1 seul ecran detecte)."
        self.statusBar().showMessage(msg, 4000)

    def sync_projection(self):
        if self.projection is not None and self.projection.isVisible():
            self.projection.set_filter(self.filter_mode)
            self.projection.refresh(self.project)
