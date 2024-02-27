import re


def mirror(text):
    mirrored_text = text[::-1]  # Обратное написание текста
    return mirrored_text


def split_into_fives(text):
    text_length = len(text)
    chunks = [text[i:i + 5] for i in range(0, min(5, text_length), 5)]  # Разбиение первых 5 символов
    if len(chunks[0]) < 5:
        chunks[0] += 'О' * (5 - len(chunks[0]))  # Добавление 'О' в первый блок, если символов меньше 5
    chunks += [text[i:i + 5] for i in range(5, text_length, 5)]  # Разбиение остальных символов на блоки по 5 символов
    return ' '.join(chunks)


def encrypt(text):
    text = ''.join(
        filter(str.isalpha, text.upper()))  # Удаление всех символов, кроме букв и преобразование в верхний регистр
    mirrored_text = mirror(text)
    encrypted_text = split_into_fives(mirrored_text)
    return encrypted_text


def unmirror(text):
    return text[::-1]  # Обратное написание текста


def decrypt_chunk(chunk):
    return unmirror(chunk)


def decrypt(text):
    text = text.replace(' ', '')  # Удаление пробелов
    chunks = [text[i:i + 5] for i in range(0, len(text), 5)]  # Разделение на пятерки букв
    decrypted_text = ' '.join(chunks)
    decrypted_text = unmirror(decrypted_text)
    return decrypted_text

# Пример использования
plaintext = "ПУСТЬ БУДЕТ ТАК, КАК МЫ ХОТЕЛИ"
encrypted_text = encrypt(plaintext)
print("Шифрограмма:", encrypted_text)

encrypted_text = "ИЛЕТО ХЫМКА ККАТТ ЕДУБЬ ТСУП"
decrypted_text = decrypt(encrypted_text)
print("Расшифрованный текст:", decrypted_text)
