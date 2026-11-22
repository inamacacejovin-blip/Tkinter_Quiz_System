import tkinter as tk
from tkinter import messagebox
import random
import os
 
 #Set of questions

QUESTIONS = [
    {
        "question": "Which device forwards packets between different networks?",
        "choices": ["A. Switch", "B. Hub", "C. Router", "D. Repeater"],
        "answer": "C",
    },
    {
        "question": "How many bits are in an IPv4 address?",
        "choices": ["A. 32", "B. 64", "C. 128", "D. 48"],
        "answer": "A",
    },
    {
        "question": "Which protocol translates domain names into IP addresses?",
        "choices": ["A. DHCP", "B. DNS", "C. FTP", "D. ARP"],
        "answer": "B",
    },
    {
        "question": "What is the default port number for HTTPS?",
        "choices": ["A. 80", "B. 21", "C. 25", "D. 443"],
        "answer": "D",
    },
    {
        "question": "Which OSI layer is responsible for logical addressing and routing?",
        "choices": ["A. Data Link", "B. Transport", "C. Session", "D. Network"],
        "answer": "D",
    },
    {
        "question": "Which protocol automatically assigns IP addresses to hosts?",
        "choices": ["A. DHCP", "B. DNS", "C. SNMP", "D. ICMP"],
        "answer": "A",
    },
    {
        "question": "Which command tests whether another host is reachable?",
        "choices": ["A. ipconfig", "B. ping", "C. netstat", "D. nslookup"],
        "answer": "B",
    },
    {
        "question": "How many bits are in a MAC address?",
        "choices": ["A. 32", "B. 64", "C. 48", "D. 128"],
        "answer": "C",
    },
    {
        "question": "In which topology is every device connected to one central device?",
        "choices": ["A. Bus", "B. Ring", "C. Mesh", "D. Star"],
        "answer": "D",
    },
    {
        "question": "Which transport protocol provides reliable, connection-oriented delivery?",
        "choices": ["A. UDP", "B. TCP", "C. IP", "D. ARP"],
        "answer": "B",
    },
]
 
 #Settings

TIME_LIMIT = 15  # seconds per question
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)
 
# Colors (white and green)
WHITE = "#FFFFFF"
GREEN_DARK = "#1B5E3B"      # header bars, main text accents
GREEN = "#2E8B57"           # buttons, progress bar
GREEN_LIGHT = "#E6F4EA"     # cards and boxes
GREEN_MID = "#BFE3C9"       # selected choice
TEXT = "#1F2D24"
MUTED = "#5F7467"
CORRECT = "#2E7D32"
WRONG = "#C62828"
 
FONT = "Segoe UI"
 
# WINDOW

root = tk.Tk()
root.title("NetBasics Quiz")
root.geometry("760x700")
root.configure(bg=WHITE)
root.resizable(False, False)
 

# QUIZ STATE

quiz_questions = []      # shuffled copy of QUESTIONS
current_question = 0     # index of the current question
score = 0
time_left = TIME_LIMIT
wrong_answers = []       # details of incorrect answers (for the review)
timer_job = None         # id of the scheduled timer, needed to cancel it
answered = False         # True once the question is submitted or time is up
 
selected_answer = tk.StringVar()   # holds the chosen letter ("A" to "D")
player_name = tk.StringVar()       # optional name typed on the start screen
 
# Widgets that change while the quiz is running
timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []
 
main_frame = tk.Frame(root, bg=WHITE)
main_frame.pack(fill="both", expand=True)
 
 

# HIGH SCORE (file handling)

def get_high_score():
    """Read the saved high score. Return 0 if the file is missing or invalid."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0
 
 
def save_high_score(new_score):
    """Save the score only if it beats the old high score. Return True if saved."""
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False
 
 

# HELPERS

def clear_screen():
    """Remove every widget from the main frame so a new screen can be built."""
    for widget in main_frame.winfo_children():
        widget.destroy()
 
 
def get_choice_text(question, letter):
    """Return the full choice text (for example 'B. ping') from its letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"
 
 
