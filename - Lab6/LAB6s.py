"663040720-4"
"Nitjapat Supanangthong"

import sys
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QScrollArea, QFrame, QFileDialog, QDialog, QLineEdit, 
    QComboBox, QDateEdit, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate, QLocale

PRIORITY_COLORS = {
    "Low": {"bg": "#d4edda", "border": "#28a745", "text": "#155724"},
    "Medium": {"bg": "#cce5ff", "border": "#007bff", "text": "#004085"},
    "High": {"bg": "#fff3cd", "border": "#ffc107", "text": "#856404"},
    "Critical": {"bg": "#f8d7da", "border": "#dc3545", "text": "#721c24"}
}

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel("<b>New Task</b>")
        layout.addWidget(title_label)
        
        task_layout = QHBoxLayout()
        task_layout.addWidget(QLabel("Task:"))
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task name...")
        task_layout.addWidget(self.task_input)
        layout.addLayout(task_layout)
        
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("Priority:"))
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High", "Critical"])
        priority_layout.addWidget(self.priority_input)
        layout.addLayout(priority_layout)
        
        deadline_layout = QHBoxLayout()
        deadline_layout.addWidget(QLabel("Deadline:"))
        self.deadline_input = QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate())
        deadline_layout.addWidget(self.deadline_input)
        layout.addLayout(deadline_layout)
        
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.add_btn = QPushButton("Add Task")
        self.add_btn.setStyleSheet("background-color: #3b82f6; color: white; font-weight: bold; padding: 5px;")
        self.add_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.add_btn)
        layout.addLayout(btn_layout)

    def get_task_data(self):
        return {
            "title": self.task_input.text().strip(),
            "deadline": self.deadline_input.date().toString("yyyy-MM-dd"),
            "priority": self.priority_input.currentText(),
            "done": False
        }

class TaskCard(QFrame):
    done_clicked = Signal(int)

    def __init__(self, task_data, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.task_data = task_data
        
        priority = task_data.get("priority", "Low")
        colors = PRIORITY_COLORS.get(priority, PRIORITY_COLORS["Low"])
        
        self.setStyleSheet(f"""
            TaskCard {{
                background-color: {colors['bg']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                margin-bottom: 5px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        top_layout = QHBoxLayout()
        title_label = QLabel(f"<b>{task_data.get('title', 'Untitled')}</b>")
        title_label.setStyleSheet("border: none;")
        
        self.done_btn = QPushButton("✓ Done")
        self.done_btn.setStyleSheet(f"""
            QPushButton {{
                color: {colors['border']}; 
                border: 1px solid {colors['border']}; 
                border-radius: 4px; 
                padding: 4px 8px;
                background-color: transparent;
            }}
            QPushButton:hover {{ background-color: white; }}
        """)
        self.done_btn.setFixedWidth(80)
        self.done_btn.clicked.connect(lambda: self.done_clicked.emit(self.index))
        
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.done_btn)
        layout.addLayout(top_layout)
        
        bottom_layout = QHBoxLayout()
        deadline_label = QLabel(f"📅 {task_data.get('deadline', '')}")
        deadline_label.setStyleSheet("border: none; color: #555;")
        
        priority_label = QLabel(priority.upper())
        priority_label.setStyleSheet(f"""
            background-color: {colors['border']}; 
            color: white; 
            font-weight: bold; 
            border-radius: 10px; 
            padding: 2px 10px;
        """)
        priority_label.setAlignment(Qt.AlignCenter)
        
        bottom_layout.addWidget(deadline_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(priority_label)
        layout.addLayout(bottom_layout)

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.resize(500, 600)
        self.tasks = []
        
        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        header_layout = QHBoxLayout()
        title = QLabel("<h2>My To-Do List</h2>")
        self.status_label = QLabel("0/0 done")
        self.status_label.setStyleSheet("color: #666;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)
        main_layout.addLayout(header_layout)
        
        toolbar_layout = QHBoxLayout()
        
        add_btn = QPushButton("+ Add Task")
        add_btn.setStyleSheet("background-color: #4a90e2; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        add_btn.clicked.connect(self.open_add_dialog)
        
        load_btn = QPushButton("📁 Load JSON")
        load_btn.setStyleSheet("background-color: #6c757d; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        load_btn.clicked.connect(self.load_json)
        
        save_btn = QPushButton("💾 Save JSON")
        save_btn.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        save_btn.clicked.connect(self.save_json)
        
        toolbar_layout.addWidget(add_btn)
        toolbar_layout.addWidget(load_btn)
        toolbar_layout.addWidget(save_btn)
        toolbar_layout.addStretch()
        main_layout.addLayout(toolbar_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: #f8f9fa;")
        
        self.tasks_container = QWidget()
        self.tasks_container.setStyleSheet("background-color: #f8f9fa;")
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(self.tasks_container)
        main_layout.addWidget(self.scroll_area)
        
        self.empty_label = QLabel("No tasks yet.\nClick + Add Task to get started!")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: #aaa; font-size: 14px;")
        main_layout.addWidget(self.empty_label)

    def update_ui(self):
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        active_count = 0
        done_count = sum(1 for t in self.tasks if t.get('done', False))
        total_count = len(self.tasks)
        
        for index, task in enumerate(self.tasks):
            if not task.get('done', False):
                card = TaskCard(task, index)
                card.done_clicked.connect(self.mark_task_done)
                self.tasks_layout.addWidget(card)
                active_count += 1
                
        self.empty_label.setVisible(active_count == 0)
        self.scroll_area.setVisible(active_count > 0)
        self.status_label.setText(f"{done_count}/{total_count} done")

    def open_add_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.Accepted:
            new_task = dialog.get_task_data()
            if new_task["title"]:
                self.tasks.append(new_task)
                self.update_ui()

    def mark_task_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['done'] = True
            self.update_ui()

    def load_json(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load Tasks", "", "JSON Files (*.json)")
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    self.tasks = json.load(file)
                self.update_ui()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load JSON file:\n{str(e)}")

    def save_json(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Tasks", "", "JSON Files (*.json)")
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    json.dump(self.tasks, file, indent=2)
                QMessageBox.information(self, "Success", "Tasks successfully saved to JSON!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save JSON file:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    
    app.setStyle("Fusion")
    
    window = TodoApp()
    window.show()
    sys.exit(app.exec())