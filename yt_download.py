import time
from tkinter import *
from pytube import YouTube
import os

root = Tk()
root_w, root_h = 640, 480
root_ws, root_hs = root.winfo_screenwidth(), root.winfo_screenheight()
root_x, root_y = (root_ws / 2) - (root_w / 2), (root_hs / 2) - (root_h / 2)
root.geometry('%dx%d+%d+%d' % (root_w, root_h, root_x, root_y))
root.resizable = False
root.title("Download your favourite video from YouTube!")
Label(root, text="YouTube Video Downloader", font="arial 20 bold").place(x=125, y=10)
link = StringVar()
Label(root, text="Paste Your Link Here", font="arial 15").place(x=225, y=200)

Entry(root, width=95, textvariable=link).place(x=35, y=230)


def downloader():
    correct_itag = 0
    path = "E:\\yt_tests\\"
    yt = YouTube(str(link.get()))

    itag = yt.streams.filter(only_video=True, res='1440p', mime_type='video/mp4').itag_index
    flag = 1
    if not itag.keys():
        itag = yt.streams.filter(only_video=True, res='1440p', mime_type='video/webm').itag_index
        flag = 2
    if not itag.keys():
        itag = yt.streams.filter(only_video=True, res='1080p', mime_type='video/webm').itag_index
        flag = 1
    if not itag.keys():
        itag = yt.streams.filter(only_video=True, res='1080p', mime_type='video/webm').itag_index
        flag = 2

    for key in itag:
        correct_itag = int(key)
    if flag == 1:
        flag = 'mp4'
    else:
        flag = 'webm'
    yt.streams.get_by_itag(correct_itag).download(f'{path}', filename=f'video.{flag}')
    yt.streams.get_by_itag(140).download(f'{path}', filename=f'audio.mp4')

    cmd = f'ffmpeg -i E:\\yt_tests\\audio.mp4 -i E:\\yt_tests\\video.{flag} -acodec copy -vcodec copy ' \
          'E:\\yt_tests\\final_0.mp4'
    os.system(cmd)
    time.sleep(5)
    os.remove(f'E:\\yt_tests\\video.{flag}')
    os.remove('E:\\yt_tests\\audio.mp4')

    for i in range(1, 100):
        if os.path.isfile(f'E:\\yt_tests\\final_{i}.mp4'):
            continue
        elif not os.path.isfile(f'E:\\yt_tests\\final_{i}.mp4'):
            os.rename('E:\\yt_tests\\final_0.mp4', f'E:\\yt_tests\\final_{i}.mp4')
            break
    ready_window()


def ready_window():
    ready = Tk()
    ready_w, ready_h = 300, 150
    ready_x, ready_y = (root_ws / 2) - (ready_w / 2), (root_hs / 2) - (ready_h / 2)
    ready.geometry('%dx%d+%d+%d' % (ready_w, ready_h, ready_x, ready_y))
    ready.resizable = False
    ready.attributes('-topmost', True)
    Label(ready, text="Downloaded", font="arial 20 bold").place(x=62, y=30)
    Button(ready, text="OK", font="arial 15", bg="violet", padx=2,
           command=ready.destroy, ).place(x=125, y=80)
    root.attributes('-topmost', True)


def exit():
    os.system('explorer.exe E:\\yt_tests')
    root.destroy()


Button(root, text="EXIT", font="arial 15 bold", bg="grey", fg='white', padx=2,
       command=exit).place(x=285, y=310)
Button(root, text="DOWNLOAD", font="arial 15", bg="violet", padx=2,
       command=downloader).place(x=250, y=260)

root.mainloop()
