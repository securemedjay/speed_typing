from tkinter import *
from tkinter import messagebox

text = "Google LLC an American is multinational technology company is " \
       "that focuses on artificial intelligence,[10] search engine, " \
       "online advertising, cloud computing, computer software, quantum computing, " \
       "e-commerce, and consumer electronics. It has been referred to as the" \
       " and one of the world's most valuable brands due to its market dominance, data collection, a"
FONT = ("Courier", 15, "normal")

# Create Window
window = Tk()
window.title("Type Speed Counter")
window.geometry("500x500+300+200")  # sets the size of the window and the position on the user desktop

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


def stop():
    """ Resets timer and wpm to zero. """

    global secs, wpm
    secs = 0
    wpm = 0
    WPM_label.configure(text=f"WPM: {wpm}")


# WPM score label
WPM_label = Label(text=f"WPM: {wpm}", font=("Arial", 30, "bold"), pady=30)
WPM_label.pack()

# Welcome text label
welcome = Label(text="Start by typing the following text and get your WPM", font=("Arial", 15, "bold"))
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
btn = Button(text="Stop", command=stop, fg="red")
btn.pack()

window.mainloop()
