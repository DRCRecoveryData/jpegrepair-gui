import sys
import os
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QSpinBox, QFileDialog, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class JPEGRepairGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.input_file = ""
        self.output_file = ""
        self.delete_original = False
        self.delete_threshold = 1
        self.Y_threshold = 0
        self.Cb_threshold = 0
        self.Cr_threshold = 0

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("JPEG-Toolkit")
        self.setGeometry(100, 100, 400, 400)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("No Image")
        self.image_label.setFixedSize(400, 300)  # Set fixed size for the image box

        self.input_path_edit = QLineEdit(self)
        self.input_path_edit.setPlaceholderText("Input file path")
        self.input_path_edit.setFixedSize(400, 30)  # Set fixed size for the input path box

        self.browse_input_button = QPushButton("Browse", self)
        self.browse_input_button.clicked.connect(self.browse_input_file)
        self.browse_input_button.setFixedHeight(30)  # Set fixed height for the button

        self.delete_threshold_spinbox = QSpinBox(self)
        self.delete_threshold_spinbox.setMinimum(1)
        self.delete_threshold_spinbox.setMaximum(999999)  # Set maximum value for the spinbox
        self.delete_threshold_spinbox.setFixedHeight(30)  # Set fixed height for the spinbox

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_and_save)
        self.delete_button.setFixedHeight(30)  # Set fixed height for the button

        self.insert_button = QPushButton("Insert", self)
        self.insert_button.clicked.connect(self.insert_and_save)
        self.insert_button.setFixedHeight(30)  # Set fixed height for the button

        self.save_Y_button = QPushButton("Y", self)
        self.save_Y_button.clicked.connect(self.save_Y)
        self.save_Y_button.setFixedHeight(30)

        self.Y_threshold_spinbox = QSpinBox(self)
        self.Y_threshold_spinbox.setMinimum(-2047)
        self.Y_threshold_spinbox.setMaximum(2047)
        self.Y_threshold_spinbox.setFixedHeight(30)

        self.save_Cb_button = QPushButton("Cb", self)
        self.save_Cb_button.clicked.connect(self.save_Cb)
        self.save_Cb_button.setFixedHeight(30)

        self.Cb_threshold_spinbox = QSpinBox(self)
        self.Cb_threshold_spinbox.setMinimum(-2047)
        self.Cb_threshold_spinbox.setMaximum(2047)
        self.Cb_threshold_spinbox.setFixedHeight(30)

        self.save_Cr_button = QPushButton("Cr", self)
        self.save_Cr_button.clicked.connect(self.save_Cr)
        self.save_Cr_button.setFixedHeight(30)

        self.Cr_threshold_spinbox = QSpinBox(self)
        self.Cr_threshold_spinbox.setMinimum(-2047)
        self.Cr_threshold_spinbox.setMaximum(2047)
        self.Cr_threshold_spinbox.setFixedHeight(30)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.input_path_edit)
        layout.addWidget(self.browse_input_button)
        layout.addWidget(self.delete_threshold_spinbox)

        layout_delete_insert = QHBoxLayout()
        layout_delete_insert.addWidget(self.delete_button)
        layout_delete_insert.addWidget(self.insert_button)
        layout.addLayout(layout_delete_insert)

        layout_y = QHBoxLayout()
        layout_y.addWidget(self.Y_threshold_spinbox)
        layout_y.addWidget(self.save_Y_button)
        layout.addLayout(layout_y)

        layout_cb = QHBoxLayout()
        layout_cb.addWidget(self.Cb_threshold_spinbox)
        layout_cb.addWidget(self.save_Cb_button)
        layout.addLayout(layout_cb)

        layout_cr = QHBoxLayout()
        layout_cr.addWidget(self.Cr_threshold_spinbox)
        layout_cr.addWidget(self.save_Cr_button)
        layout.addLayout(layout_cr)

        self.setLayout(layout)

    def browse_input_file(self):
        self.input_file, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if self.input_file:
            self.input_path_edit.setText(self.input_file)
            self.show_image(self.input_file)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))
        self.image_label.setText("")

    def delete_and_save(self):
        if not self.input_file:
            QMessageBox.warning(self, "Warning", "Please select an input file.")
            return

        self.delete_threshold = self.delete_threshold_spinbox.value()
        output_dir = os.path.join(os.path.dirname(self.input_file), "Repaired")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.basename(self.input_file)
        self.output_file = os.path.join(output_dir, output_filename)
        subprocess.run(["jpegrepair.exe", self.input_file, self.output_file, "delete", str(self.delete_threshold)])
        self.show_image(self.output_file)

    def insert_and_save(self):
        if not self.input_file:
            QMessageBox.warning(self, "Warning", "Please select an input file.")
            return

        self.delete_threshold = self.delete_threshold_spinbox.value()
        output_dir = os.path.join(os.path.dirname(self.input_file), "Repaired")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.basename(self.input_file)
        self.output_file, _ = QFileDialog.getSaveFileName(self, "Save Output File", directory=output_dir, filter=f"JPEG files (*{os.path.splitext(output_filename)[1]})")
        if self.output_file:
            subprocess.run(["jpegrepair.exe", self.input_file, self.output_file, "insert", str(self.delete_threshold)])
            self.show_image(self.output_file)

    def save_Y(self):
        if not self.input_file:
            QMessageBox.warning(self, "Warning", "Please select an input file.")
            return

        self.Y_threshold = self.Y_threshold_spinbox.value()
        output_dir = os.path.join(os.path.dirname(self.input_file), "Repaired")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.basename(self.input_file)
        self.output_file = os.path.join(output_dir, output_filename)
        subprocess.run(["jpegrepair.exe", self.input_file, self.output_file, "cdelta", "0", str(self.Y_threshold)])
        self.show_image(self.output_file)

    def save_Cb(self):
        if not self.input_file:
            QMessageBox.warning(self, "Warning", "Please select an input file.")
            return

        self.Cb_threshold = self.Cb_threshold_spinbox.value()
        output_dir = os.path.join(os.path.dirname(self.input_file), "Repaired")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.basename(self.input_file)
        self.output_file = os.path.join(output_dir, output_filename)
        subprocess.run(["jpegrepair.exe", self.input_file, self.output_file, "cdelta", "1", str(self.Cb_threshold)])
        self.show_image(self.output_file)

    def save_Cr(self):
        if not self.input_file:
            QMessageBox.warning(self, "Warning", "Please select an input file.")
            return

        self.Cr_threshold = self.Cr_threshold_spinbox.value()
        output_dir = os.path.join(os.path.dirname(self.input_file), "Repaired")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.basename(self.input_file)
        self.output_file = os.path.join(output_dir, output_filename)
        subprocess.run(["jpegrepair.exe", self.input_file, self.output_file, "cdelta", "2", str(self.Cr_threshold)])
        self.show_image(self.output_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JPEGRepairGUI()
    window.show()
    sys.exit(app.exec())
