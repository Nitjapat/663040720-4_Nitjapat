"663040720-4"
"Nitjapat Supanangthong"

import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QGridLayout, QLabel, QComboBox, QSpinBox, 
                               QPushButton, QTableWidget, QTableWidgetItem, 
                               QHeaderView, QAbstractItemView, QMessageBox)
from PySide6.QtCore import Qt

class StudentGradeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.students_data = {} # Dictionary to map ID -> Name
        self.init_data()
        self.init_ui()
        self.apply_styles()

    def init_data(self):
        """Reads student data from students.txt into a dictionary."""
        if not os.path.exists("students.txt"):
            QMessageBox.warning(self, "Error", "students.txt not found. Creating a blank one.")
            with open("students.txt", "w") as f:
                f.write("Select Student ID,\n") 
                
        with open("students.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    self.students_data[parts[0].strip()] = parts[1].strip()

    def init_ui(self):
        self.setWindowTitle("P1: Student Scores and Grades")
        self.resize(850, 500)

        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        
        input_layout = QGridLayout()
        input_layout.setHorizontalSpacing(20)
        
        
        input_layout.addWidget(QLabel("Student ID:"), 0, 0, alignment=Qt.AlignRight)
        self.id_combo = QComboBox()
        self.id_combo.addItems(self.students_data.keys())
        self.id_combo.currentTextChanged.connect(self.update_student_name)
        input_layout.addWidget(self.id_combo, 0, 1)

        input_layout.addWidget(QLabel("Student Name:"), 0, 2, alignment=Qt.AlignRight)
        self.name_label = QLabel("")
        self.name_label.setObjectName("nameLabel") # For specific styling
        input_layout.addWidget(self.name_label, 0, 3)

        
        score_layout = QHBoxLayout()
        score_layout.setSpacing(15)

        self.math_spin = self.create_spinbox()
        self.science_spin = self.create_spinbox()
        self.english_spin = self.create_spinbox()

        score_layout.addWidget(QLabel("Math:"))
        score_layout.addWidget(self.math_spin)
        score_layout.addWidget(QLabel("Science:"))
        score_layout.addWidget(self.science_spin)
        score_layout.addWidget(QLabel("English:"))
        score_layout.addWidget(self.english_spin)
        score_layout.addStretch()

        input_layout.addLayout(score_layout, 1, 0, 1, 4)
        main_layout.addLayout(input_layout)

        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.add_btn = QPushButton("Add Student")
        self.add_btn.setObjectName("actionBtn")
        self.add_btn.clicked.connect(self.add_student)

        self.reset_btn = QPushButton("Reset Input")
        self.reset_btn.clicked.connect(self.reset_inputs)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setObjectName("dangerBtn")
        self.clear_btn.clicked.connect(self.clear_table)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.clear_btn)
        main_layout.addLayout(btn_layout)

        
        columns = ["Student ID", "Name", "Math", "Science", "English", "Total", "Average", "Grade"]
        self.table = QTableWidget(0, len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        
        
        self.update_student_name(self.id_combo.currentText())

    def create_spinbox(self):
        """Helper to create a standard 0-100 spinbox."""
        spinbox = QSpinBox()
        spinbox.setRange(0, 100)
        spinbox.setValue(0)
        spinbox.setFixedWidth(80)
        return spinbox

    def apply_styles(self):
        """Apply custom QSS to make the app look modern."""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                background-color: #f4f5f7;
                color: #333;
            }
            QLabel {
                font-weight: bold;
            }
            #nameLabel {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: normal;
                min-width: 200px;
            }
            QComboBox, QSpinBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #fff;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                background-color: #e2e8f0;
                border: 1px solid #cbd5e1;
                color: #475569;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
            }
            #actionBtn {
                background-color: #3b82f6;
                color: white;
                border: none;
            }
            #actionBtn:hover {
                background-color: #2563eb;
            }
            #dangerBtn {
                background-color: #ef4444;
                color: white;
                border: none;
            }
            #dangerBtn:hover {
                background-color: #dc2626;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 6px;
                border: 1px solid #eee;
                font-weight: bold;
            }
        """)

  

    def update_student_name(self, student_id):
        name = self.students_data.get(student_id, "")
        self.name_label.setText(name)

    def add_student(self):
        student_id = self.id_combo.currentText()
        if not student_id or student_id == "Select Student ID":
            QMessageBox.warning(self, "Warning", "Please select a valid Student ID.")
            return

        name = self.name_label.text()
        math_score = self.math_spin.value()
        sci_score = self.science_spin.value()
        eng_score = self.english_spin.value()

        
        total = math_score + sci_score + eng_score
        average = total / 3.0
        
        if average >= 80: grade = "A"
        elif average >= 70: grade = "B"
        elif average >= 60: grade = "C"
        elif average >= 50: grade = "D"
        else: grade = "F"

        
        self.table.setSortingEnabled(False)
        row = self.table.rowCount()
        self.table.insertRow(row)

       
        def create_item(text):
            item = QTableWidgetItem(str(text))
            item.setTextAlignment(Qt.AlignCenter)
            return item

        self.table.setItem(row, 0, create_item(student_id))
        self.table.setItem(row, 1, QTableWidgetItem(name)) 
        self.table.setItem(row, 2, create_item(math_score))
        self.table.setItem(row, 3, create_item(sci_score))
        self.table.setItem(row, 4, create_item(eng_score))
        self.table.setItem(row, 5, create_item(total))
        self.table.setItem(row, 6, create_item(f"{average:.2f}"))
        
        grade_item = create_item(grade)
        if grade == "A":
            grade_item.setBackground(Qt.green)
            grade_item.setForeground(Qt.black)
        elif grade == "F":
            grade_item.setBackground(Qt.red)
            grade_item.setForeground(Qt.white)
            
        self.table.setItem(row, 7, grade_item)

        
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)

    def reset_inputs(self):
        self.id_combo.setCurrentIndex(0)
        self.math_spin.setValue(0)
        self.science_spin.setValue(0)
        self.english_spin.setValue(0)

    def clear_table(self):
        self.table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentGradeCalculator()
    window.show()
    sys.exit(app.exec())