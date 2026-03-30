import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QGridLayout, QWidget, QLabel, QLineEdit, QPushButton, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


kg, lb = "kilograms", "pounds"
cm, m, ft = "centimeters", "meters", "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 360, 520)

       
        central = QWidget()
        central.setStyleSheet("background-color: white; color: black;") 
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

       
        head = QLabel("Adult and Child BMI Calculator", alignment=Qt.AlignCenter)
        head.setFont(QFont("Arial", 14, QFont.Bold))
        head.setStyleSheet("background-color: #003366; color: white; padding: 10px; border-radius: 4px;")
        self.layout.addWidget(head)

        
        self.input_section = InputSection()
        self.layout.addWidget(self.input_section)
        
        
        self.output_section = OutputSection()
        self.layout.addWidget(self.output_section)

        
        self.input_section.btn_submit.clicked.connect(lambda: self.input_section.submit_reg(self.output_section))
        self.input_section.btn_clear.clicked.connect(lambda: self.input_section.clear_form(self.output_section))

class OutputSection(QWidget):
    def __init__(self):
        super().__init__()
        self.cont = QWidget()
        self.cont.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 5px;")
        
       
        main_lay = QVBoxLayout(self)
        main_lay.addWidget(self.cont)
        self.res_lay = QVBoxLayout(self.cont)
        self.res_lay.setAlignment(Qt.AlignTop)
        
        
        t = QLabel("Your BMI", alignment=Qt.AlignCenter)
        t.setStyleSheet("border: none; color: black; font-size: 14px;")
        self.res_lay.addWidget(t)
        
      
        self.bmi_text = QLabel("0.00", alignment=Qt.AlignCenter)
        self.bmi_text.setFont(QFont("Arial", 28, QFont.Bold))
        self.bmi_text.setStyleSheet("border: none; color: #003366;")
        self.res_lay.addWidget(self.bmi_text)

        
        self.adult_table = self.show_adult_table()
        self.child_table = self.show_child_link()
        
        self.res_lay.addWidget(self.adult_table)
        self.res_lay.addWidget(self.child_table)
        
        self.clear_result()

    def show_adult_table(self):
        w = QWidget()
        w.setStyleSheet("border: none; color: black;") 
        gl = QGridLayout(w)
        
       
        gl.addWidget(QLabel("BMI", font=QFont("Arial", 10, QFont.Bold)), 0, 0, alignment=Qt.AlignCenter)
        gl.addWidget(QLabel("Condition", font=QFont("Arial", 10, QFont.Bold)), 0, 1, alignment=Qt.AlignLeft)
        
       
        data = [("< 18.5", "Thin"), ("18.5 - 25.0", "Normal"), ("25.1 - 30.0", "Overweight"), ("> 30.0", "Obese")]
        for i, (b, c) in enumerate(data):
            gl.addWidget(QLabel(b, alignment=Qt.AlignCenter), i+1, 0)
            gl.addWidget(QLabel(c), i+1, 1)
        return w

    def show_child_link(self):
        w = QWidget()
        w.setStyleSheet("border: none; color: black;")
        v = QVBoxLayout(w)
        
        lbl = QLabel("For child's BMI interpretation, please click one of the following links.")
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl)
        
        h = QHBoxLayout()
        links = [
            ("BMI graph for BOYS", "https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf"),
            ("BMI graph for GIRLS", "https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf")
        ]
        
        for text, url in links:
            l = QLabel(f'<a href="{url}">{text}</a>')
            l.setOpenExternalLinks(True)  
            l.setAlignment(Qt.AlignCenter)
            h.addWidget(l)
            
        v.addLayout(h)
        return w

    def update_results(self, bmi, age_group):
        self.bmi_text.setText(f"{bmi:.2f}")
        
        if age_group == adult:
            self.adult_table.show()
            self.child_table.hide()
        else:
            self.adult_table.hide()
            self.child_table.show()

    def clear_result(self):
        self.bmi_text.setText("0.00")
        self.adult_table.hide()
        self.child_table.hide()

class InputSection(QWidget):
    def __init__(self):
        super().__init__()
        gl = QGridLayout(self)
        gl.setSpacing(10)
        
       
        lbl_style = "color: black; font-size: 12px;"
        
        
        l1 = QLabel("BMI age group:"); l1.setStyleSheet(lbl_style)
        self.age = QComboBox(); self.age.addItems([adult, child])
        gl.addWidget(l1, 0, 0); gl.addWidget(self.age, 0, 1, 1, 2)

        
        l2 = QLabel("Weight:"); l2.setStyleSheet(lbl_style)
        self.w = QLineEdit()
        self.wu = QComboBox(); self.wu.addItems([kg, lb])
        gl.addWidget(l2, 1, 0); gl.addWidget(self.w, 1, 1); gl.addWidget(self.wu, 1, 2)

        
        l3 = QLabel("Height:"); l3.setStyleSheet(lbl_style)
        self.h = QLineEdit()
        self.hu = QComboBox(); self.hu.addItems([cm, m, ft])
        gl.addWidget(l3, 2, 0); gl.addWidget(self.h, 2, 1); gl.addWidget(self.hu, 2, 2)

       
        btn_style = """
            QPushButton { 
                background-color: white; 
                color: black; 
                border: 2px solid #003366; 
                border-radius: 5px; 
                padding: 6px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E6F0FF; }
            QPushButton:pressed { background-color: #CCE0FF; }
        """
        self.btn_clear = QPushButton("clear")
        self.btn_clear.setStyleSheet(btn_style)
        
        self.btn_submit = QPushButton("Submit Registration")
        self.btn_submit.setStyleSheet(btn_style)
        
        gl.addWidget(self.btn_clear, 3, 0)
        gl.addWidget(self.btn_submit, 3, 1, 1, 2)

    def clear_form(self, output_section):
        self.w.clear()
        self.h.clear()
        self.age.setCurrentIndex(0)
        self.wu.setCurrentIndex(0)
        self.hu.setCurrentIndex(0)
        output_section.clear_result()

    def submit_reg(self, output_section):
        bmi = self.calculate_BMI()
        if bmi is not None:
            output_section.update_results(bmi, self.age.currentText())
        else:
            output_section.clear_result()

    def calculate_BMI(self):
        try:
            
            w_text, h_text = self.w.text(), self.h.text()
            if not w_text or not h_text: return None
            
            w = float(w_text)
            h = float(h_text)

            
            if self.wu.currentText() == lb: w *= 0.453592
            
            hu = self.hu.currentText()
            if hu == cm: h /= 100.0
            elif hu == ft: h *= 0.3048
            
            
            if h <= 0: return None
            return w / (h ** 2)

        except ValueError:
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())