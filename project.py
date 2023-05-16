from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import hashlib
import base64
import random
import os

def execute_encryption():
    encryption_type = combo.get()
    text = txt.get()
    action = select_vibor.get()
    result = ""

    if encryption_type == 'MD5':
        result = hashlib.md5(text.encode()).hexdigest()
    elif encryption_type == 'SHA256':
        result = hashlib.sha256(text.encode()).hexdigest()
    elif encryption_type == 'SHA512':
        result = hashlib.sha512(text.encode()).hexdigest()
    elif encryption_type == 'Шифр Цезаря':
        shift = 3  # Задайте значение сдвига
        if action == 'Зашифровать':
            result = encrypt_cesyar(text, shift)
        else:
            result = decrypt_cesyar(text, shift)
    elif encryption_type == 'base64':
        if action == 'Зашифровать':
            result = base64.b64encode(text.encode()).decode("ascii")
        else:
            try:
                decoded_text = base64.b64decode(text.encode()).decode("ascii")
                result = decoded_text
            except:
                messagebox.showwarning("Предупреждение", "Неверный формат текста для декодирования из base64.")
                return
    elif encryption_type == 'Шифр Виженера':
        key = "secret"  # Задайте ключ 
        if action == 'Зашифровать':
            result = encrypt_vigenere(text, key)
        else:
            result = decrypt_vigenere(text, key)
    elif encryption_type == 'Омофоническая замена':
        omophonic_dict = create_omophonic_dict()
        if action == 'Зашифровать':
            result = encrypt_omophonic(text, omophonic_dict)
        else:
            result = decrypt_omophonic(text, omophonic_dict)
    else:
        messagebox.showwarning("Предупреждение", "Выберите тип шифрования.")
        return
            
    if encryption_type in ['MD5', 'SHA256', 'SHA512'] and action == 'Дешифровать':
        messagebox.showwarning("Предупреждение", "Данные, зашифрованные с помощью MD5, SHA256 или SHA512, нельзя дешифровать.")
        return
     
    if not text:
         messagebox.showwarning("Предупреждение", "Поле ввода не может быть пустым.")
         return

    txt2.config(state=NORMAL)
    txt2.delete(0, 'end')
    txt2.insert(0, result)
    txt2.config(state='readonly')

# Шифр цезаря
def encrypt_cesyar(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            # Сдвигаем букву по алфавиту с учетом границы a/A и z/Z
            if char.isupper():
                encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            encrypted_text += char
    return encrypted_text


def decrypt_cesyar(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            # Сдвигаем букву по алфавиту с учетом границы a/A и z/Z
            if char.isupper():
                decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
            else:
                decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            decrypted_text += char
    return decrypted_text


# Шифр Виженера
def encrypt_vigenere(text, key):
    encrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            # Сдвигаем букву по алфавиту с учетом границы a/A и z/Z
            if char.isupper():
                encrypted_text += chr((ord(char) + ord(key[key_index].upper()) - 2 * 65) % 26 + 65)
            else:
                encrypted_text += chr((ord(char) + ord(key[key_index].lower()) - 2 * 97) % 26 + 97)
            key_index = (key_index + 1) % len(key)
        else:
            encrypted_text += char
    return encrypted_text


def decrypt_vigenere(text, key):
    decrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            # Сдвигаем букву по алфавиту с учетом границы a/A и z/Z
            if char.isupper():
                decrypted_text += chr((ord(char) - ord(key[key_index].upper()) + 26) % 26 + 65)
            else:
                decrypted_text += chr((ord(char) - ord(key[key_index].lower()) + 26) % 26 + 97)
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text


# Омофоническая замена
def create_omophonic_dict():
    omophonic_dict = {}
    for i in range(97, 123):
        omophonic_dict[chr(i)] = []
    omophonic_dict[' '] = [' ']
    omophonic_dict['.'] = ['.']
    omophonic_dict[','] = [',']
    omophonic_dict['!'] = ['!']
    omophonic_dict['?'] = ['?']
    omophonic_dict['-'] = ['-']
    omophonic_dict['\''] = ['\'']
    omophonic_dict['\"'] = ['\"']
    omophonic_dict['('] = ['(']
    omophonic_dict[')'] = [')']
    omophonic_dict[':'] = [':']
    omophonic_dict[';'] = [';']
    omophonic_dict['/'] = ['/']
    omophonic_dict['\\'] = ['\\']
    omophonic_dict['@'] = ['@']
    omophonic_dict['#'] = ['#']
    omophonic_dict['$'] = ['$']
    omophonic_dict['%'] = ['%']
    omophonic_dict['^'] = ['^']
    omophonic_dict['&'] = ['&']
    omophonic_dict['*'] = ['*']
    omophonic_dict['+'] = ['+']
    omophonic_dict['='] = ['=']
    omophonic_dict['_'] = ['_']
    omophonic_dict['~'] = ['~']
    omophonic_dict['`'] = ['`']
    for i in range(10):
        omophonic_dict[str(i)] = [str(i)]
    for i in range(97, 123):
        for j in range(5):
            omophonic_dict[chr(i)].append(chr(random.randint(97, 123)))
    return omophonic_dict


def encrypt_omophonic(text, omophonic_dict):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            # Выбираем случайный символ из словаря для замены
            encrypted_text += omophonic_dict[char][random.randint(0, len(omophonic_dict[char])-1)]
        else:
            encrypted_text += char
    return encrypted_text


def decrypt_omophonic(text, omophonic_dict):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            # Ищем символ в словаре и возвращаем его ключ
            for key, value in omophonic_dict.items():
                if char in value:
                    decrypted_text += key
                    break
        else:
            decrypted_text += char
    return decrypted_text


window = Tk()
window.title("Encryption")
window.geometry('600x400')
window.iconbitmap(default='shield.ico')
window.resizable(width=False, height=False)

label = Label(window, text="Encryption", font="Helvetica 12 bold")
label.pack(anchor='n', pady=5, padx=5)

label2 = Label(window, text="Выберите тип шифрования:")
label2.pack(anchor='w', padx=40, pady=40)

combo = Combobox(window, state="readonly")
combo['values'] = ('MD5', 'SHA256', 'SHA512', 'Шифр Цезаря', 'Шифр Виженера', 'Омофоническая замена', 'base64')
combo.current(1)
combo.place(x=210, y=69)

vibor = ["Зашифровать", "Дешифровать"]
select_vibor = StringVar(value=vibor[0])

for index, vib in enumerate(vibor):
    vib_btn = Radiobutton(text=vib, value=vib, variable=select_vibor)
    vib_btn.place(x=40 + index * 110, y=110)

lbl = Label(window, text="Введите текст:")
lbl.place(x=40, y=150)

txt = Entry(window, width=100)
txt.pack(anchor="sw", padx=40, pady=50)

lbl2= Label(window, text="Вывод:")
lbl2.place(x=40, y=220)

txt2 = Entry(window, width=86, state=DISABLED)
txt2.place(x=40, y=250)

btn = Button(text="Выполнить", command=execute_encryption)
btn.place(x=240, y=280)

window.mainloop()
