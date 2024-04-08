import random
import Questions
from QuizTimers import Timers
from DataGame import Data


class Game:
    def __init__(self):
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

    def welcome_message(self):
        if not hasattr(self, 'name_input'):
            while True:
                self.name_input = input("Hello! Tell us your name:")
                if self.name_input.strip():
                    break
                else:
                    print("Please enter a valid name.")
        message = (
            f"Welcome {self.name_input} in TextQuizGame! version 1.4\n"
            "You will have to answer 20 questions.\n"
            "Of course, if you will have a trouble, you can ask for help by typing HELP.\n"
            "You have few options to choose for help, they are using different amount of points, which are:\n"
            "next: 4 points\n"
            "time: 2 points\n"
            "half: 1 point\n"
            "or\n"
            "save: to save the game\n"
            f"Your total points: {self.player_help_count} \n"
        )
        print(message)
        input("Press ENTER to start the game...")

    def load_game(self):
        self.save_input = input("Would you like to load your last saved game? (YES/NO): ")
        if self.save_input.lower() == "yes":
            self.name_input = input("Enter your name: ")
            game_state = self.data_manager.load_game_state(self.name_input)
            if game_state is not None:
                self.points = game_state["points"]
                self.questions_count = game_state["currentQuestion"]
                self.player_help_count = game_state["currentHelp"]
                print("Game loaded successfully.")
            else:
                print("No saved game state found for this player.")
        elif self.save_input.lower() == "no":
            pass

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

    def print_current_question(self):
        question_text = self.current_question["question"]
        print(f"Question {self.questions_count + 1}: {question_text}")
        for option, answer in self.current_question['answers'].items():
            print(f"{option}: {answer}")

    def next_question(self):
        if self.questions_count < len(self.shuffled_questions):
            self.current_question = self.shuffled_questions[self.questions_count]
            self.correct_player_answer()
        else:
            self.win_game()

    def lose_game(self):
        player_data = self.data_manager.get_player_data(self.name_input)
        if player_data is not None:
            self.data_manager.update_player(self.name_input, self.points)
        else:
            self.data_manager.add_player(self.name_input, self.points)

        print(f"Game over! You scored {self.points} points.")
        self.data_manager.load_players_data()
        self.data_manager.leaderboard()
        while True:
            restart_input = input('Type "restart" to try again, or "exit" to quit: ')
            if restart_input.lower() == "restart":
                self.data_manager.reset_player_data(self.name_input)
                self.run_game()
                break
            elif restart_input.lower() == "exit":
                exit()
            else:
                print("Invalid input. Please type 'restart' to try again or 'exit' to quit.")

    def extra_points(self):
        self.help_extra_points = self.player_help_count * 2
        self.points = self.help_extra_points + self.points
        print(f"You gain extra points for every NOT used help points. Your extra points {self.help_extra_points}")

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

    def help_next(self):
        if self.player_help_count < 4:
            print(f"You have run out of help points. Current help points: {self.player_help_count}")
        else:
            self.player_help_count -= 4
            self.questions_count += 1
            print(f"Let's move to another question. Current help points: {self.player_help_count}")

    def help_half(self):
        if self.player_help_count < 1:
            print(f"You have run out of help points. Current help points: {self.player_help_count}")
        else:
            self.player_help_count -= 1
            self.half_answers()
            self.help_used = True
            print(f"Two options left. Current help points: {self.player_help_count} ")

    def help_time(self):
        if self.player_help_count < 2:
            print(f"You have run out of help points. Current help points: {self.player_help_count}")
        else:
            self.player_help_count -= 2
            self.help_used = True
            self.timers.help_add_time()
            print(f"You have 30 seconds more to answer. Current help points: {self.player_help_count}")

    def player_answer(self):
        self.current_question = self.shuffled_questions[self.questions_count]
        self.correct_player_answer()
        if self.help_used == True:
            self.player_input = input("Which answer is correct?: ")
        else:
            self.print_current_question()
            self.player_input = input("Which answer is correct?: ")
            self.help_used = False

    def player_choice(self, player_input):
        while self.questions_count < 20:
            self.timers.start_time()
            self.player_answer()

            if self.player_input.lower() in ["a", "b", "c", "d"]:
                if self.player_input == self.correct_answer:
                    if self.timers.player_time > 20:
                        self.points += 2
                        self.questions_count += 1
                        print("Correct! Good Job! You earned 2 point.")
                        print(f"Current points: {self.points}")
                        self.next_question()
                    else:
                        self.points += 1
                        self.questions_count += 1
                        print("Correct! Good Job! You earned 1 point.")
                        print(f"Current points: {self.points}")
                        self.next_question()
                    self.timers.reset_question_timer()
                elif self.timers.player_time == 0:
                    print("Time is up. You lose.")
                    self.lose_game()
                else:
                    print(f"Incorrect answer. The correct answer was {self.correct_answer}.")
                    self.lose_game()
                    self.timers.reset_question_timer()

            elif self.player_input.lower() == "help":
                self.timers.help_pause_time()
                self.input_help = input("Choose what kind of help would you like to use? (next/half/time/save): ")
                if self.input_help.lower() == "next":
                    self.help_next()
                    self.timers.help_resume_time()
                elif self.input_help.lower() == "half":
                    self.help_half()
                    self.timers.help_resume_time()
                elif self.input_help.lower() == "time":
                    self.help_time()
                    self.timers.help_resume_time()
                elif self.input_help.lower() == "save":
                    self.data_manager.update_player(
                        self.name_input,
                        self.points,
                        current_question=self.questions_count,
                        current_help=self.player_help_count
                    )
                    self.data_manager.save_game_state(self.name_input, self.points, self.questions_count, self.player_help_count)
                    print("Game state saved. Game closing...")
                    exit()
            else:
                print("Invalid input. Please enter a, b, c, d, or help.")
        if self.questions_count == 20:
            self.win_game()

    def run_game(self):
        self.timers.reset_timer()
        self.points = 0
        self.questions_count = 0
        self.player_help_count = 10
        self.correct_answer = None
        self.current_question = None
        self.help_used = False
        self.load_game()
        self.welcome_message()
        self.player_choice("")