def make_button(parent, text, command, color=GREEN, fg=WHITE, width=12):
    """Create a flat, consistently styled button."""
    return tk.Button(
        parent, text=text, command=command, font=(FONT, 12, "bold"),
        bg=color, fg=fg, activebackground=GREEN_DARK, activeforeground=WHITE,
        relief="flat", bd=0, width=width, pady=7, cursor="hand2",
        disabledforeground="#A8B8AE",
    )
 
 
def make_header(title, subtitle=""):
    """Create the green bar at the top of a screen and return it."""
    header = tk.Frame(main_frame, bg=GREEN_DARK)
    header.pack(fill="x")
    tk.Label(header, text=title, font=(FONT, 22, "bold"),
             bg=GREEN_DARK, fg=WHITE).pack(anchor="w", padx=30, pady=(18, 0))
    tk.Label(header, text=subtitle, font=(FONT, 11),
             bg=GREEN_DARK, fg=GREEN_MID).pack(anchor="w", padx=30, pady=(0, 16))
    return header
 
 
def make_stat_box(parent, value, caption):
    """Create a small light-green box with a big value and a caption."""
    box = tk.Frame(parent, bg=GREEN_LIGHT)
    tk.Label(box, text=value, font=(FONT, 22, "bold"),
             bg=GREEN_LIGHT, fg=GREEN_DARK).pack(padx=20, pady=(12, 0))
    tk.Label(box, text=caption, font=(FONT, 10),
             bg=GREEN_LIGHT, fg=MUTED).pack(padx=20, pady=(0, 12))
    return box
 
 
# START SCREEN

def show_start_screen():
    clear_screen()
    make_header("NetBasics Quiz", "Test your Networking Fundamentals")
 
    body = tk.Frame(main_frame, bg=WHITE)
    body.pack(fill="both", expand=True, padx=30, pady=30)
 
    stats = tk.Frame(body, bg=WHITE)
    stats.pack(fill="x")
    make_stat_box(stats, str(len(QUESTIONS)), "Questions").pack(
        side="left", expand=True, fill="x", padx=(0, 8))
    make_stat_box(stats, f"{TIME_LIMIT}s", "Per question").pack(
        side="left", expand=True, fill="x", padx=8)
    make_stat_box(stats, f"{get_high_score()} / {len(QUESTIONS)}",
                  "High score").pack(side="left", expand=True, fill="x",
                                     padx=(8, 0))
 
    tk.Label(body, text="Pick an answer, then press Submit before the timer "
             "runs out.", font=(FONT, 11), bg=WHITE, fg=MUTED
             ).pack(pady=(30, 20))
 
    tk.Label(body, text="Your name (optional)", font=(FONT, 11, "bold"),
             bg=WHITE, fg=GREEN_DARK).pack(anchor="w")
    tk.Entry(body, textvariable=player_name, font=(FONT, 14), bg=GREEN_LIGHT,
             fg=TEXT, insertbackground=TEXT, relief="flat"
             ).pack(fill="x", ipady=8, pady=(4, 0))
 
    make_button(body, "Start Quiz", start_quiz, width=20).pack(pady=35)
 
 

# QUIZ FLOW

