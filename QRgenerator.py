#QRgenerator 
# need pypng !!! no import required only have it installed: pip install pypng

VERSION = "v0.5"

import pyqrcode
from tkinter import *
from PIL import Image, ImageTk
import io                           #clipboatd   
import win32clipboard               #clipboard  pip install pywin32
import os
import subprocess
import webbrowser

BG_COLOR = "#ECE9E9"

root = Tk()
root.title(f'QR Code Generator {VERSION}')
root.geometry('300x350')
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# globalna referencia na obrazok
global_photo_image = None

# --- FUNKCIE ---
def generate_qr_code():
    global global_photo_image

    text = url_entry.get().strip()
    if not text:
        return

    qr = pyqrcode.create(text, encoding='utf-8')       # diakritika
    qr.png('qr_code.png', scale=5)

    image = Image.open('qr_code.png')

    # FIXNA VELKOST QR OBRAZKA
    image = image.resize((220, 220), Image.LANCZOS)

    global_photo_image = ImageTk.PhotoImage(image)
    qr_label.config(image=global_photo_image)

def open_qr_folder():
    file_path = os.path.abspath("qr_code.png")
    if os.path.exists(file_path):
        subprocess.run(f'explorer /select,"{file_path}"')

def clear_qr():
    qr_label.config(image='')
    url_entry.delete(0, END)

def copy_qr_to_clipboard(event=None):               # copy to clipboard
    if global_photo_image is None:
        return

    # otvor PNG znova ako PIL Image
    image = Image.open("qr_code.png").convert("RGB")

    output = io.BytesIO()
    image.save(output, "BMP")
    data = output.getvalue()[14:]  # odstráni BMP header
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def open_github(event=None):                            #→ event=None → aby fungovalo aj z klávesnice alebo iného volania.
    webbrowser.open_new("https://github.com/igvisk")


# --- GRID KONFIGURACIA ---
root.columnconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

# --- UI ---
url_label = Label(root, text='Enter text or URL', font=("Arial", 10, "bold"))
url_label.configure(bg=BG_COLOR)
url_label.grid(row=0, column=0, pady=(10, 2))

url_entry = Entry(root, width=35)
url_entry.grid(row=1, column=0, pady=(0, 8))


# FRAME PRE TLAČIDLÁ
buttons_frame = Frame(root)
buttons_frame.configure(bg=BG_COLOR)
buttons_frame.grid(row=2, column=0, pady=5)

button = Button(
    buttons_frame,
    text='Generate QR Code',
    command=generate_qr_code,
    bg=BG_COLOR
)
button.grid(row=0, column=0, padx=(0, 20))


open_folder_button = Button(
    buttons_frame,
    text="📂",
    width=3,
    command=open_qr_folder,
    bg=BG_COLOR
)
buttons_frame.configure(bg=BG_COLOR)
open_folder_button.grid(row=0, column=1, padx=(23, 0))


clear_button = Button(
    buttons_frame,
    text='🗑',
    width=3,
    command=clear_qr,
    bg=BG_COLOR
)
clear_button.grid(row=0, column=2, padx=(5, 0))

# QR frame – pevne rezervovane miesto
qr_frame = Frame(root, height=230)

qr_frame.grid(row=3, column=0)
qr_frame.grid_propagate(False)   #  ZAKAZE ZMENU VYSKY

qr_label = Label(qr_frame, cursor='hand2', bg=BG_COLOR)
qr_label.pack(expand=True)

# Author label / @ footer frame
footer_frame = Frame(root, bg=BG_COLOR)
footer_frame.grid(row=4, column=0, pady=(5, 5))

author_label = Label(
    footer_frame,
    text="© 2026 Igor Vitovský | github.com/igvisk",
    fg="gray",
    cursor="hand2",
    font=("Arial", 9),
    bg=BG_COLOR
)
author_label.pack()

# bind clipboard
qr_frame.bind("<Button-1>", copy_qr_to_clipboard)
qr_label.bind("<Button-1>", copy_qr_to_clipboard)

# bind footer
footer_frame.bind("<Button-1>", open_github)
author_label.bind("<Button-1>", open_github)


root.mainloop()
