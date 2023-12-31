# Flash Cards
# 17/07/2023
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# show next card function


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

# Flip Card Function


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# Is known function (removes known words from the to learn dict)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# Create Window
window = Tk()
window.title("Flash Cards")
window.config(padx=40, pady=40, bg=BACKGROUND_COLOR)


# Flip Card after 3 seconds
flip_timer = window.after(3000, func=flip_card)

# Add card image to canvas
canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(
    400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(
    400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(
    image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# call next card at the start of the program
next_card()

window.mainloop()
