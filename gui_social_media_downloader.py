from customtkinter import *
from tkinter import filedialog, messagebox
import yt_dlp as ytdl
from yt_dlp.utils import download_range_func
from threading import Thread

# button configuration
button_configuration = {
    'border_width':2,
    'border_color':'#875cf5',
    'fg_color':'transparent',
    'hover_color':'#875cf5',
    'corner_radius':20,
    'text_color':'white'
}

# main_functions

def information():
    messagebox.showinfo('About the app','''-Welcome to Social Media Downloader\n-You can download from Youtube, Facebood, Instagram and other platforms \n-You can also choose a specific part from the video to download or the whole vide ''')

def convert_to_seconds(time):
    if not time:
        return None
    parts = time.split(':')
    if len(parts) == 2:
        minutes, seconds = parts[0], parts[1]
        return int(minutes) * 60 + int(seconds)
    elif len(parts) == 3:
        hours, minutes, seconds = parts[0], parts[1], parts[2]
        return int(hours)*3600 + int(minutes)*60 + int(seconds)
    else:
        messagebox.showerror('Error','Use format: HH:MM:SS or MM:SS')
        return None


def download_video(url,format_choice,quality,path,start_time,end_time):
    ydl_opts= {
        'format':quality,
        'outtmpl':f'{path}/%(title)s.%(ext)s',
        'verbose':True,
        'progress_hooks':[progress_hook]
    }
    if format_choice == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    if start_time or end_time:
        ydl_opts['download_ranges'] = download_range_func(None,[(start_time,end_time)])
        ydl_opts['force_keyframes_at_cuts'] = True

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return 'success'
        except Exception as e:
            return f'Error: {str(e)}'
        
        


def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d['_percent_str'].strip()
        percent_label.configure(text=percentage)
        progress_bar.set(float(d['downloaded_bytes']) / float(d['total_bytes']))
    elif d['status'] == 'finished':
        percent_label.configure(text='100%')
        progress_bar.set(1)


def get_parameters():
    url = url_entry.get()
    if not url:
        messagebox.showerror('Error!','Enter a valid link')
        return
    path = filedialog.askdirectory()
    if not path:
        messagebox.showerror('Error!','Enter a valid directory')
        return
    quality = quality_box.get()
    format_choice = format_box.get()
    str_start = start_entry.get() if start_entry.get() else None
    str_end = end_entry.get() if end_entry.get() else None
    start_time = convert_to_seconds(str_start)
    end_time = convert_to_seconds(str_end) 

    download_button.configure(text= 'Downloading...', state='disable',fg_color='#875cf5')
    url_entry.configure(state='readonly')
    start_entry.configure(state='readonly')
    end_entry.configure(state='readonly')
    percent_label.pack(pady=10)
    progress_bar.pack(pady=10)
    Thread(target=handle_downloading,args=(url,format_choice,quality,path,start_time,end_time)).start()


def handle_downloading(url,format_choice,quality,path,start_time,end_time):
    result = download_video(url,format_choice,quality,path,start_time,end_time)
    if result == 'success':
        messagebox.showinfo('Success!','Downloaded successfully :)')
    else:
        messagebox.showerror('Error!',f'Error happened :(\n{result}')
    action_frame.pack(pady=10)


    
def download_another():
    url_entry.delete(0,END)
    start_entry.delete(0,END)
    end_entry.delete(0,END)
    url_entry.configure(state='normal')
    start_entry.configure(state='normal')
    end_entry.configure(state='normal')
    download_button.configure(state='normal',text='Download',fg_color= 'transparent')
    percent_label.pack_forget()
    progress_bar.pack_forget()
    progress_bar.set(0)
    percent_label.configure(text='0%')
    action_frame.pack_forget()











# create the main window 
root = CTk()
root.title('Social Media Downloader')
root.geometry('700x580+450+150')
root.minsize(400,500)

# create the main frame and the main welcome label
main_frame = CTkFrame(root,fg_color='black',corner_radius=15)
main_frame.pack(fill='both',expand= True,padx=5,pady=5)

main_label = CTkLabel(main_frame,text='welcome to social media downloader'.title(),corner_radius=15 ,font=('helvatica',18,'bold'),fg_color='#35235c')
main_label.pack(fill=X, pady=5, padx=5)


# main widgets
url_label = CTkLabel(main_frame,text='Enter your URL:', font=('arial',18,'bold'),fg_color='black',text_color='white')
url_label.pack(pady=10)

url_entry = CTkEntry(main_frame,corner_radius=15,justify= 'center',width=400, font=('helvatica',16),border_color='#35235c')
url_entry.pack(pady=10)

quality_box = CTkComboBox(main_frame, values=['best','worst'],border_color='#875cf5',
                          dropdown_hover_color='#35235c',button_color='#875cf5',button_hover_color='#35235c',width=180,
                          state='readonly')
quality_box.pack(pady=10)
quality_box.set('best')

format_box = CTkComboBox(main_frame,values=['mp4','mp3'],border_color='#875cf5',
                          dropdown_hover_color='#875cf5',button_color='#875cf5',button_hover_color='#35235c',width=180,
                          state='readonly')
format_box.pack(pady=10)
format_box.set('mp4')

# start and end time 

start_end_frame = CTkFrame(main_frame,fg_color='black')
start_end_frame.pack(fill=X)

start_end_frame.rowconfigure(0,weight=1)
start_end_frame.rowconfigure(1,weight=1)
start_end_frame.columnconfigure(0,weight=1)
start_end_frame.columnconfigure(1,weight=1)

start_label = CTkLabel(start_end_frame,text='Start time (Optional):',font=('arial',16),bg_color='black')
start_label.grid(row=0,column=0, padx=10, pady=10)

start_entry = CTkEntry(start_end_frame,placeholder_text='HH:MM:SS',border_color='#35235c',corner_radius=10)
start_entry.grid(row=1,column=0, padx=10, pady=10)


end_label = CTkLabel(start_end_frame,text='End time (Optional):',font=('arial',16),bg_color='black')
end_label.grid(row=0,column=1, padx=10, pady=10)

end_entry = CTkEntry(start_end_frame,placeholder_text='HH:MM:SS',border_color='#35235c',corner_radius=10)
end_entry.grid(row=1,column=1, padx=10, pady=10)

download_button = CTkButton(main_frame , **button_configuration ,text='Download' ,command= get_parameters )
download_button.pack(pady=10)

# while downloading

percent_label = CTkLabel(main_frame,text='0%',fg_color='black')


progress_bar = CTkProgressBar(main_frame,width=400,progress_color='#875cf5')
progress_bar.set(0)



# after downloading 

action_frame = CTkFrame(main_frame,fg_color='black')


action_frame.columnconfigure(0, weight=1)
action_frame.columnconfigure(1, weight=1)

exit_button = CTkButton(action_frame,text='Close', border_width=2,
                        border_color='red',fg_color='transparent',
                        hover_color='red',corner_radius=20,text_color='white', command=root.quit)
exit_button.grid(row=0, column=0, padx=10)

another_button = CTkButton(action_frame,text='Another video',border_width=2,
                           border_color='blue',fg_color='transparent',
                           hover_color='blue',corner_radius=20,text_color='white',command=download_another)
another_button.grid(row=0,column=1,padx=10)





information_button = CTkButton(main_frame,text='About the app', **button_configuration, command=information)
information_button.pack(pady=10)


root.mainloop()