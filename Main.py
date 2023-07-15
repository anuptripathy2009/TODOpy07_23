import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QListWidgetItem, QDialog, QLabel, QDialogButtonBox

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Task")
        self.setFixedSize(400, 250)  # Decrease width and height of the dialog box window

        layout = QVBoxLayout()

        label = QLabel("Enter task:")
        label.setStyleSheet("font-size: 20px; font-weight: bold")  # Increase font size and set font weight to bold
        layout.addWidget(label)

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("font-size: 21px")  # Increase font size of the input field
        self.input_field.setFixedHeight(40)  # Increase height of the input field
        layout.addWidget(self.input_field)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("font-size: 18px")  # Increase font size of the buttons in the button box
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_task_text(self):
        return self.input_field.text()

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Todo List")
        self.setGeometry(100, 100, 800, 600)  # Increase width and height of the window

        self.layout = QVBoxLayout()

        self.task_list = QListWidget()
        self.task_list.setAlternatingRowColors(True)

        self.add_button = QPushButton("Add Task")
        self.add_button.setFixedWidth(150)  # Increase width of the button
        self.add_button.setFixedHeight(40)  # Increase height of the button
        self.add_button.setStyleSheet("background-color: #525FE1; color: #202020; font-weight: bold; font-size: 18px")  # Set button color, text color, font weight, and font size
        self.add_button.clicked.connect(self.add_task_dialog)

        self.edit_button = QPushButton("Edit Task")
        self.edit_button.setFixedWidth(150)  # Increase width of the button
        self.edit_button.setFixedHeight(40)  # Increase height of the button
        self.edit_button.setStyleSheet("background-color: lightgreen; color: #202020; font-weight: bold; font-size: 18px")  # Set button color, text color, font weight, and font size
        self.edit_button.clicked.connect(self.edit_task)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedWidth(150)  # Increase width of the button
        self.delete_button.setFixedHeight(40)  # Increase height of the button
        self.delete_button.setStyleSheet("background-color: #B31312; color: #202020; font-weight: bold; font-size: 18px")  # Set button color, text color, font weight, and font size
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setEnabled(False)

        self.layout.addWidget(self.task_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.task_list.itemSelectionChanged.connect(self.update_button_state)

    def add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            task_text = dialog.get_task_text()
            if task_text:
                task = QListWidgetItem(task_text)
                task.setFont(self.get_task_font())  # Set font for the task item
                task.setTextAlignment(Qt.AlignLeft)  # Align text to the left
                task.setBackground(self.get_task_background_color(self.task_list.count()))  # Set background color
                task.setSizeHint(self.get_task_block_size_hint(task_text))  # Set size hint for task item
                self.task_list.addItem(task)

    def edit_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            dialog = AddTaskDialog(self)
            dialog.setWindowTitle("Edit Task")
            dialog.input_field.setText(current_item.text())
            if dialog.exec_() == QDialog.Accepted:
                new_task_text = dialog.get_task_text()
                if new_task_text:
                    current_item.setText(new_task_text)
                    current_item.setSizeHint(self.get_task_block_size_hint(new_task_text))
        else:
            QMessageBox.warning(self, "Warning", "Nothing is selected.")

    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            result = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.task_list.takeItem(self.task_list.row(current_item))
        else:
            QMessageBox.warning(self, "Warning", "Nothing is selected.")

    def update_button_state(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            self.edit_button.setStyleSheet("background-color: #008000; color: #202020; font-weight: bold; font-size: 18px")  # Change background color to darker shade for selected item
            self.delete_button.setStyleSheet("background-color: #FF7575; color: #202020; font-weight: bold; font-size: 18px")  # Change background color to lighter shade for selected item
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            self.reset_button_colors()
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)

    def reset_button_colors(self):
        self.edit_button.setStyleSheet("background-color: lightgreen; color: #202020; font-weight: bold; font-size: 18px")  # Reset background color for edit button
        self.delete_button.setStyleSheet("background-color: #B31312; color: #202020; font-weight: bold; font-size: 18px")  # Reset background color for delete button

    def get_task_font(self):
        font = self.task_list.font()
        font.setPointSize(font.pointSize() + 5)  # Increase font size by 5 pixels
        font.setWeight(QFont.Bold)  # Set font weight to bold
        return font

    def get_task_background_color(self, task_index):
        if task_index % 2 == 0:
            if task_index % 4 == 0:
                return QColor("#E8E8E8")  # Light grey color for nth even child
            else:
                return QColor("#F0F0F0")  # Dark grey color for other even child
        else:
            return self.palette().base()

    def get_task_block_size_hint(self, task_text):
        text_width = self.task_list.fontMetrics().boundingRect(task_text).width() + 10
        return QSize(text_width, 50)  # Modify the height as per your preference

    def mousePressEvent(self, event):
        self.task_list.clearSelection()
        super().mousePressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
