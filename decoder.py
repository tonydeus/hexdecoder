import tkinter as tk
from tkinter import messagebox

def decode_byte_string(hex_string):
    try:
        # Преобразуем hex-строку в байты
        byte_string = bytes.fromhex(hex_string)

        # Словарь для управляющих символов ASCII (0-31 и 127)
        control_chars = {
            0: 'NUL', 1: 'SOH', 2: 'STX', 3: 'ETX', 4: 'EOT', 5: 'ENQ', 6: 'ACK', 7: 'BEL',
            8: 'BS', 9: 'TAB', 10: 'LF', 11: 'VT', 12: 'FF', 13: 'CR', 14: 'SO', 15: 'SI',
            16: 'DLE', 17: 'DC1', 18: 'DC2', 19: 'DC3', 20: 'DC4', 21: 'NAK', 22: 'SYN', 23: 'ETB',
            24: 'CAN', 25: 'EM', 26: 'SUB', 27: 'ESC', 28: 'FS', 29: 'GS', 30: 'RS', 31: 'US',
            127: 'DEL'
        }

        result = []
        for byte in byte_string:
            if byte in control_chars:
                result.append(f"[{control_chars[byte]}]")
            else:
                result.append(chr(byte))
        return ''.join(result)
    except ValueError:
        return None  # Возвращаем None в случае ошибки

def on_decode():
    hex_string = entry.get().strip()
    if not hex_string:
        messagebox.showerror("Ошибка", "Введите hex-строку!")
        return

    # Декодируем строку
    decoded_string = decode_byte_string(hex_string)
    if decoded_string is None:
        messagebox.showerror("Ошибка", "Некорректная hex-строка!")
        return

    # Очищаем поле вывода
    result_text.delete(1.0, tk.END)

    # Выводим входящую строку
    result_text.insert(tk.END, "Входящая строка:\n")
    result_text.insert(tk.END, hex_string + "\n\n")

    # Выводим результат декодирования
    result_text.insert(tk.END, "Результат декодирования:\n")
    result_text.insert(tk.END, decoded_string + "\n")

    # Очищаем поле ввода
    entry.delete(0, tk.END)

def paste_text():
    try:
        # Вставляем текст из буфера обмена
        text = root.clipboard_get()
        entry.delete(0, tk.END)  # Очищаем поле ввода
        entry.insert(tk.END, text)  # Вставляем текст
    except tk.TclError:
        messagebox.showerror("Ошибка", "Не удалось вставить текст из буфера обмена.")

# Создаем графическое окно
root = tk.Tk()
root.title("Hex Decoder")

# Поле для ввода hex-строки
label = tk.Label(root, text="Введите hex-строку:")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Кнопка для вставки текста
#paste_button = tk.Button(root, text="Вставить", command=paste_text)
#paste_button.pack(pady=5)

# Кнопка для декодирования
decode_button = tk.Button(root, text="Декодировать", command=on_decode)
decode_button.pack(pady=10)

# Поле для вывода результата
result_text = tk.Text(root, height=15, width=60)
result_text.pack(pady=5)

# Запуск основного цикла
root.mainloop()