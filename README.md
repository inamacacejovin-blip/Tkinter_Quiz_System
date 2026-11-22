# NetBasics Quiz

**Name:** Ace Jovin I. Inamac
**Section:** SE - 3A
**Topic:** Networking Fundamentals

## Features Completed

- 10 multiple-choice questions (four choices each, one correct answer)
- Random question order every time the quiz starts or restarts
- 15-second countdown timer that is visible on screen
- Answer checking and time-out handling
- No double submission, and the timer stops when an answer is submitted
- Score tracking (1 point per correct answer)
- Progress indicator ("Question X of 10" and a progress bar)
- Results screen with score, percentage, and a performance message
- Answer review that lists only the wrong answers with the correct ones
- High score saved in a text file
- Restart button
- Own design: white and green theme, green header bar, optional player name, colored answer feedback

## How the Questions Are Stored and Shuffled

Each question is a Python dictionary with three keys: `"question"` , `"choices"`, and `"answer"` . All ten dictionaries are placed inside one list called `QUESTIONS`.

When the player starts or restarts, `start_quiz()` calls `random.sample(QUESTIONS, len(QUESTIONS))`. This makes a new list with the same questions in a random order, so the original `QUESTIONS` list is never changed. The program then uses that shuffled list, called `quiz_questions`. The question number shown on screen comes from `current_question + 1`, so the numbers stay correct even when the order changes.

## How the Timer Works

The timer uses Tkinter's `root.after(1000, update_timer)`, which calls a function again after one second without freezing the window. `update_timer()` shows the time left, and if it is not zero yet, it subtracts 1 and schedules itself again. The countdown starts at 15 because `show_question()` resets `time_left` to `TIME_LIMIT`. The label turns red when 5 seconds or less are left.

When the player clicks Submit, `submit_answer()` sets `answered = True` and calls `stop_timer()`. That function uses `root.after_cancel()` with the saved `timer_job` id to cancel the next scheduled call. `update_timer()` also returns right away if `answered` is already `True`. If the time reaches 0 first, `time_up()` runs instead, which marks the question wrong and shows the correct answer.

## How the Program Identifies the Correct Answer

Every radio button has the choice's letter as its value ("A", "B", "C", or "D"), and all four share one variable, `selected_answer`. When Submit is clicked, the program reads the chosen letter with `selected_answer.get()` and compares it to the `"answer"` letter stored in the current question:

```python
if choice == question["answer"]:
```

If they match, the player gets a point. If they do not, the question, the player's answer, and the correct answer are saved in the `wrong_answers` list. If no choice is selected, a warning appears and nothing is marked, so the timer keeps running. Because `answered` becomes `True` after the first submit, clicking Submit again does nothing.

## How the Score and High Score Work

The `score` variable starts at 0 and goes up by 1 for each correct answer. On the results screen, the percentage is calculated with `(score / total) * 100`, where `total` is the number of questions. A message is picked with `if / elif / else`: 90% and above is the best message, 70% and above is good, 50% and above is "keep practicing", and anything lower tells the player to review the topic.

The high score is stored in `high_score.txt`, next to the program file (the path is built with `os.path.dirname(os.path.abspath(__file__))`). `get_high_score()` opens the file and reads the number, and it returns 0 if the file does not exist or has invalid text. `save_high_score()` is called on the results screen. It writes the new score to the file only if it is higher than the saved one, and it returns `True` so the screen can show "New high score!". Since the number is in a file, it is still there when the program is closed and opened again.

## Function Explanations

| Function | Purpose | Called when |
|----------|---------|-------------|
| `get_high_score()` | Reads the saved high score from the text file (0 if missing or invalid) | The start screen and results screen are shown |
| `save_high_score()` | Writes the score to the file only if it is higher than the old one | The results screen is shown |
| `clear_screen()` | Removes every widget from the main frame so a new screen can be built | Before each screen is drawn |
| `get_choice_text()` | Turns an answer letter into the full choice text, like "C. Router" | A wrong answer or time-out is recorded |
| `make_button()` | Creates a button with the same green style | Any screen needs a button |
| `make_header()` | Builds the green title bar at the top of a screen | The start and results screens are drawn |
| `make_stat_box()` | Builds a small light-green box with a value and caption | The start and results screens are drawn |
| `show_start_screen()` | Shows the title, quiz info, high score, name entry, and Start button | The program opens |
| `start_quiz()` | Resets the variables and shuffles the questions | Start or Restart is clicked |
| `show_question()` | Builds the question screen and starts the timer | A new question is displayed |
| `update_timer()` | Shows the time left and counts down every second | A question is displayed, then once per second |
| `stop_timer()` | Cancels the scheduled timer call | An answer is submitted, time is up, or the quiz restarts or closes |
| `lock_choices()` | Disables the radio buttons after a question is finished | An answer is submitted or time is up |
| `reveal_answer()` | Colors the correct choice green and a wrong choice red | An answer is submitted or time is up |
| `submit_answer()` | Checks the answer, updates the score, and blocks double submission | Submit is clicked |
| `time_up()` | Marks the question wrong when the timer reaches 0 | The countdown reaches zero |
| `next_question()` | Moves to the next question or to the results | Next (or Results) is clicked |
| `show_results()` | Shows the score, percentage, message, high score, and answer review | After question 10 |
| `on_close()` | Stops the timer and closes the window | The window is closed or Exit is clicked |

## Screenshots

uploaded in the repository

## Challenges I Faced

- Making the timer stop. At first the countdown kept running after I submitted an answer. I fixed it by saving the id from `root.after()` in `timer_job` and cancelling it with `root.after_cancel()` inside `stop_timer()`.
- Stopping double submission. Clicking Submit twice could add the point twice. I added the `answered` variable and a check at the start of `submit_answer()` that returns right away if it is already `True`.
- Old answers staying selected. A radio button from the last question stayed selected on the next one. Calling `selected_answer.set("")` at the start of `show_question()` solved it.
- Buttons hidden on the results screen. The review box pushed the Restart and Exit buttons out of view, so I packed the buttons first at the bottom of the frame.
