import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtWidgets import QPushButton, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QDesktopServices, QColor, QPalette
from PySide6.QtCore import QUrl

# Constants
kg = "kilograms"
lb = "pounds"
cm = "centimeters"
m = "meters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 400, 500) # Adjusted size for better fit

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # -- Header (Red background as per screenshot) --
        header_label = QLabel("Adult and Child BMI Calculator")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_label.setStyleSheet("background-color: #A52A2A; color: white; padding: 5px; border-radius: 4px;")
        header_label.setFixedHeight(40)
        self.main_layout.addWidget(header_label)

        # Create an input section object
        # return QWidget
        self.input_section = InputSection()
        self.main_layout.addWidget(self.input_section)
        
        # create an output section object
        # return QWidget
        self.output_section = OutputSection()
        self.main_layout.addWidget(self.output_section)

        # connect signals from clicking submit and clear buttons
        # Note: We access the buttons inside input_section to connect them
        self.input_section.btn_submit.clicked.connect(lambda: self.input_section.submit_reg(self.output_section))
        self.input_section.btn_clear.clicked.connect(lambda: self.input_section.clear_form(self.output_section))


class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 0, 0)

        # Create the linen background container
        self.result_container = QWidget()
        self.result_container.setStyleSheet("background-color: #FAF0E6; border-radius: 5px;")  # Linen color
        
        self.layout = QVBoxLayout(self.result_container)
        self.layout.setAlignment(Qt.AlignTop)

        # 1. "Your BMI" Label
        lbl_title = QLabel("Your BMI")
        lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl_title)

        # 2. BMI Value Label (Big Blue Text)
        self.bmi_text = QLabel("0.00")
        self.bmi_text.setAlignment(Qt.AlignCenter)
        self.bmi_text.setFont(QFont("Arial", 26, QFont.Bold))
        self.bmi_text.setStyleSheet("color: #5d5aff;") # Periwinkle/Blue color
        self.layout.addWidget(self.bmi_text)
        
        self.layout.addSpacing(10)

        # 3. Create the tables/links but hide them initially
        self.adult_table = self.show_adult_table()
        self.child_table = self.show_child_link()

        self.layout.addWidget(self.adult_table)
        self.layout.addWidget(self.child_table)

        # Initial state: Hidden
        self.adult_table.hide()
        self.child_table.hide()
        
        self.layout.addStretch() # Push everything up

        # Add container to main layout
        main_layout.addWidget(self.result_container)


    def show_adult_table(self):
        container = QWidget()
        table_layout = QGridLayout(container)

        # Headers
        label_bmi = QLabel("BMI")
        label_bmi.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout.addWidget(label_bmi, 0, 0, Qt.AlignCenter)
        
        label_cond = QLabel("Condition")
        label_cond.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout.addWidget(label_cond, 0, 1, Qt.AlignLeft)
        
        # Rows
        data = [
            ("< 18.5", "Thin"),
            ("18.5 - 25.0", "Normal"),
            ("25.1 - 30.0", "Overweight"),
            ("> 30.0", "Obese")
        ]

        for i, (bmi_range, condition) in enumerate(data):
            l1 = QLabel(bmi_range)
            l1.setAlignment(Qt.AlignCenter)
            l2 = QLabel(condition)
            table_layout.addWidget(l1, i+1, 0)
            table_layout.addWidget(l2, i+1, 1)

        return container

    def show_child_link(self):
        container = QWidget()
        child_layout = QVBoxLayout(container)

        info = QLabel("For child's BMI interpretation, please click one of the following links.")
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        child_layout.addWidget(info)

        link_layout = QHBoxLayout()
        
        # HTML links
        boy_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf">BMI graph for BOYS</a>')
        girl_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf">BMI graph for GIRLS</a>')
        
        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)
        
        link_layout.addWidget(boy_link, alignment=Qt.AlignCenter)
        link_layout.addWidget(girl_link, alignment=Qt.AlignCenter)

        child_layout.addLayout(link_layout)
        return container
        

    def update_results(self, bmi, age_group):
        # Update text
        self.bmi_text.setText(f"{bmi:.2f}")

        # Show/Hide appropriate widgets
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
        
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        # 1. Age Group
        lbl_age = QLabel("BMI age group:")
        self.combo_age = QComboBox()
        self.combo_age.addItems([adult, child])
        self.layout.addWidget(lbl_age, 0, 0)
        self.layout.addWidget(self.combo_age, 0, 1, 1, 2)

        # 2. Weight
        lbl_w = QLabel("Weight:")
        self.input_weight = QLineEdit()
        self.combo_weight = QComboBox()
        self.combo_weight.addItems([kg, lb])
        self.layout.addWidget(lbl_w, 1, 0)
        self.layout.addWidget(self.input_weight, 1, 1)
        self.layout.addWidget(self.combo_weight, 1, 2)

        # 3. Height
        lbl_h = QLabel("Height:")
        self.input_height = QLineEdit()
        self.combo_height = QComboBox()
        self.combo_height.addItems([cm, m, ft])
        self.layout.addWidget(lbl_h, 2, 0)
        self.layout.addWidget(self.input_height, 2, 1)
        self.layout.addWidget(self.combo_height, 2, 2)

        # 4. Buttons
        self.btn_clear = QPushButton("clear")
        self.btn_submit = QPushButton("Submit Registration")
        self.layout.addWidget(self.btn_clear, 3, 0)
        self.layout.addWidget(self.btn_submit, 3, 1, 1, 2)

    def clear_form(self, output_section):
        # clear input form
        self.input_weight.clear()
        self.input_height.clear()
        self.combo_age.setCurrentIndex(0)
        self.combo_weight.setCurrentIndex(0)
        self.combo_height.setCurrentIndex(0)

        # clear output section
        output_section.clear_result()

    def submit_reg(self, output_section):
        bmi = self.calculate_BMI()
        if bmi is not None:
            age_group = self.combo_age.currentText()
            output_section.update_results(bmi, age_group)
        else:
            output_section.clear_result()

    def calculate_BMI(self):
        try:
            w_text = self.input_weight.text()
            h_text = self.input_height.text()
            
            if not w_text or not h_text:
                return None

            weight = float(w_text)
            height = float(h_text)

            # Convert Weight to Kg
            if self.combo_weight.currentText() == lb:
                weight = weight * 0.453592
            
            # Convert Height to Meters
            h_unit = self.combo_height.currentText()
            if h_unit == cm:
                height = height / 100
            elif h_unit == ft:
                height = height * 0.3048
            
            if height == 0: return 0

            return weight / (height ** 2)

        except ValueError:
            return None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()