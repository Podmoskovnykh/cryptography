import random
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QSizePolicy, QApplication, QTabWidget, QRadioButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class PolybiusCipher:
    def __init__(self):
        self.alphabet = "абвгдежзиклмнопрстуфхцчшщъыьэюя.!, "
        self.polybius_table = self.generate_polybius_table(7, 5)

    def generate_polybius_table(self, rows, cols):
        table = [['' for _ in range(cols)] for _ in range(rows)]
        used_chars = []

        for i in range(rows):
            for j in range(cols):
                char = random.choice(self.alphabet)
                while char in used_chars:
                    char = random.choice(self.alphabet)
                table[i][j] = char
                used_chars.append(char)

        return table

    def polybius_encrypt(self, message):
        message = message.lower().replace('ё', 'е').replace('й', 'и')
        encrypted_message = ""
        for char in message:
            if char in self.alphabet:
                for i in range(len(self.polybius_table)):
                    for j in range(len(self.polybius_table[0])):
                        if self.polybius_table[i][j] == char:
                            encrypted_message += self.polybius_table[(i + 1) % len(self.polybius_table)][j]
                            break
            else:
                encrypted_message += char
        return encrypted_message

    def polybius_decrypt(self, encrypted_message):
        decrypted_message = ""
        for char in encrypted_message:
            if char in self.alphabet:
                for i in range(len(self.polybius_table)):
                    for j in range(len(self.polybius_table[0])):
                        if self.polybius_table[i][j] == char:
                            decrypted_row = (i - 1) if i > 0 else len(self.polybius_table) - 1
                            decrypted_message += self.polybius_table[decrypted_row][j]
                            break
            else:
                decrypted_message += char
        return decrypted_message


