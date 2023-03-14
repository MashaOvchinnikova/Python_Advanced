import sys


def decrypt(encrypted_str: str) -> str:
    """
    Дешифратор
    :param encrypted_str: Зашифрованное сообщение в виде строки
    :return: Расшифрованное сообщение в виде втроки
    """
    decrypted_chars = []
    for symbol in encrypted_str:
        decrypted_chars.append(symbol)
        if len(decrypted_chars) > 2 and (decrypted_chars[-1], decrypted_chars[-2]) == ('.', '.'):
            decrypted_chars.pop()
            decrypted_chars.pop()
            if decrypted_chars:
                decrypted_chars.pop()
    return ''.join([char for char in decrypted_chars if char != '.'])


if __name__ == '__main__':
    message = sys.stdin.read()
    print(decrypt(message))
