import tkinter as tk
from tkinter import messagebox
import keyboard
import requests
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import sys
import os

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FGtranslate")
        self.root.attributes('-topmost', True)  # Pencerenin her zaman üstte kalmasını sağlar
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)  # Pencereyi kapatma düğmesine basıldığında tamamen kapat

        # İkonu ekliyoruz
        self.icon_path = self.resource_path('icon.png')
        self.root.iconphoto(False, ImageTk.PhotoImage(file=self.icon_path))

        # Frame oluşturalım
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Enter a word:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.frame)
        self.entry.pack(pady=5)

        self.entry.bind('<Return>', lambda event: self.lookup_word())

        self.button = tk.Button(self.frame, text="Lookup", command=self.lookup_word)
        self.button.pack(pady=5)

        self.result = tk.Text(self.frame, height=10, width=50, wrap='word')
        self.result.pack(pady=5, padx=10)

        self.history_label = tk.Label(self.frame, text="Recent Searches: (WIN+ALT+T to toggle window)")
        self.history_label.pack(pady=5)

        self.history = tk.Label(self.frame, text="", anchor='w', justify='left')
        self.history.pack(pady=5, padx=10)

        self.search_history = []

        root.bind('<Escape>', self.hide)

        # Alt menü çubuğu
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side='bottom', fill='x')
        self.about_button = tk.Button(self.bottom_frame, text="About", command=self.show_about)
        self.about_button.pack(side='left', padx=10, pady=5)

        # Sistem tepsisi ikonu
        self.icon = None
        self.create_tray_icon()

    def resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def lookup_word(self):
        word = self.entry.get()
        if word:
            self.add_to_history(word)
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if response.status_code == 200:
                data = response.json()
                definitions = data[0]["meanings"]
                self.result.delete('1.0', tk.END)
                for meaning in definitions:
                    part_of_speech = meaning["partOfSpeech"]
                    self.result.insert(tk.END, f"{part_of_speech.capitalize()}:\n")
                    for definition in meaning["definitions"]:
                        self.result.insert(tk.END, f"- {definition['definition']}\n")
                        if 'example' in definition:
                            self.result.insert(tk.END, f"  e.g. {definition['example']}\n")
                    self.result.insert(tk.END, "\n")
            elif word == "AEBASOL":
                self.result.delete('1.0', tk.END)
                self.result.insert(tk.END, "lol thats me")
            elif word == "FGtranslate":
                self.result.delete('1.0', tk.END)
                self.result.insert(tk.END, "she is tired, let her rest. Translation is hard work...")
            else:
                self.result.delete('1.0', tk.END)
                self.result.insert(tk.END, "Word not found.")

    def add_to_history(self, word):
        if word not in self.search_history:
            self.search_history.insert(0, word)
            if len(self.search_history) > 3:
                self.search_history.pop()
            self.update_history_display()

    def update_history_display(self):
        history_display = ""
        for word in self.search_history:
            if len(word) > 10:
                word = word[:10] + "..."
            history_display += word + " | "
        self.history.config(text=history_display.rstrip(" | "))

    def show(self, event=None):
        self.root.deiconify()
        self.entry.focus_set()  # Giriş kutusuna odaklan

    def hide(self, event=None):
        self.root.withdraw()

    def hide_window(self):
        self.root.withdraw()
        self.show_notification("FGtranslate", "The app is still running in the background. Use WIN+ALT+T to show the window again.")

    def create_tray_icon(self):
        image = Image.open(self.icon_path)
        self.icon = pystray.Icon("FGtranslate", image, "FGtranslate", self.create_menu())
        self.icon.run_detached()

    def create_menu(self):
        return pystray.Menu(
            item('Show', self.show_window),
            item('Exit', self.exit_app)
        )

    def show_window(self):
        self.root.deiconify()
        self.entry.focus_set()  # Giriş kutusuna odaklan

    def exit_app(self):
        if self.icon:
            self.icon.stop()
        self.root.quit()  # Tkinter uygulamasını düzgün kapatır

    def show_notification(self, title, message):
        messagebox.showinfo(title, message)

    def show_about(self):
        about_text1 = (
            "In the vast expanse of cyberspace, where knowledge once was held with grace, "
            "Now doth the giant Google stand, with all the world's data in its hand. "
            "But oh, what woes hath it brought forth, a kingdom lost, a barren north. "
            "For every search, a thousand ads, in this commerce-driven world of fads. "
            "Methinks the Bard would frown and chide, at such a breach of human pride. "
            "No longer dost we seek the truth, but filter through the marketing sleuth. "
            "Google's algorithms, cold and stark, hath led us from the knowledge ark. "
            "In days of yore, the library stood, a beacon of the common good. "
            "Yet now we drift on digital seas, our minds confined to bytes and keys. "
            "Oh, Google, thou art vast and grand, but dost thou truly understand, "
            "The essence of the quest we seek, the answers that our souls do speak? "
            "Would that we could turn the page, to wisdom of a bygone age. "
            "Where knowledge bloomed in written word, not dictated by the Google herd. "
            "Yet here we stand, in twenty-four, and ask, what future lies in store?"
        )
        messagebox.showinfo("About FGtranslate", about_text1)
        about_text2 = (
            "FGtranslate is a simple dictionary app that uses the DictionaryAPI to provide word definitions."
            "\n\nCreated by AEBASOL"
        )
        messagebox.showinfo("About FGtranslate", about_text2)

    def toggle_window(self):
        if self.root.state() == 'withdrawn':
            self.show_window()  # show metodu yerine show_window metodu kullanıldı
        else:
            self.hide()

def main():
    root = tk.Tk()
    root.withdraw()  # Start with the window hidden
    app = DictionaryApp(root)
    keyboard.add_hotkey('win+alt+t', app.toggle_window)
    root.mainloop()

if __name__ == "__main__":
    main()
