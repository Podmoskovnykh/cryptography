import random
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QSizePolicy, QApplication
from PyQt5.QtCore import Qt


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


class PolybiusGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шифр «Полибианский квадрат»")
        self.cipher = PolybiusCipher()
        self.initUI()
        self.setGeometry(0, 0, 834, 336)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        left_layout = QVBoxLayout()
        middle_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(right_layout)

        centering_layout_message = QHBoxLayout()
        left_layout.addLayout(centering_layout_message)
        message_label = QLabel("Введите сообщение:")
        message_label.setAlignment(Qt.AlignCenter)
        centering_layout_message.addWidget(message_label)

        self.message_entry = QTextEdit()
        left_layout.addWidget(self.message_entry)

        centering_layout_table = QHBoxLayout()
        middle_layout.addLayout(centering_layout_table)
        table_label = QLabel("Сгенерированная таблица:")
        table_label.setAlignment(Qt.AlignCenter)
        centering_layout_table.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setRowCount(len(self.cipher.polybius_table))
        self.table.setColumnCount(len(self.cipher.polybius_table[0]))
        self.table.setHorizontalHeaderLabels([str(i) for i in range(1, len(self.cipher.polybius_table[0]) + 1)])
        self.table.setVerticalHeaderLabels([str(i) for i in range(1, len(self.cipher.polybius_table) + 1)])

        for i, row in enumerate(self.cipher.polybius_table):
            for j, item in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(item))

        for i in range(len(self.cipher.polybius_table[0])):
            self.table.setColumnWidth(i, 1)

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        middle_layout.addWidget(self.table)

        centering_layout_encrypted = QHBoxLayout()
        right_layout.addLayout(centering_layout_encrypted)
        encrypted_label = QLabel("Зашифрованное сообщение:")
        encrypted_label.setAlignment(Qt.AlignCenter)
        centering_layout_encrypted.addWidget(encrypted_label)

        self.encrypted_message_text = QTextEdit()
        right_layout.addWidget(self.encrypted_message_text)

        encrypt_button = QPushButton("Зашифровать")
        encrypt_button.clicked.connect(self.encrypt_message)
        left_layout.addWidget(encrypt_button)

        decrypt_button = QPushButton("Расшифровать")
        decrypt_button.clicked.connect(self.decrypt_message)
        right_layout.addWidget(decrypt_button)

    def encrypt_message(self):
        message = self.message_entry.toPlainText()
        encrypted_message = self.cipher.polybius_encrypt(message)
        self.encrypted_message_text.setPlainText(encrypted_message)

    def decrypt_message(self):
        encrypted_message = self.encrypted_message_text.toPlainText()
        decrypted_message = self.cipher.polybius_decrypt(encrypted_message)
        self.message_entry.setPlainText(decrypted_message)


def main():
    app = QApplication(sys.argv)
    window = PolybiusGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
