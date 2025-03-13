import tkinter as tk
from tkinter import messagebox, filedialog

# Словарь управляющих символов
CONTROL_CHARS = {
    0: 'NUL', 1: 'SOH', 2: 'STX', 3: 'ETX', 4: 'EOT', 5: 'ENQ', 6: 'ACK', 7: 'BEL',
    8: 'BS', 9: 'TAB', 10: 'LF', 11: 'VT', 12: 'FF', 13: 'CR', 14: 'SO', 15: 'SI',
    16: 'DLE', 17: 'DC1', 18: 'DC2', 19: 'DC3', 20: 'DC4', 21: 'NAK', 22: 'SYN', 23: 'ETB',
    24: 'CAN', 25: 'EM', 26: 'SUB', 27: 'ESC', 28: 'FS', 29: 'GS', 30: 'RS', 31: 'US',
    127: 'DEL'
}

# Максимальная длина hex-строки
MAX_HEX_LENGTH = 1000

def decode_byte_string(hex_string):
    try:
        return ''.join(
            f'[{CONTROL_CHARS.get(byte, chr(byte))}]' 
            if byte in CONTROL_CHARS else chr(byte)
            for byte in bytes.fromhex(hex_string)
        )
    except ValueError:
        return None

def is_valid_hex(hex_string):
    # Проверяем, что строка состоит только из допустимых hex-символов
    hex_digits = set("0123456789ABCDEFabcdef")
    return all(char in hex_digits for char in hex_string)

def on_decode():
    hex_string = entry.get().strip()
    if not hex_string:
        messagebox.showerror("Ошибка", "Введите hex-строку!")
        entry.config(highlightbackground="red", highlightthickness=2)  # Подсветка ошибки
        entry.delete(0, tk.END)  # Очищаем поле ввода
        return

    if len(hex_string) > MAX_HEX_LENGTH:
        messagebox.showerror("Ошибка", f"Слишком длинная строка. Максимум {MAX_HEX_LENGTH} символов.")
        entry.config(highlightbackground="red", highlightthickness=2)  # Подсветка ошибки
        entry.delete(0, tk.END)  # Очищаем поле ввода
        return

    if not is_valid_hex(hex_string):
        messagebox.showerror("Ошибка", "Некорректная hex-строка! Используйте только символы 0-9, A-F, a-f.")
        entry.config(highlightbackground="red", highlightthickness=2)  # Подсветка ошибки
        entry.delete(0, tk.END)  # Очищаем поле ввода
        return

    decoded_string = decode_byte_string(hex_string)
    if decoded_string is None:
        messagebox.showerror("Ошибка", "Некорректная hex-строка!")
        entry.config(highlightbackground="red", highlightthickness=2)  # Подсветка ошибки
        entry.delete(0, tk.END)  # Очищаем поле ввода
        return

    # Сброс подсветки, если ошибок нет
    entry.config(highlightbackground="SystemButtonFace", highlightthickness=0)

    # Добавляем новый результат к истории
    result_text.insert(tk.END, f"Входящая строка:\n{hex_string}\n\n")
    result_text.insert(tk.END, f"Результат декодирования:\n{decoded_string}\n")
    result_text.insert(tk.END, "-" * 60 + "\n\n")  # Разделитель между результатами

    # Прокрутка к концу текста
    result_text.see(tk.END)

    # Очищаем поле ввода
    entry.delete(0, tk.END)

def clear_result():
    result_text.delete(1.0, tk.END)

def add_context_menu(widget):
    context_menu = tk.Menu(widget, tearoff=0)
    context_menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    context_menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Выделить всё", command=lambda: widget.event_generate("<<SelectAll>>"))
    
    def show_context_menu(event):
        context_menu.tk_popup(event.x_root, event.y_root)
    
    widget.bind("<Button-3>", show_context_menu)

