import random
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QSizePolicy, QApplication, QTabWidget
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


class NewCipher:
    def __init__(self):
        # Инициализация вашего нового шифра
        pass

    def encrypt(self, message):
        # Логика для шифрования новым методом
        pass

    def decrypt(self, message):
        # Логика для дешифрования новым методом
        pass


class PolybiusGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Криптография")
        self.cipher_polybius = PolybiusCipher()
        self.cipher_new = NewCipher()
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
        tab_widget.addTab(new_cipher_tab, "Новый шифр")

        self.setup_polybius_tab(polybius_tab)
        self.setup_new_cipher_tab(new_cipher_tab)

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

    def setup_new_cipher_tab(self, new_cipher_tab):
        layout = QVBoxLayout(new_cipher_tab)

        # Добавьте элементы управления для нового шифра здесь

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
    window = PolybiusGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
