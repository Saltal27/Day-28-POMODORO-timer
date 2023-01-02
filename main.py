from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
break_time = -1
initial_timer = ""
cycles_num = 0

# ---------------------------- TIMER RESET ------------------------------- #


def reset_pomodoro():
    global cycles_num
    global reps
    global break_time

    timer.config(text="Timer", fg=GREEN)
    window.after_cancel(initial_timer)
    canvas.itemconfig(timer_text, text="00:00")
    reps = 0
    break_time = -1
    check_marks.config(text="")
    cycles_num = 0
    cycles_text.config(text="")
    cycles_text.grid(column=0, row=0)


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global break_time

    if break_time < 0:
        timer.config(text="Work", foreground=RED)
        countdown(WORK_MIN * 60)
    else:
        if reps % 4 == 0:
            countdown(LONG_BREAK_MIN * 60)
            timer.config(text="Break", foreground=GREEN)
        else:
            countdown(SHORT_BREAK_MIN * 60)
            timer.config(text="Break", foreground=PINK)

    if reps > 0:
        if reps % 4 == 0:
            check_marks.config(text="✔✔✔✔")
        elif reps % 3 == 0:
            check_marks.config(text="✔✔✔")
        elif reps % 2 == 0:
            check_marks.config(text="✔✔")
        else:
            check_marks.config(text="✔")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(count):
    global initial_timer

    count_min = math.floor(count / 60)
    count_sec = math.floor(count % 60)
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        initial_timer = window.after(1000, countdown, count - 1)
    else:
        global break_time
        global reps
        global cycles_num

        if break_time < 0:
            reps += 1
        else:
            if reps % 4 == 0:
                check_marks.config(text="")
                reps = 0
                cycles_num += 1
                cycles_text.grid(column=1, row=4)
                if cycles_num == 1:
                    cycles_text.config(text="You have completed\n 1 cycle so far!")
                else:
                    cycles_text.config(text=f"You have completed\n {cycles_num} cycles so far!")

        break_time *= -1
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer = Label(text="Timer", font=(FONT_NAME, 35, "bold"), foreground=GREEN, background=YELLOW)
timer.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="White", font=(FONT_NAME, 28, "bold"))
canvas.grid(column=1, row=1)

start = Button(text="Start", font=(FONT_NAME, 10, "bold"), highlightthickness=0, command=start_timer)
start.grid(column=0, row=2)

reset = Button(text="Reset", font=(FONT_NAME, 10, "bold"), highlightthickness=0, command=reset_pomodoro)
reset.grid(column=2, row=2)

check_marks = Label(font=(FONT_NAME, 15, "bold"), foreground=GREEN, background=YELLOW)
check_marks.grid(column=1, row=3)

cycles_text = Label(foreground=RED, font=(FONT_NAME, 15, "bold"))
cycles_text.config(pady=15)


window.mainloop()
