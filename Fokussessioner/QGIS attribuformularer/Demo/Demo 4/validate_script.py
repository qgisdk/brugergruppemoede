# kabel_form.py – Python-hook til QGIS 3.x / PyQt5
# Live-validering af felterne "Navn" og "Type":
#  • Initialiserer NULL-repræsentationer til tom streng
#  • Låser OK og farver felter røde, hvis tomme eller NULL

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit, QDialogButtonBox

def formOpen(dialog, layer, feature):
    """
    Kører hver gang formen åbnes.
    Dialog = QgsAttributeForm-instans
    """
    # 1) Find widgets i denne dialog via objectName fra .ui
    le_navn = dialog.findChild(QLineEdit,        "Navn")
    le_type = dialog.findChild(QLineEdit,        "Type")
    btn_box = dialog.findChild(QDialogButtonBox, "buttonBox")
    btn_ok  = btn_box.button(QDialogButtonBox.Ok)
    btn_ok.setEnabled(False)
    
    # 2) Tømmer line edit hvis den er NULL
    if le_navn.text() == "NULL":
        le_navn.clear()          
    if le_type.text() == "NULL":
        le_type.clear()

    # 3) Funktion til live-opdatering af UI
    def _update_ui():
        """Opdater farver + lås OK-knap."""
        try:
            rød = "background:#ffc9c9;"
        
            # -------- Navn --------
            if le_navn.text().strip():
                le_navn.setStyleSheet("")        # gyldig → klar baggrund
                navn_ok = True
            else:
                le_navn.setStyleSheet(rød)       # ugyldig → rød
                navn_ok = False
        
            # -------- Type --------
            if le_type.text().strip():
                le_type.setStyleSheet("")        # gyldig → klar baggrund
                type_ok = True
            else:
                le_type.setStyleSheet(rød)       # ugyldig → rød
                type_ok = False
        
            # OK-knap kun aktiv når begge felter er gyldige
            btn_ok.setEnabled(navn_ok and type_ok)
        except RuntimeError:
            # QLineEdit er allerede slettet – ignorer
            return

    # 4) Endelig validering når brugeren klikker OK
    def _validate():
        try:
            if le_navn.text().strip() and le_type.text().strip():
                parent = dialog.parent()
                if hasattr(parent, "accept"):
                    parent.accept()
            else:
                _update_ui()
        except RuntimeError:
            return

    # 5) Initial kørsel og kobling til teksten i felterne
    QTimer.singleShot(0, _update_ui)
    le_navn.textChanged.connect(_update_ui)
    le_type.textChanged.connect(_update_ui)

    # 6) Tag kontrol over OK-knappen: fjern standard handler, bind egen validering
    btn_box.accepted.connect(_validate)