def start_quiz():
    """Reset everything and shuffle the questions (also used by Restart)."""
    global quiz_questions, current_question, score, wrong_answers
    stop_timer()
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))  # new shuffled list
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()
 
 
def show_question():
    """Build the question screen and start the countdown."""
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons
 
    clear_screen()
    answered = False
    selected_answer.set("")          # no radio button preselected
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]
    total = len(quiz_questions)
 
    # Green header: question number on the left, timer on the right
    header = tk.Frame(main_frame, bg=GREEN_DARK)
    header.pack(fill="x")
    tk.Label(header, text=f"Question {current_question + 1} of {total}",
             font=(FONT, 16, "bold"), bg=GREEN_DARK, fg=WHITE
             ).pack(side="left", padx=30, pady=16)
    tk.Label(header, text=f"Score: {score}", font=(FONT, 14, "bold"),
             bg=GREEN_DARK, fg=WHITE).pack(side="right", padx=30)
 
    # Progress bar under the header
    bar = tk.Canvas(main_frame, width=760, height=6, bg=GREEN_MID,
                    highlightthickness=0)
    bar.pack()
    bar.create_rectangle(0, 0, 760 * (current_question + 1) / total, 6,
                         fill=GREEN, width=0)
 
    body = tk.Frame(main_frame, bg=WHITE)
    body.pack(fill="both", expand=True, padx=30, pady=18)
 
    # Question card
    card = tk.Frame(body, bg=GREEN_LIGHT)
    card.pack(fill="x", pady=(0, 16))
    tk.Label(card, text=question["question"], font=(FONT, 16, "bold"),
             wraplength=660, justify="left", bg=GREEN_LIGHT, fg=TEXT
             ).pack(anchor="w", padx=18, pady=18)
 
    # Four choices. Each Radiobutton's value is its letter (A to D).
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(
            body, text=choice, variable=selected_answer, value=letter,
            font=(FONT, 13), indicatoron=0, anchor="w", padx=16, pady=9,
            bg=WHITE, fg=TEXT, selectcolor=GREEN_MID,
            activebackground=GREEN_LIGHT, activeforeground=TEXT,
            disabledforeground=TEXT, relief="solid", bd=1, cursor="hand2",
        )
        button.pack(fill="x", pady=4)
        choice_buttons.append(button)
 
    # Bottom row: feedback on the left, timer above Submit and Next on the right
    bottom = tk.Frame(body, bg=WHITE)
    bottom.pack(side="bottom", fill="x", pady=(10, 0))
    feedback_label = tk.Label(bottom, text="", font=(FONT, 12, "bold"),
                              wraplength=380, justify="left", bg=WHITE, fg=TEXT)
    feedback_label.pack(side="left", anchor="s")
 
    right_side = tk.Frame(bottom, bg=WHITE)
    right_side.pack(side="right")
    timer_label = tk.Label(right_side, text=f"Time left: {TIME_LIMIT}s",
                           font=(FONT, 16, "bold"), bg=WHITE, fg=GREEN_DARK)
    timer_label.pack(anchor="e", pady=(0, 8))
 
    button_row = tk.Frame(right_side, bg=WHITE)
    button_row.pack(anchor="e")
    submit_button = make_button(button_row, "Submit", submit_answer)
    submit_button.pack(side="left")
    next_text = "Next" if current_question < total - 1 else "Results"
    next_button = make_button(button_row, next_text, next_question,
                              color=GREEN_DARK)
    next_button.config(state="disabled")
    next_button.pack(side="left", padx=(8, 0))
 
    update_timer()
 
 

# TIMER

def update_timer():
    """Show the time left and call itself again after 1 second."""
    global time_left, timer_job
    if answered:
        return
    timer_label.config(text=f"Time left: {time_left}s",
                       fg=WRONG if time_left <= 5 else GREEN_DARK)
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)
 
 
def stop_timer():
    """Cancel the scheduled timer call, if there is one."""
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None
 
 

# ANSWER CHECKING

def lock_choices():
    """Disable the radio buttons after the question is finished."""
    for button in choice_buttons:
        button.config(state="disabled")
 
 
def reveal_answer(question, chosen):
    """Color the correct choice green and a wrong chosen choice red."""
    for button in choice_buttons:
        letter = button["value"]
        if letter == question["answer"]:
            button.config(bg=CORRECT, selectcolor=CORRECT,
                          disabledforeground=WHITE)
        elif letter == chosen:
            button.config(bg=WRONG, selectcolor=WRONG,
                          disabledforeground=WHITE)
 
 
