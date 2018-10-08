"""GUI for Imgur Album Downloader"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import queue
import threading
import time
import os
import re
import ImgurAlbum

class GUI:
    """Object-oriented GUI building"""
    def __init__(self):
        """Window initializer"""
        # Window generation
        self.main_window = tk.Tk()
        self.album_url = tk.StringVar()
        self.main_window.title("Imgur Album Downloader")
        self.main_window.resizable(0, 0)
        self.createWidgets()

        # Main loop
        self.main_window.mainloop()

    def createWidgets(self):
        self.album_input_lbl = tk.Label(self.main_window, text="Album")
        self.album_input_lbl.grid(column=0, row=0)
        
        self.album_input = tk.Entry(self.main_window, textvariable=self.album_url, width=50)
        self.album_input.grid(column=1, row=0)

        self.album_get_btn = tk.Button(self.main_window, text="Get Album", command=self.getAlbum)
        self.album_get_btn.grid(column=2, row=0)

    def verifyURL(self):
        match = re.search("imgur.com", self.album_url.get())
        if match:
            is_valid_url = True
        else:
            is_valid_url = False

        return is_valid_url

    def getAlbum(self):
        correct_url = self.verifyURL()
        if correct_url:
            url = self.album_url.get()
            imgurAlbum = ImgurAlbum.ImgurJSON(url)
            try:
                imgurAlbum.getAlbumJSON()
                if imgurAlbum.isAccessible():
                    imgurAlbum.downloadImages(os.getcwd())
                    self.album_input.delete(0, 'end')
                    messagebox.showinfo(title="Success", message="The album was downloaded successfully!")
                else:
                    messagebox.showwarning(message="Something happened")
            except:
                raise
        else:
            messagebox.showwarning(message="The url supplied is not valid!")
            self.album_input.delete(0, 'end')

class ThreadedClient:
    def __init__(self, master_window):
        self.master = master_window
        self.queue = queue.Queue()
        self.gui = 

def launch():
    GUI()

if __name__ == '__main__':
    launch()




