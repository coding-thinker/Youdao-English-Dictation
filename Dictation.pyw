import tkinter as tk
import requests as r
import random
import mp3play
import time
import os
import os.path
from bs4 import BeautifulSoup as B
import tkinter.messagebox as tkmsgbox

error = []
count = 0
word = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36'}


def gettrans(wd):
    try:
        global clip
        clip = None
        res = r.get('https://youdao.com/w/%s' % wd, timeout=(2, 5))
        res.encoding = res.apparent_encoding
        page = B(res.text, features='html.parser')
        transcontainer = page.find('div', class_='trans-container')
        if transcontainer != None:
            translation = transcontainer.text.strip().replace('\n', '  ')
        else:
            translation = 'No-translation'
        translation = ' '.join(translation.split())
        phonetic = page.find('span', class_='phonetic')
        if phonetic != None:
            phoneticsymbol = phonetic.text.strip()
        else:
            phoneticsymbol = 'No-phonetic-symbol'
        return (translation, phoneticsymbol)
    except Exception as e:
        print(e)
        tkmsgbox.showinfo(title='Error', message=e)


def getaudio(inword: str):
    try:
        res = r.get('http://dict.youdao.com/dictvoice?audio=%s&type=1' % inword, timeout=(2, 5))
        res.raise_for_status()
        with open('temp.mp3', 'wb') as f:
            f.write(res.content)
        return 1
    except Exception as e:
        print(e)
        tkmsgbox.showinfo(title='Error', message=e)
        return 0


def save(*args):
    try:
        if os.path.exists('temp.mp3'):
            os.remove('temp.mp3')
        progress_var.set('You have %d error(s)' % len(error))
        if len(error):
            with open(time.ctime().replace(':', '.') + '.txt', 'w') as f:
                f.write('\n'.join(error))
    except Exception as e:
        print(e)
        tkmsgbox.showinfo(title='Error', message=e)


def start(*args):
    try:
        res = r.get('http://dict.youdao.com/')
        res.raise_for_status()
    except Exception as e:
        tkmsgbox.showinfo(title='Error', message='Internet not conntected.')
        return
    try:
        path = path_entry.get()
        global number
        number = int(number_entry.get())
        global choice
        with open(path, 'rb') as f:
            sample = f.readlines()
        random.shuffle(sample)
        if number > len(sample):
            number = len(sample)
        choice = random.sample(sample, number)
        nextitem()
    except Exception as e:
        print(e)
        tkmsgbox.showinfo(title='Error', message=e)
        tkmsgbox.showinfo(title='Error', message='Check the file path and word number')


def playaudio(*args):
    try:
        global clip
        clip = mp3play.load('temp.mp3')
        clip.play()
    except Exception as e:
        print(e)
        tkmsgbox.showinfo(title='Error', message=e)
        tkmsgbox.showinfo(title='Error', message='Maybe you have saved the file and ended the test, please start again')


def nextitem(*args):
    global count
    global choice
    global error
    global word
    global worded
    worded = word
    count += 1
    if len(choice):
        word = choice.pop().decode('utf-8')
        word = word.strip()
        ret = getaudio(word)
        if ret:
            progress_var.set(str(count) + '/' + str(number))
            playaudio()
            answer_entry.focus_set()
        else:
            nextitem()
    else:
        progress_var.set('You have %d error(s)' % len(error))


def check(*args):
    if word == answer_entry.get().strip():
        key_var.set('Okay:  ' + word)
    else:
        key_var.set('error:' + word)
        error.append(word)
    trans, phon = gettrans(word)
    phonetic_var.set(phon)
    answer_entry.delete(0, 'end')
    try:
        text.delete('1.0', 'end')
    except Exception as e:
        print(e)
    text.insert('end', trans)
    nextitem()


def erase():
    if eraseability.get():
        error.remove(worded)
        progress_var.set('error erased')
    else:
        tkmsgbox.showinfo(title='Error', message='Function not activated')


root = tk.Tk()
root.title('Dictation')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 500
height = 200
x = (screen_width - width) / 2
y = (screen_height - height) / 2
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.minsize(width, height)
root.maxsize(width, height)

progress_var = tk.StringVar()
progress_var.set('Here shows the progress')
progress_label = tk.Label(root, textvariable=progress_var)
progress_label.place(x=5, y=0)

key_var = tk.StringVar()
key_var.set('Here shows keys')
key_label = tk.Label(root, textvariable=key_var)
key_label.pack(side='top')

phonetic_var = tk.StringVar()
phonetic_var.set('Here shows phonetic')
phonetic_label = tk.Label(root, textvariable=phonetic_var)
phonetic_label.pack(side='top')

eraseability = tk.IntVar()
eraseable = tk.Checkbutton(root, text='Error erase-ability', variable=eraseability, onvalue=1, offvalue=0)
eraseable.place(x=5, y=90)

start_button = tk.Button(root, text='start', command=start)
start_button.place(x=20, y=120)

answer_entry = tk.Entry(root, show=None)
answer_entry.bind("<Return>", check)
answer_entry.pack()

play_button = tk.Button(root, text='play', command=playaudio)
play_button.pack()

save_button = tk.Button(root, text='save', command=save)
save_button.pack()

erase_button = tk.Button(root, text='erase', command=erase)
erase_button.place(x=60, y=120)

path_init = tk.StringVar()
path_init.set('Here is a full path to a txt file')
path_entry = tk.Entry(root, show=None,textvariable=path_init)
path_entry.bind("<Return>", start)
path_entry.place(x=5, y=30)

number_init = tk.StringVar()
number_init.set('How many words do you want?')
number_entry = tk.Entry(root, show=None, textvariable=number_init)
number_entry.bind("<Return>", start)
number_entry.place(x=5, y=60)

test_var = tk.StringVar()
text = tk.Text(root, wrap='char', width=20, height=12)
text.place(x=490, y=0, anchor='ne')

root.mainloop()
