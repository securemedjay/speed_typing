from tkinter import *
from tkinter import messagebox
import requests
from random import choice
import os

seed_text_list = ["hello", "boy"]  # DeepAI requires that you provide a seed text to generate the display text
FONT = ("Courier", 15, "normal")
text = ""
deep_ai_key = os.environ.get("DEEP_AI_KEY")  # storing DeepAI key as environment variable.
deep_ai_url = "https://api.deepai.org/api/text-generator"

# Create Window
window = Tk()
window.title("Type Speed Counter")
window.geometry("500x600+300+200")  # sets the size of the window and the position on the user desktop

#  Declare variables
user_word_list = []
secs = 0
timer_id = ""
wpm = 0


# Check user input to see if it is in line with displayed text
def check_align():
    """ Check user input to see if it is in line with displayed text. """

    display_list = text.split(" ")

    word = entry.get().strip()  # strip user word off leading and trailing spaces

    if word in display_list:
        user_word_list.append(word)
        word_index = user_word_list.index(word)
        index_list = [i for i, e in enumerate(display_list) if e == word]
        if word_index in index_list:
            return word
        else:
            user_word_list.remove(word)
            messagebox.showinfo(title="Out of Order", message="You typed a word out of order")
    else:
        messagebox.showinfo(title="Wrong Input", message="Wrong entry or incorrect spelling")


def timer(event=None):
    """ Starts a seconds counter from Zero as soon as the user presses a key in the text box. """

    global secs, timer_id
    entry.unbind("<KeyPress>")  # So the timer won't go crazy on multiple presses.
    secs += 1
    timer_id = window.after(1000, timer)


def calc_wpm(event=None):
    """ Calculates wpm by dividing number of words typed by time in minute. """

    global wpm
    word = check_align()
    time_in_min = secs / 60

    if word is not None:
        wpm = round(len(user_word_list) / time_in_min)
        WPM_label.configure(text=f"WPM: {wpm}")

    entry.delete(0, 'end')  # delete entry text each function is called


def refresh():
    """ Resets timer and wpm to zero. """

    global secs, wpm, user_word_list
    user_word_list = []
    generate_text()
    secs = 0
    wpm = 0
    display.configure(text=text)
    WPM_label.configure(text=f"WPM: {wpm}")


def generate_text():
    """ Generates display text using DeepAI api. """
    global text
    url = deep_ai_url
    seed_text = {
        "text": choice(seed_text_list),
    }
    headers = {
        "Api-Key": deep_ai_key
    }
    data = requests.post(url=url, data=seed_text, headers=headers)
    result = data.json()

    # check for out of range exception and retry if true
    try:
        text = result["output"].split("\n\n")[1].strip()
    except IndexError:
        generate_text()


generate_text()

# WPM score label
WPM_label = Label(text=f"WPM: {wpm}", font=("Arial", 30, "bold"), pady=30)
WPM_label.pack()

# Welcome text label
welcome = Label(text="Start by typing the following text and get your WPM. If you mistyped a word simply retype it",
                font=("Arial", 15, "bold"), wraplength=350)
welcome.pack()

# Display Text label
display = Label(text=text, anchor="center", height=15, width=50, wraplength=350, font=FONT, pady=30)
display.pack()

# Textbox
entry = Entry(window, font=('calibre', 10, 'normal'), justify="center", highlightthickness=1)
entry.pack(pady=10)

entry.bind("<KeyPress>", timer)
entry.bind("<space>", calc_wpm)

# Stop button
btn = Button(text="Refresh", command=refresh, fg="red")
btn.pack()

window.mainloop()