def submit_answer():
    """Check the selected answer when Submit is clicked."""
    global score, answered
    if answered:                       # blocks multiple submissions
        return
 
    choice = selected_answer.get()
    if choice == "":                   # nothing selected: warn, timer keeps running
        messagebox.showwarning("No answer", "Please select an answer first.")
        return
 
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")
 
    question = quiz_questions[current_question]
    reveal_answer(question, choice)
 
    if choice == question["answer"]:   # this line checks the answer
        score += 1
        feedback_label.config(text="Correct! +1 point", fg=CORRECT)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"]),
        })
        feedback_label.config(text="Wrong answer", fg=WRONG)
 
    next_button.config(state="normal")
 
 
def time_up():
    """Called when the countdown reaches zero: count the question as wrong."""
    global answered
    if answered:
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")
 
    question = quiz_questions[current_question]
    reveal_answer(question, None)
    correct_text = get_choice_text(question, question["answer"])
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": correct_text,
    })
    feedback_label.config(text=f"Time is up! Answer: {correct_text}", fg=WRONG)
    next_button.config(state="normal")
 
 
def next_question():
    """Go to the next question, or to the results after the last one."""
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()
 
 

# RESULTS SCREEN

def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)
 
    if percentage >= 90:
        message = "Outstanding! You know your networking."
    elif percentage >= 70:
        message = "Great job! Your fundamentals are solid."
    elif percentage >= 50:
        message = "Not bad. A little more practice will help."
    else:
        message = "Review the topic and try again."
 
    name = player_name.get().strip() or "Player"
    make_header("Quiz Results", f"Well played, {name}")
 
    body = tk.Frame(main_frame, bg=WHITE)
    body.pack(fill="both", expand=True, padx=30, pady=18)
 
    # Buttons are packed first (at the bottom) so the review box cannot hide them
    button_row = tk.Frame(body, bg=WHITE)
    button_row.pack(side="bottom", pady=(12, 0))
    make_button(button_row, "Restart", start_quiz).pack(side="left", padx=8)
    make_button(button_row, "Exit", on_close, color=GREEN_DARK
                ).pack(side="left", padx=8)
 
    # Score, percentage and high score side by side
    stats = tk.Frame(body, bg=WHITE)
    stats.pack(fill="x")
    make_stat_box(stats, f"{score} / {total}", "Score").pack(
        side="left", expand=True, fill="x", padx=(0, 8))
    make_stat_box(stats, f"{percentage:.0f}%", "Percentage").pack(
        side="left", expand=True, fill="x", padx=8)
    make_stat_box(stats, f"{max(get_high_score(), score)} / {total}",
                  "High score").pack(side="left", expand=True, fill="x",
                                     padx=(8, 0))
 
    result_text = message + ("  New high score!" if new_record else "")
    tk.Label(body, text=result_text, font=(FONT, 13, "bold"), bg=WHITE,
             fg=GREEN_DARK).pack(pady=(14, 8))
 
    # Answer review: only the incorrect answers
    tk.Label(body, text="Answer Review", font=(FONT, 12, "bold"),
             bg=WHITE, fg=GREEN_DARK).pack(anchor="w")
    review_frame = tk.Frame(body, bg=GREEN_LIGHT)
    review_frame.pack(fill="both", expand=True, pady=(4, 0))
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, font=(FONT, 11), wrap="word",
                         bg=GREEN_LIGHT, fg=TEXT, relief="flat", padx=12,
                         pady=10, yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)
 
    if not wrong_answers:
        review_box.insert("end", "Perfect score! You answered every question correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")
    review_box.config(state="disabled")   # read-only
 

# CLOSING THE PROGRAM

def on_close():
    """Cancel the timer before closing so no errors appear after the window is gone."""
    stop_timer()
    root.destroy()
 
 
root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()
 