class PermutationCipher:

    def mirror(self, text):
        mirrored_text = text[::-1]
        return mirrored_text

    def split_into_fives(self, text):
        chunks = [text[i:i + 5] for i in range(0, len(text), 5)]
        return ' '.join(chunks)

    def encrypt(self, text):
        text = ''.join(
            filter(str.isalpha, text.upper()))
        mirrored_text = self.mirror(text)
        encrypted_text = self.split_into_fives(mirrored_text)
        return encrypted_text

    def unmirror(self, text):
        return text[::-1]

    def decrypt(self, text):
        text = text.replace(' ', '')
        unmirrored_text = self.unmirror(text)
        return unmirrored_text


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Криптография")
        self.cipher_polybius = PolybiusCipher()
        self.cipher_permutation = PermutationCipher()
        self.initUI()
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(0, 0, 860, 364)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        polybius_tab = QWidget()
        new_cipher_tab = QWidget()
        tab_widget.addTab(polybius_tab, "Полибианский шифр")
        tab_widget.addTab(new_cipher_tab, "Шифр перестановки")

        tab_widget.setStyleSheet("""
                    QTabWidget::pane { background-color: white; border: 2px solid #2196F3; border-radius: 4px; }
                    QTabBar::tab:selected { background-color: #2196F3; color: white; }
                    QTabBar::tab:!selected { background-color: #EEEEEE; color: #2196F3; }
                """)

        self.setup_polybius_tab(polybius_tab)
        self.setup_permutation_tab(new_cipher_tab)

    def setup_permutation_tab(self, new_cipher_tab):
        layout = QGridLayout(new_cipher_tab)

        message_label = QLabel("Открытый текст")
        message_label.setAlignment(Qt.AlignTop)
        layout.addWidget(message_label, 0, 0)

        self.message_entry_permutation = QTextEdit()
        self.message_entry_permutation.setFixedWidth(700)
        self.message_entry_permutation.setFixedHeight(30)
        layout.addWidget(self.message_entry_permutation, 0, 1, 1, 2)

        result_label = QLabel("Результат")
        result_label.setAlignment(Qt.AlignTop)
        layout.addWidget(result_label, 1, 0)

        self.result_text = QTextEdit()
        self.result_text.setFixedWidth(700)
        self.result_text.setFixedHeight(30)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text, 1, 1, 1, 2)

        buttons_layout = QHBoxLayout()
        self.encrypt_radio = QRadioButton("Зашифровать")
        self.decrypt_radio = QRadioButton("Расшифровать")
        buttons_layout.addWidget(self.encrypt_radio)
        buttons_layout.addWidget(self.decrypt_radio)

        self.encrypt_button = QPushButton("Выберите действие")
        buttons_layout.addWidget(self.encrypt_button)

        self.encrypt_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; border: 2px solid #1976D2; "
            "border-radius: 5px; padding: 8px; } QPushButton:hover { background-color: #1976D2; }")

        layout.addLayout(buttons_layout, 2, 0, 1, 3)

        self.encrypt_radio.toggled.connect(self.on_encrypt_toggled)
        self.decrypt_radio.toggled.connect(self.on_decrypt_toggled)
        self.encrypt_button.clicked.connect(self.perform_action)

    def on_encrypt_toggled(self, checked):
        if checked:
            self.encrypt_button.setText("Зашифровать")
            self.encrypt_button.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; border: 2px solid #4CAF50; border-radius: 5px; "
                "padding: 8px; } QPushButton:hover { background-color: #45a049; }")

    def on_decrypt_toggled(self, checked):
        if checked:
            self.encrypt_button.setText("Расшифровать")
            self.encrypt_button.setStyleSheet(
                "QPushButton { background-color: #f44336; color: white; border: 2px solid #f44336; border-radius: 5px; "
                "padding: 8px; } QPushButton:hover { background-color: #d32f2f; }")

    def perform_action(self):
        if self.encrypt_radio.isChecked():
            message = self.message_entry_permutation.toPlainText()
            result = PermutationCipher().encrypt(message)
            self.result_text.setPlainText(result)
        elif self.decrypt_radio.isChecked():
            message = self.message_entry_permutation.toPlainText()
            result = PermutationCipher().decrypt(message)
            self.result_text.setPlainText(result)

    def setup_polybius_tab(self, polybius_tab):
        layout = QHBoxLayout(polybius_tab)

        left_layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        layout.addLayout(left_layout)
        layout.addLayout(center_layout)
        layout.addLayout(right_layout)

        centering_layout_message = QHBoxLayout()
        left_layout.addLayout(centering_layout_message)
        message_label = QLabel("Введите сообщение:")
        message_label.setAlignment(Qt.AlignCenter)
        centering_layout_message.addWidget(message_label)

        self.message_entry_polybius = QTextEdit()
        left_layout.addWidget(self.message_entry_polybius)

        self.table_polybius = QTableWidget(len(self.cipher_polybius.polybius_table),
                                           len(self.cipher_polybius.polybius_table[0]))
        self.table_polybius.setHorizontalHeaderLabels(
            [str(i) for i in range(1, len(self.cipher_polybius.polybius_table[0]) + 1)])
        self.table_polybius.setVerticalHeaderLabels(
            [str(i) for i in range(1, len(self.cipher_polybius.polybius_table) + 1)])

        for i, row in enumerate(self.cipher_polybius.polybius_table):
            for j, item in enumerate(row):
                item_widget = QTableWidgetItem(item)
                item_widget.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item_widget.setTextAlignment(Qt.AlignCenter)
                self.table_polybius.setItem(i, j, item_widget)

        for i in range(len(self.cipher_polybius.polybius_table[0])):
            self.table_polybius.setColumnWidth(i, 1)

        self.table_polybius.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.table_polybius)

        centering_layout_encrypted = QHBoxLayout()
        right_layout.addLayout(centering_layout_encrypted)
        encrypted_label = QLabel("Зашифрованное сообщение:")
        encrypted_label.setAlignment(Qt.AlignCenter)
        centering_layout_encrypted.addWidget(encrypted_label)

        self.encrypted_message_text_polybius = QTextEdit()
        right_layout.addWidget(self.encrypted_message_text_polybius)

        encrypt_button = QPushButton("Зашифровать")
        encrypt_button.clicked.connect(self.encrypt_message_polybius)
        left_layout.addWidget(encrypt_button)

        decrypt_button = QPushButton("Расшифровать")
        decrypt_button.clicked.connect(self.decrypt_message_polybius)
        right_layout.addWidget(decrypt_button)

        encrypt_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 4px; padding: 8px; } "
            "QPushButton:hover { background-color: #45a049; }")
        decrypt_button.setStyleSheet(
            "QPushButton { background-color: #f44336; color: white; border: none; border-radius: 4px; padding: 8px; } "
            "QPushButton:hover { background-color: #d32f2f; }")

    def encrypt_message_polybius(self):
        message = self.message_entry_polybius.toPlainText()
        encrypted_message = self.cipher_polybius.polybius_encrypt(message)
        self.encrypted_message_text_polybius.setPlainText(encrypted_message)

    def decrypt_message_polybius(self):
        encrypted_message = self.encrypted_message_text_polybius.toPlainText()
        decrypted_message = self.cipher_polybius.polybius_decrypt(encrypted_message)
        self.message_entry_polybius.setPlainText(decrypted_message)


def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
