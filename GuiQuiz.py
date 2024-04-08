import tkinter as tk
from tkinter import messagebox
import random
import Questions
from QuizTimers import Timers
from DataGame import Data


class QuizGUI:
    def __init__(self, master):
        self.data_manager = Data()
        self.points = 0
        self.questions_count = 0
        self.player_help_count = 10
        self.help_extra_points = 0
        self.correct_answer = None
        self.current_question = None
        self.shuffled_questions = self.questions_shuffle()
        self.help_used = False
        self.timers = Timers()
        self.master = master
        self.master.title("Gui Quiz Game")
        self.master.geometry("800x600")
        self.selected_answer = None

        self.create_welcome_gui()
        self.game_gui()
        self.help_gui()
        self.answer_gui()
        self.after_game_gui()
        self.timer_running = False

    def create_welcome_gui(self):
        self.label = tk.Label(self.master, text="Welcome! Tell us your name!", font=("Helvetica", 12))
        self.label.pack(pady=150, anchor=tk.CENTER, expand=True)

        self.name_label = tk.Label(self.master, text="Enter your name:", font=("Helvetica", 12))
        self.name_label.pack()

        self.name_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.name_entry.pack()

        self.name_button = tk.Button(self.master, text="Start game", font=("Helvetica", 12), command=self.welcome_game)
        self.name_button.pack()

    def game_gui(self):
        self.start_button = tk.Button(self.master, text=" BEGIN", font=("Helvetica", 12), command=self.start_game)

        self.load_player_label = tk.Label(self.master,text="Would you like to load your last saved game?", font=("Helvetica", 12))
        self.yes_load_button = tk.Button(self.master, text="YES")
        self.no_load_button = tk.Button(self.master, text="NO")

    def timer_gui(self):
        self.timer_label = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.timer_label.place(relx=0.9, rely=0.05, anchor=tk.CENTER)

    def help_gui(self):
        self.help_button = tk.Button(self.master, text="Help", font=("Helvetica", 12), command=self.show_help_buttons)
        self.next_button = tk.Button(self.master, text="next", font=("Helvetica", 12), command=self.help_next)
        self.half_button = tk.Button(self.master, text="half", font=("Helvetica", 12), command=self.help_half)
        self.time_button = tk.Button(self.master, text="time", font=("Helvetica", 12), command=self.help_time)
        self.save_button = tk.Button(self.master, text="save game", font=("Helvetica", 12))

    def answer_gui(self):
        self.answer_a_button = tk.Button(self.master, text="A", font=("Helvetica", 12), command=lambda: self.select_answer("A"))
        self.answer_b_button = tk.Button(self.master, text="B", font=("Helvetica", 12), command=lambda: self.select_answer("B"))
        self.answer_c_button = tk.Button(self.master, text="C", font=("Helvetica", 12), command=lambda: self.select_answer("C"))
        self.answer_d_button = tk.Button(self.master, text="D", font=("Helvetica", 12), command=lambda: self.select_answer("D"))

    def after_game_gui(self):
        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.exit_button = tk.Button(self.master, text="Exit", command=exit)

    def help_points_gui(self):
        self.help_points_label = tk.Label(self.master,text=f"Help points:{self.player_help_count} ")

    def game_points_gui(self):
        self.game_points_label= tk.Label(self.master, text=f"Score: {self.points}")

    def start_timer(self):
        self.timer_running = True
        self.master.after(30000, self.timer_finished)

    def timer_finished(self):
        self.timer_running = False
        print("Timer finished!")

    def show_load_game(self):
        self.load_player_label.pack()

    def restart_game(self):
        self.data_manager.reset_player_data(self.name_input)

    def select_answer(self, answer):
        self.selected_answer = answer

    def show_question(self, question):
        self.label.config(text=question, anchor=tk.CENTER, font=("Helvetica", 12))

        self.answer_a_button.pack()
        self.answer_b_button.pack()
        self.answer_c_button.pack()
        self.answer_d_button.pack()

    def show_help_buttons(self):
        self.label.pack_forget()
        self.start_button.pack_forget()
        self.help_button.pack_forget()
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)
        self.half_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)
        self.time_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SE)

    def hide_help_buttons(self):
        self.next_button.pack_forget()
        self.time_button.pack_forget()
        self.half_button.pack_forget()

    def help_next(self):
        self.help_next()
        self.hide_help_buttons()

    def help_half(self):
        self.help_half()
        self.hide_help_buttons()

    def help_time(self):
        self.help_time()
        self.hide_help_buttons()

    def welcome_game(self):
        self.name_input = self.name_entry.get().strip()
        if self.name_input:
            self.label.config(text=f"Welcome {self.name_input} to TextQuizGame! version 1.5\n"
                                   "You will have to answer 20 questions.\n"
                                   "Of course, if you have trouble, you can ask for help by using the HELP button.\n"
                                   "You have a few options to choose for help, each using a different amount of points:\n"
                                   "next: 4 points\n"
                                   "time: 2 points\n"
                                   "half: 1 point\n"
                                   "or\n"
                                   "save: to save the game\n"
                                   f"Your total points: ", font=("Helvetica", 12))
            self.name_entry.delete(0, tk.END)
            self.name_label.pack_forget()
            self.name_entry.pack_forget()
            self.name_button.pack_forget()
            self.start_button.pack()
        else:
            tk.messagebox.showerror("Error", "Please enter your name.")

    def start_game(self):
        self.start_button.pack_forget()
        self.show_question(self.shuffled_questions[self.questions_count])

    def print_current_question(self, question):
        self.label.config(text=question["question"])

        self.answers_frame = tk.Frame(self.master)
        self.answers_frame.pack()

        self.selected_answer = tk.StringVar()  

        for option, answer in question['answers'].items():
            answer_button = tk.Radiobutton(self.answers_frame, text=answer, font=("Helvetica", 12),
                                           variable=self.selected_answer, value=option)
            answer_button.grid(row=0, padx=5, pady=5)

        submit_button = tk.Button(self.master, text="Submit", font=("Helvetica", 12), command=self.submit_answer)
        submit_button.pack(pady=10)

    def questions_shuffle(self):
        shuffled_questions = list(Questions.questions.values())
        random.shuffle(shuffled_questions)
        return shuffled_questions

    def correct_player_answer(self):
        self.correct_answer = self.current_question["correct"]

    def half_answers(self):
        question = self.shuffled_questions[self.questions_count]
        correct_option = question["correct"]
        wrong_options = [option for option in question["answers"] if option != correct_option]
        random.shuffle(wrong_options)
        wrong_option = wrong_options[0]
        remaining_options = {option: answer for option, answer in question["answers"].items()
                             if option == correct_option or option == wrong_option}
        question_text = self.current_question["question"]
        print(f"Question {self.questions_count + 1}: {question_text}")
        for option, answer in remaining_options.items():
            print(f"{option}: {answer}")

    def next_question(self):
        if self.questions_count < len(self.shuffled_questions):
            self.current_question = self.shuffled_questions[self.questions_count]
            self.correct_player_answer()
        else:
            self.win_game()

    def win_game(self):
        print("Congratulations! You won!")
        self.extra_points()
        print(f"You scored {self.points} points.")
        if self.points >= 40:
            print("You have incredible knowledge about programming!")
        elif self.points >= 30:
            print("Very Good.")
        elif self.points >= 20:
            print("Not bad.")
        elif self.points >= 10:
            print("Keep learning and improving.")

        player_data = self.data_manager.get_player_data(self.name_input)
        if player_data is not None:
            self.data_manager.update_player(self.name_input, self.points)
        else:
            self.data_manager.add_player(self.name_input, self.points)
        self.data_manager.load_players_data()
        self.data_manager.leaderboard()

    def extra_points(self):
        self.help_extra_points = self.player_help_count * 2
        self.points = self.help_extra_points + self.points
        print(f"You gain extra points for every NOT used help points. Your extra points {self.help_extra_points}")


def main():
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
