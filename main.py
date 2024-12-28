import tkinter
import tkinter.filedialog
from pytubefix import YouTube
import customtkinter


class YouTubeDownloadApp:
    def __init__(self):
        # INITIALIZATION OF CORE VARIABLES, OBJECTS AND GENERAL INTERFACE
        self.app = customtkinter.CTk()
        self.app.geometry("800x480")
        self.app.title("YouTube Downloader")
        self.url = tkinter.StringVar()
        self.path = tkinter.StringVar()
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        # Creation of GUI elements for the app
        self.title = customtkinter.CTkLabel(
            self.app, text="Enter YouTube link")
        self.title.pack(padx=10, pady=10)

        self.link = customtkinter.CTkEntry(
            self.app, width=350, height=40, textvariable=self.url)

        self.choose_path_button = customtkinter.CTkButton(
            self.app, text="Choose a directory", command=self.choose_directory
        )

        self.file_path = customtkinter.CTkEntry(
            self.app, width=350, height=40, textvariable=self.path
        )

        self.percentage = customtkinter.CTkLabel(self.app, text="0%")

        self.prog_bar = customtkinter.CTkProgressBar(self.app, width=350)
        self.prog_bar.set(0)

        self.download_button = customtkinter.CTkButton(
            self.app, text="Download NOW!", command=lambda: self.download_video()
        )
        self.download_button.configure(state="disabled")

    def _layout_widgets(self):
        # Packing of GUI elements
        self.title.pack(padx=10, pady=10)
        self.link.pack()
        self.choose_path_button.pack(padx=10, pady=10)
        self.file_path.pack()
        self.percentage.pack()
        self.prog_bar.pack()
        self.download_button.pack(padx=10, pady=10)

    def choose_directory(self):
        # This fucntion uses the tkinter method to ask the user for a directory to
        # download video. If the directory url exists, sets the path to the directory
        # URL and enables the download Button. Else, the download button is disabled-
        save_path = tkinter.filedialog.askdirectory()
        if save_path:
            self.path.set(save_path)
            self.download_button.configure(state="normal")
        else:
            self.download_button.configure(state="disabled")

    def download_video(self):
        # This is the key function of the whole application
        # it gets the url and the path of the host pc to download
        # the video.
        # It filters and orders by resolution, downloading the
        # highest resolution possible
        url = self.url.get()
        save_path = self.path.get()
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            print(f'downloading {yt.title} ...')
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'bitrate').desc().first()
            streams.download(output_path=save_path)
        except Exception as e:
            print(e)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        per = int(bytes_downloaded / total_size * 100)
        # print(per)
        self.percentage.configure(text=f'{per}%')
        self.percentage.update()
        self.prog_bar.set(per/100)

    def run(self):
        self.app.mainloop()


if __name__ == '__main__':
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = YouTubeDownloadApp()
    app.run()
