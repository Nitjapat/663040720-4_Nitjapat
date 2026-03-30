"663040720-4"
"Nitjapat Supanangthong"

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QDateEdit, QRadioButton,
                             QButtonGroup, QComboBox, QTextEdit, QCheckBox,
                             QPushButton)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("P2: Student Registration")
        self.resize(400, 600)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 20, 15, 20)

        # --- Title ---
        title_label = QLabel("Student Registration Form")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        main_layout.addSpacing(15)

        # --- Basic Information Fields ---
        main_layout.addWidget(QLabel("Full Name:"))
        self.name_input = QLineEdit()
        main_layout.addWidget(self.name_input)

        main_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        main_layout.addWidget(self.email_input)

        main_layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        main_layout.addWidget(self.phone_input)

        main_layout.addSpacing(10)

        # --- Date of Birth ---
        main_layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True) 
        self.date_edit.setDisplayFormat("dd/MM/yyyy") 
        self.date_edit.setDate(QDate(2000, 1, 1)) # Default: Jan 1, 2000
        # Make the date edit roughly half the width to match the image
        self.date_edit.setFixedWidth(150)
        main_layout.addWidget(self.date_edit)

        main_layout.addSpacing(10)

        # --- Gender (Radio Buttons) ---
        main_layout.addWidget(QLabel("Gender:"))
        
        gender_layout = QHBoxLayout()
        self.gender_group = QButtonGroup()

        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.nb_radio = QRadioButton("Non-binary")
        self.pnts_radio = QRadioButton("Prefer not to say")

        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.nb_radio)
        self.gender_group.addButton(self.pnts_radio)

        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addWidget(self.nb_radio)
        gender_layout.addWidget(self.pnts_radio)
        gender_layout.addStretch() # Pushes radio buttons to the left

        main_layout.addLayout(gender_layout)

        main_layout.addSpacing(15)

        # --- Program (Combo Box) ---
        main_layout.addWidget(QLabel("Program:"))
        self.program_combo = QComboBox()
        programs = [
            "Select your program",
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electical Engineering", 
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Power Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ]
        self.program_combo.addItems(programs)
        main_layout.addWidget(self.program_combo)

        main_layout.addSpacing(10)

        # --- About Yourself (Text Edit) ---
        main_layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        self.about_text = QTextEdit()
        self.about_text.setMaximumHeight(100) # Max height limit
        main_layout.addWidget(self.about_text)

        main_layout.addSpacing(15)

        # --- Terms Checkbox ---
        self.terms_checkbox = QCheckBox("I accept the terms and conditions.")
        main_layout.addWidget(self.terms_checkbox)

        main_layout.addSpacing(15)

        # --- Submit Button ---
        submit_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Submit Registration")
        
        # Adding stretches centers the button horizontally
        submit_layout.addStretch()
        submit_layout.addWidget(self.submit_btn)
        submit_layout.addStretch()
        
        main_layout.addLayout(submit_layout)

        # Push everything up
        main_layout.addStretch()

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())