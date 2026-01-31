#QRgenerator 

# pypng is required to app functionality!; anyway no import required, only have to it installed: pip install pypng

import pyqrcode
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io                           # clipboard
import win32clipboard               # clipboard  pip install pywin32
import os
import subprocess
import webbrowser

VERSION = "v0.7b"
BG_COLOR = "#ECE9E9"

class QRCodeGeneratorApp:
    def __init__(self):
        # --- ROOT ---
        self.root = Tk()
        self.root.title(f'QR Code Generator {VERSION}')
        self.set_window_geometry(300, 350)
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # Zistenie absolútnej cesty k priečinku, v ktorom sa nachádza skript
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Icon
        # try:
        #     icon_path = os.path.join(self.script_dir, "icon.ico")
        #     self.iconbitmap(icon_path)
        # except Exception as e:
        #      messagebox.showwarning("Upozornenie", f"Ikona sa nepodarila načítať:\n{e}")

        # globalna referencia na obrazok (teraz atribut triedy)
        self.photo_image = None
        #Ak neexistuje qr_code.png
        self.qr_path = None 

        # --- UI ---
        self.create_layout()
        self.bind_events()

    # --- FUNKCIE ---
       # Window geometry - Open app in the center of the screen         
    def set_window_geometry(self, width, height):
        # Obtain Screen resolution
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Position calculation of the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set position of the window to center 
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def generate_qr_code(self):
        text = self.url_entry.get().strip()
        if not text:
            return

        qr = pyqrcode.create(text, encoding='utf-8')       # diakritika

         # path to .png located in script_dir
        self.qr_path = os.path.join(self.script_dir, "qr_code.png")

        qr.png(self.qr_path, scale=5)

        image = Image.open(self.qr_path)

        self.open_folder_button.config(state=NORMAL)                        #odomknutie tlacidla open_folder_button po vygenerovani qr code

        # fix size of QR image
        image = image.resize((220, 220), Image.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(image)
        self.qr_label.config(image=self.photo_image)

    def open_qr_folder(self):
        if self.qr_path and os.path.exists(self.qr_path):
            subprocess.run(f'explorer /select,"{self.qr_path}"')

    def clear_qr(self):
        self.qr_label.config(image='')
        self.url_entry.delete(0, END)
        self.photo_image = None
        self.open_folder_button.config(state=DISABLED)

    def copy_qr_to_clipboard(self, event=None):
        if self.photo_image is None or not self.qr_path:
            return

    # otvor PNG znova ako PIL Image
        image = Image.open(self.qr_path).convert("RGB")

        output = io.BytesIO()
        image.save(output, "BMP")
        data = output.getvalue()[14:]                         # odstráni BMP header
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def open_github(self, event=None):                        # → event=None → aby fungovalo aj z klávesnice alebo iného volania.
        webbrowser.open_new("https://github.com/igvisk")

    # --- UI KONSTRUKCIA ---
    def create_layout(self):
        # --- GRID KONFIGURACIA ---
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

        self.url_label = Label(
            self.root,
            text='Enter text or URL',
            font=("Arial", 10, "bold"),
            bg=BG_COLOR
        )
        self.url_label.grid(row=0, column=0, pady=(10, 2))

        self.url_entry = Entry(self.root, width=35)
        self.url_entry.grid(row=1, column=0, pady=(0, 8))

        # FRAME PRE TLAČIDLÁ
        self.buttons_frame = Frame(self.root, bg=BG_COLOR)
        self.buttons_frame.grid(row=2, column=0, pady=5)

        self.generate_button = Button(
        self.buttons_frame,
        text='Generate QR Code',
        command=self.generate_qr_code,
        bg=BG_COLOR
        )
        self.generate_button.grid(row=0, column=0, padx=(0, 20))

        self.open_folder_button = Button(
        self.buttons_frame,
        text="📂",
        width=3,
        command=self.open_qr_folder,    
        state=DISABLED,                             #po prvom spusteni app bude btn disabled, aktivuje sa v generate_qr az ked subor existuje
        bg=BG_COLOR
        )
        self.open_folder_button.grid(row=0, column=1, padx=(23, 0))

        self.clear_button = Button(
        self.buttons_frame,
        text='🗑',
        width=3,
        command=self.clear_qr,
        bg=BG_COLOR
        )
        self.clear_button.grid(row=0, column=2, padx=(5, 0))

        # QR frame – pevne rezervovane miesto
        self.qr_frame = Frame(self.root, height=230)
        self.qr_frame.grid(row=3, column=0)
        self.qr_frame.grid_propagate(False)   # ZAKAZE ZMENU VYSKY

        self.qr_label = Label(self.qr_frame, cursor='hand2', bg=BG_COLOR)
        self.qr_label.pack(expand=True)

        # Footer
        self.footer_frame = Frame(self.root, bg=BG_COLOR)
        self.footer_frame.grid(row=4, column=0, pady=(5, 5))

        self.author_label = Label(
            self.footer_frame,
            text="© 2026 Igor Vitovský | github.com/igvisk",
            fg="gray",
            cursor="hand2",
            font=("Arial", 9),
            bg=BG_COLOR
        )
        self.author_label.pack()

    # --- BINDY ---
    def bind_events(self):
        # bind clipboard
        self.qr_frame.bind("<Button-1>", self.copy_qr_to_clipboard)
        self.qr_label.bind("<Button-1>", self.copy_qr_to_clipboard)

        # bind footer
        self.footer_frame.bind("<Button-1>", self.open_github)
        self.author_label.bind("<Button-1>", self.open_github)

    def run(self):
        self.root.mainloop()


# --- START APP ---
if __name__ == "__main__":
    app = QRCodeGeneratorApp()
    app.run()