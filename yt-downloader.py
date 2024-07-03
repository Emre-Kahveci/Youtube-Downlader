from pytube import YouTube
import ffmpeg
from threading import Thread
import customtkinter as ctk
from time import sleep
from re import sub
import os
from pytube.exceptions import RegexMatchError

ctk.set_appearance_mode("dark")

def kapat():
    window.quit()
    window.destroy()

def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    indir_button.configure(text=f"%{round(pct_completed, 2)}")
    window.update()

# Zamanlayıcı değişkeni
timer = None

def on_key_release(event):
    global timer
    if timer is not None:
        window.after_cancel(timer)
    timer = window.after(300, lambda: ses_video_guncelle(event))

def convert_video(audio, video, dir_path, title, res, extension):
    """
    Adds the audio file to the video and converts the video to the desired format
    audio = audio file
    video = video file
    dir_path = AppData\Roaming\YT-Downloader
    title = title of the video
    res = selected resolution
    extension = desired extension
    """

    temp_file_path = f'{dir_path}\\temp.mp4'
    file_name = title + "_" + res + extension

    ffmpeg.output(ffmpeg.input(audio), ffmpeg.input(video), temp_file_path, codec='copy').run(overwrite_output=True) # merge the video and audio

    file_path = ctk.filedialog.asksaveasfilename(defaultextension=extension,
                                              filetypes=[("Video files", f"*{extension}"),
                                                         ("All files", "*.*")],
                                              initialfile=file_name) # user choose where and what name the file will be saved with filedialog
     
    os.replace(temp_file_path, file_path)
    os.remove(audio)
    os.remove(video)

def button_configure(button, text, button_state=None, sleep_time=0):
    """Function that configures the button, refreshes the screen and waits for the desired time"""
    button.configure(text=text, state=button_state)
    window.update()
    sleep(sleep_time)

def combobox_configure(cbox, values):
    """Function that configures the combobox, and set the first value"""
    cbox.configure(values=values)
    cbox.set(values[0])

def download_video(yt, title, extension, res, dir_path):
    """Function that downloads the video (uses the "convert_video" function to combine and save with the audio file)"""
    video = yt.streams.filter(file_extension="mp4", resolution=res).last().download(filename_prefix="video", output_path=dir_path)
    audio = yt.streams.filter(only_audio=True).order_by('abr').last().download(filename_prefix="audio", output_path=dir_path)
    
    button_configure(indir_button, "Dönüştürülüyor")
        
    convert_video(audio, video, dir_path, title, res, extension)

    button_configure(indir_button, "İndirme tamamlandı.", sleep_time=1.5)

    button_configure(indir_button, "İndir", button_state=ctk.NORMAL)

def download_audio(yt, extension, res):
    """Function that downloads the audio"""
    audio = yt.streams.filter(only_audio=True, abr=res).last().download()
    pre, ext = os.path.splitext(audio)
    os.rename(audio, pre + "_" + res + extension)

    button_configure(indir_button, "İndirme tamamlandı.", sleep_time=1.5)

    button_configure(indir_button, "İndir", button_state=ctk.NORMAL)

def download_main():
    """
    main function of downloads. 
    It performs main operations such as creating the pytube element and removing characters in the title that do not comply with Windows name rules.
    """
    link = link_entry.get()
    type = radio_var.get()
    ext = uzanti_cmbox.get()
    res = cozunurluk_cmbox.get()
    
    yt = YouTube(link, on_progress_callback=on_progress)
    title = sub(r'[?\"\\/*<>:|]', '', yt.title)

    dir_path = os.path.join(os.environ['APPDATA'], 'YT-Downloader')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    button_configure(indir_button, "İndiriliyor", button_state=ctk.DISABLED)
    
    if type == 1:
        Thread(target=download_video, args=(yt, title, ext, res, dir_path)).start()
    elif type == 2:
        Thread(target=download_audio, args=(yt, ext, res, dir_path)).start()
    else:
        print("Hata")

def cozunurluk_cek(link):
    """Gets the resolution options of the video to be downloaded"""
    try:
        yt = YouTube(link)
        c_values = [".mp4", ".webm"]
        k_values = list(dict.fromkeys([stream.resolution for stream in yt.streams.order_by('resolution')]))
        
        combobox_configure(uzanti_cmbox, c_values)
        combobox_configure(cozunurluk_cmbox, k_values)
        button_configure(indir_button, "İndir", button_state=ctk.NORMAL)
    except RegexMatchError:
        sleep(.2)

def abr_cek(link):
    """Gets the abr options of the audio to be downloaded"""
    try:
        yt = YouTube(link)
        c_values = [".mp3", ".mp4", ".webm"]
        k_values = list(dict.fromkeys([stream.abr for stream in yt.streams.filter(only_audio=True).order_by('abr')]))
        
        combobox_configure(uzanti_cmbox, c_values)
        combobox_configure(cozunurluk_cmbox, k_values)
        button_configure(indir_button, "İndir", button_state=ctk.NORMAL)
    except RegexMatchError:
        sleep(.2)

def ses_video_guncelle(event=0):
    """Updates the quality combobox when switching between audio/video."""
    r_var = radio_var.get()
    link = link_entry.get()

    button_configure(indir_button, "yükleniyor", button_state=ctk.DISABLED)

    if r_var == 1:
        Thread(target=cozunurluk_cek, args=(link,)).start()

    elif r_var == 2:
        Thread(target=abr_cek, args=(link,)).start()

window = ctk.CTk()
window.title("YouTube Downloader")

frame = ctk.CTkFrame(window)
frame.pack(pady=10)

link_entry = ctk.CTkEntry(frame, width=350)
link_entry.grid(row=0, column=0, columnspan=4, padx=5)
link_entry.focus()

link_entry.bind('<KeyRelease>', on_key_release)

cozunurluk_cmbox = ctk.CTkComboBox(frame, values=["çözünürlük"], width=100)
cozunurluk_cmbox.grid(row=0, column=4, padx=5)

radio_var = ctk.IntVar(value=1)
mp4_rb = ctk.CTkRadioButton(master=frame, text="video", variable=radio_var, value=1, command=ses_video_guncelle)
mp4_rb.grid(row=1, column=0, pady=5, padx=(0, 5), sticky="e")
mp3_rb = ctk.CTkRadioButton(master=frame, text="ses", variable=radio_var, value=2, command=ses_video_guncelle)
mp3_rb.grid(row=1, column=1, pady=5, padx=(0, 5), sticky="e")

uzanti_cmbox = ctk.CTkComboBox(frame, values=[".mp4", ".webm"], width=90)
uzanti_cmbox.grid(row=1, column=2, pady=5, padx=5, sticky="w")

indir_button = ctk.CTkButton(frame, text="İndir", command=download_main, width=100, text_color_disabled='black')
indir_button.grid(row=1, column=4, padx=5, sticky="w")

window.protocol("WM_DELETE_WINDOW", kapat)

window.mainloop()