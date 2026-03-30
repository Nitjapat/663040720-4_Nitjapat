"663040720-4"
"Nitjapat Supanangthong"

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QDateEdit, 
                               QSpinBox, QPushButton, QStackedWidget, 
                               QFrame, QMessageBox)
from PySide6.QtCore import QDate, Qt, Signal

# --- Custom Room Card Widget ---
class RoomCard(QFrame):
    clicked = Signal(str, int)  # Emits (Room Name, Price)

    def __init__(self, name, price):
        super().__init__()
        self.name = name
        self.price = price
        self.selected = False
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(180, 100)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.price_label = QLabel(f"${self.price} / night")
        
        layout.addWidget(self.name_label)
        layout.addWidget(self.price_label)
        layout.setAlignment(Qt.AlignCenter)
        self.update_style()

    def mousePressEvent(self, event):
        self.clicked.emit(self.name, self.price)

    def set_selected(self, is_selected):
        self.selected = is_selected
        self.update_style()

    def update_style(self):
        if self.selected:
            self.setStyleSheet("RoomCard { background-color: #3498db; color: white; border-radius: 8px; }")
        else:
            self.setStyleSheet("RoomCard { background-color: #ecf0f1; color: black; border-radius: 8px; border: 1px solid #bdc3c7; }")

# --- Main Application ---
class CozyStayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay Hotel Booking")
        self.resize(500, 650)
        
        self.selected_room_name = ""
        self.selected_room_price = 0

        # Stacked Widget to manage Page 1 and Page 2
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setup_page1()
        self.setup_page2()

    def setup_page1(self):
        self.page1 = QWidget()
        layout = QVBoxLayout(self.page1)
        layout.setSpacing(15)

        title = QLabel("Booking Information")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Customer Info
        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full Name")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone Number")
        
        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.full_name)
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(self.phone)

        # Dates
        date_layout = QHBoxLayout()
        self.check_in = QDateEdit(QDate.currentDate())
        self.check_in.setCalendarPopup(True)
        self.check_in.setDisplayFormat("dd/MM/yyyy")

        self.check_out = QDateEdit(QDate.currentDate().addDays(1))
        self.check_out.setCalendarPopup(True)
        self.check_out.setDisplayFormat("dd/MM/yyyy")

        date_layout.addWidget(QLabel("Check-in:"))
        date_layout.addWidget(self.check_in)
        date_layout.addWidget(QLabel("Check-out:"))
        date_layout.addWidget(self.check_out)
        layout.addLayout(date_layout)

        # Guests
        self.guests_spin = QSpinBox()
        self.guests_spin.setRange(1, 10)
        self.guests_spin.setSuffix(" guest(s)")
        layout.addWidget(QLabel("Number of Guests:"))
        layout.addWidget(self.guests_spin)

        # Room Selection
        layout.addWidget(QLabel("Select a Room:"))
        room_layout = QHBoxLayout()
        self.cards = [
            RoomCard("Standard Room", 100),
            RoomCard("Deluxe Suite", 250),
            RoomCard("Penthouse", 500)
        ]
        for card in self.cards:
            card.clicked.connect(self.on_room_selected)
            room_layout.addWidget(card)
        layout.addLayout(room_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear Info")
        clear_btn.clicked.connect(self.clear_inputs)
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.go_to_review)
        
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(next_btn)
        layout.addLayout(btn_layout)
        
        self.stack.addWidget(self.page1)

    def setup_page2(self):
        self.page2 = QWidget()
        layout = QVBoxLayout(self.page2)
        layout.setSpacing(10)

        title = QLabel("Review Booking")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("font-size: 14px; line-height: 1.5;")
        self.summary_label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.summary_label)

        self.total_label = QLabel()
        self.total_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2ecc71; margin-top: 20px;")
        layout.addWidget(self.total_label)

        # Buttons
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        confirm_btn = QPushButton("Confirm")
        confirm_btn.clicked.connect(self.show_confirm_dialog)
        
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(confirm_btn)
        layout.addLayout(btn_layout)

        self.stack.addWidget(self.page2)

    def on_room_selected(self, name, price):
        self.selected_room_name = name
        self.selected_room_price = price
        for card in self.cards:
            card.set_selected(card.name == name)

    def go_to_review(self):
        if not self.full_name.text() or not self.selected_room_name:
            QMessageBox.warning(self, "Incomplete", "Please enter your name and select a room.")
            return

        # Calculation
        check_in = self.check_in.date()
        check_out = self.check_out.date()
        nights = check_in.daysTo(check_out)
        if nights < 1: nights = 1
        
        total_price = self.selected_room_price * nights

        summary = (
            f"<b>Room:</b> {self.selected_room_name} (${self.selected_room_price}/night)\n"
            f"<b>Customer:</b> {self.full_name.text()}\n"
            f"<b>Phone:</b> {self.phone.text()}\n"
            f"<b>Stay:</b> {self.check_in.date().toString('dd/MM/yyyy')} to {self.check_out.date().toString('dd/MM/yyyy')}\n"
            f"<b>Duration:</b> {nights} night(s)\n"
            f"<b>Guests:</b> {self.guests_spin.value()}"
        )
        self.summary_label.setText(summary)
        self.total_label.setText(f"Total Price: ${total_price}")
        self.stack.setCurrentIndex(1)

    def show_confirm_dialog(self):
        name = self.full_name.text()
        msg = QMessageBox(self)
        msg.setWindowTitle("Booking Confirmed")
        msg.setText(f"Thank you for booking with us, {name}!")
        msg.setStandardButtons(QMessageBox.Ok)
        if msg.exec() == QMessageBox.Ok:
            self.clear_inputs()
            self.stack.setCurrentIndex(0)

    def clear_inputs(self):
        self.full_name.clear()
        self.phone.clear()
        self.check_in.setDate(QDate.currentDate())
        self.check_out.setDate(QDate.currentDate().addDays(1))
        self.guests_spin.setValue(1)
        self.selected_room_name = ""
        for card in self.cards:
            card.set_selected(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CozyStayApp()
    window.show()
    sys.exit(app.exec())