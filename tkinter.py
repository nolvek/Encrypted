from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

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
