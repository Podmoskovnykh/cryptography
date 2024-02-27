class PermutationCipher:

    def mirror(self, text):
        mirrored_text = text[::-1]  # Обратное написание текста
        return mirrored_text

    def split_into_fives(text):
        chunks = [text[i:i + 5] for i in range(0, len(text), 5)]  # Разбиение на пятерки букв
        return ' '.join(chunks)

    def encrypt(text):
        text = ''.join(
            filter(str.isalpha, text.upper()))  # Удаление всех символов, кроме букв и преобразование в верхний регистр
        cipher = PermutationCipher()
        mirrored_text = cipher.mirror(text)
        encrypted_text = PermutationCipher.split_into_fives(mirrored_text)
        return encrypted_text

    def unmirror(text):
        return text[::-1]  # Обратное написание текста

    def decrypt(text):
        text = text.replace(' ', '')  # Удаление пробелов
        unmirrored_text = PermutationCipher.unmirror(text)
        return unmirrored_text


    # Пример использования
    plaintext = "ПУСТЬ БУДЕТ ТАК, КАК МЫ ХОТЕЛИ"
    encrypted_text = encrypt(plaintext)
    print("Шифрограмма:", encrypted_text)

    encrypted_text = "ИЛЕТО ХЫМКА ККАТТ ЕДУБЬ ТСУП"
    decrypted_text = decrypt(encrypted_text)
    print("Расшифрованный текст:", decrypted_text)
