# VoteManager Pro — Version Python (PyQt6)

Application native Windows, sans navigateur ni Chromium embarque. Plus legere
qu'une version Electron.

## Fonctionnalites
- Sections avec seuil "Top N elus"
- Ajout/suppression de candidats, vote +/-, edition directe du score
- Classement automatique + mise en avant des elus (bordure doree)
- Filtres : Tous / Elus / Non elus
- Sauvegarde/chargement de projets (fichiers JSON locaux)
- Export TXT des resultats
- Projection sur 2eme ecran : detection automatique du moniteur secondaire
  (vrai multi-ecran natif Qt, pas de popup a deplacer a la main)

## Tester le code (sur PC avec Python installe)
```
pip install -r requirements.txt
python main.py
```

## Compiler le .exe depuis ton telephone Android (sans PC)

1. Cree un compte GitHub (github.com) si besoin.
2. Cree un nouveau depot **public**, par exemple `votemanager-pro-python`.
3. Envoie (push) tout ce dossier dans le depot, depuis Termux ou l'app GitHub.
   - Le fichier `.github/workflows/build.yml` compile automatiquement le
     `.exe` sur un serveur Windows des que tu push sur `main`.
4. Va dans l'onglet **Actions** du depot -> attends la fin du job
   "Build Windows EXE (Python)" (2-4 minutes).
5. Ouvre le job termine -> section **Artifacts** -> telecharge
   `VoteManagerPro-Windows.zip`. Il contient `VoteManagerPro.exe`,
   pret a lancer sur n'importe quel PC Windows (aucune installation de
   Python necessaire pour l'utilisateur final).

## Compiler sur PC Windows directement
```
pip install -r requirements.txt
pyinstaller --noconfirm --windowed --onefile --name VoteManagerPro --collect-all PyQt6 main.py
```
Le `.exe` sera dans le dossier `dist/`.