def paste_text(event=None):
    try:
        # Получаем текст из буфера обмена
        text = root.clipboard_get()
        
        # Проверяем длину текста
        if len(text) > MAX_HEX_LENGTH:
            messagebox.showerror("Ошибка", f"Слишком длинный текст. Максимум {MAX_HEX_LENGTH} символов.")
            entry.delete(0, tk.END)  # Очищаем поле ввода
            return
        
        # Проверяем, что текст состоит только из hex-символов
        if not is_valid_hex(text):
            messagebox.showerror("Ошибка", "Некорректный текст. Используйте только символы 0-9, A-F, a-f.")
            entry.delete(0, tk.END)  # Очищаем поле ввода
            return
        
        # Вставляем текст в поле ввода
        entry.delete(0, tk.END)
        entry.insert(tk.END, text)
    except tk.TclError:
        messagebox.showerror("Ошибка", "Не удалось вставить текст из буфера обмена.")

def export_to_file():
    # Получаем содержимое текстового поля
    content = result_text.get(1.0, tk.END)
    if not content.strip():
        messagebox.showerror("Ошибка", "Нет данных для экспорта!")
        return

    # Открываем диалог сохранения файла
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
        title="Сохранить как"
    )
    if not file_path:  # Если пользователь отменил выбор
        return

    # Сохраняем содержимое в файл
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Успех", f"Данные успешно экспортированы в файл:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

def create_gui():
    global root, entry, result_text
    
    root = tk.Tk()
    root.title("Hex Decoder")
    
    # Поле для ввода hex-строки
    tk.Label(root, text="Введите hex-строку:").pack(pady=5)
    
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    
    # Горячие клавиши для поля ввода
    entry.bind("<Control-v>", paste_text)  # Ctrl+V для вставки
    entry.bind("<Control-c>", lambda event: entry.event_generate("<<Copy>>"))  # Ctrl+C для копирования
    entry.bind("<Control-x>", lambda event: entry.event_generate("<<Cut>>"))   # Ctrl+X для вырезания
    entry.bind("<Control-a>", lambda event: entry.event_generate("<<SelectAll>>"))  # Ctrl+A для выделения всего
    entry.bind("<Return>", lambda event: on_decode())                          # Enter для декодирования
    
    # Контекстное меню для поля ввода
    add_context_menu(entry)
    
    # Кнопка "Декодировать" после поля ввода
    decode_button = tk.Button(root, text="Декодировать", command=on_decode)
    decode_button.pack(pady=10)
    
    # Создаем фрейм для текстового поля и скроллбара
    frame = tk.Frame(root)
    frame.pack(pady=5)
    
    # Текстовое поле с выводом результатов
    result_text = tk.Text(frame, height=15, width=60)
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Вертикальный скроллбар
    scrollbar = tk.Scrollbar(frame, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Привязываем скроллбар к текстовому полю
    result_text.config(yscrollcommand=scrollbar.set)
    
    # Горячие клавиши для поля вывода
    result_text.bind("<Control-v>", lambda event: result_text.event_generate("<<Paste>>"))  # Ctrl+V для вставки
    result_text.bind("<Control-c>", lambda event: result_text.event_generate("<<Copy>>"))  # Ctrl+C для копирования
    result_text.bind("<Control-x>", lambda event: result_text.event_generate("<<Cut>>"))   # Ctrl+X для вырезания
    result_text.bind("<Control-a>", lambda event: result_text.event_generate("<<SelectAll>>"))  # Ctrl+A для выделения всего
    
    # Контекстное меню для поля вывода
    add_context_menu(result_text)
    
    # Кнопки "Очистить" и "Экспорт" после поля вывода
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    
    clear_button = tk.Button(button_frame, text="Очистить", command=clear_result)
    clear_button.pack(side=tk.LEFT, padx=5)
    
    export_button = tk.Button(button_frame, text="Экспорт", command=export_to_file)
    export_button.pack(side=tk.LEFT, padx=5)
    
    return root, entry, result_text

if __name__ == "__main__":
    root, entry, result_text = create_gui()
    root.mainloop()
    