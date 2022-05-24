from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3

root = Tk()

root.title("Mp3 Player")
root.geometry("1000x500")

# initialize pygame
pygame.mixer.init()

# create functions for time
def play_time():
    # getting the current time and conerting it into time format 
    current_time = pygame.mixer.music.get_pos() / 1000
    cnvrted_crnt_time = time.strftime('%M:%S', time.gmtime(current_time))

        #   ---find current song total length---
    # getting the song
    song = playlist_box.get(ACTIVE)
    # reconstruct song title
    song = f'D:/mp3_player/audio{song}.mp3'
    song_mut = MP3(song)
    # getting the current time and conerting it into time format 
    global song_length 
    song_length = song_mut.info.length
    cnvrted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # displaying the time in the status bar
    if current_time >= 1:
        status_bar.config(text=f'Time Elapsed: {cnvrted_crnt_time} of {cnvrted_song_length}')
    # looping this function for every 1sec as to update the time for each sec
    status_bar.after(1000, play_time)


# create functions to add songs into playlist
def add_song():
    song = filedialog.askopenfilename(initialdir="audio/", title="choose a song", filetypes=(("mp3 Files","*.mp3"), ))
    # striping the title
    song = song.replace("D:/mp3_player/audio", "")
    song = song.replace(".mp3", "")
    # adding song to playlist
    playlist_box.insert(END, song)
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="audio/", title="choose a song", filetypes=(("mp3 Files","*.mp3"), ))
    # loop thru song list
    for song in songs:
        # striping the title
        song = song.replace("D:/mp3_player/audio", "")
        song = song.replace(".mp3", "")
        # adding song to playlist
        playlist_box.insert(END, song)

# create function to delete songs from playlist
def delete_song():
    playlist_box.delete(ANCHOR)
def delete_all_songs():
    playlist_box.delete(0, END)

# create button functions

def play():
    # getting the song
    song = playlist_box.get(ACTIVE)
    # reconstruct song title
    song = f'D:/mp3_player/audio{song}.mp3'
    # display song at label
    my_label.config(text=song)
    # load and play the song with pygame mixer
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # get song time
    play_time()

def stop():
    pygame.mixer.music.stop()
    # clear playlist selection
    playlist_box.selection_clear(ACTIVE)
    # clear current playing label
    my_label.config(text="")
    # als0 clear the status bar
    status_bar.config(text='')

global paused
paused = False
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pause
        pygame.mixer.music.pause()
        paused = True

def next_song():
    # get current song and add it 1
    next_one = playlist_box.curselection()
    next_one = next_one[0] + 1
    # getting, loading and playing the song 
    song = playlist_box.get(next_one)
    # reconstruct song title
    song = f'D:/mp3_player/audio{song}.mp3'
    # display song at label
    my_label.config(text=song)
    # load and play the song with pygame mixer
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear, move and set playlist active bar
    playlist_box.selection_clear(0, END)
    playlist_box.activate(next_one)
    playlist_box.selection_set(next_one, last=None)

def prev_song():
    # get current song and add it 1
    last_one = playlist_box.curselection()
    last_one = last_one[0] - 1
    # getting, loading and playing the song 
    song = playlist_box.get(last_one)
    # reconstruct song title
    song = f'D:/mp3_player/audio{song}.mp3'
    # display song at label
    my_label.config(text=song)
    # load and play the song with pygame mixer
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # clear, move and set playlist active bar
    playlist_box.selection_clear(0, END)
    playlist_box.activate(last_one)
    playlist_box.selection_set(last_one, last=None)




# create playlist box
playlist_box = Listbox(root, bg="gray1", fg="LightPink1", width=100, selectbackground="dark orange")
playlist_box.pack(pady=20)

# define button images for controls
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
back_btn_img = PhotoImage(file='images/back50.png')

# create button frame
control_frame = Frame(root)
control_frame.pack(pady=20)

# create play,pause etc buttons
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song) 
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=prev_song)

play_button.grid(row=0, column=0, padx=10)
pause_button.grid(row=0, column=1, padx=10)
stop_button.grid(row=0, column=2, padx=10)
forward_button.grid(row=0, column=3, padx=10)
back_button.grid(row=0, column=4, padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# create add song menu dropdown
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="add a song into playlist", command=add_song)
add_song_menu.add_command(label="add many songs into playlist", command=add_many_songs)

# delete song menu dropdown
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="remove song", menu=remove_song_menu)
remove_song_menu.add_command(label="delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="delete all song from playlist", command=delete_all_songs)

# create status bar
status_bar = Label(root, text="", bd=5, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# current song label
my_label = Label(root, text="")
my_label.pack(pady=20)
 

root.mainloop()