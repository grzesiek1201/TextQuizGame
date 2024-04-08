import unittest
from unittest.mock import patch
from io import StringIO
from TextQuizGame import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_correct_player_answer(self):
        self.game.current_question = {"correct": "a"}
        self.game.correct_player_answer()
        self.assertEqual(self.game.correct_answer, "a")

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_current_question(self, mock_stdout):
        self.game.current_question = {"question": "What is 2 + 2?", "answers": {"a": "4", "b": "3", "c": "2", "d": "5"}}
        expected_output = "Question 1: What is 2 + 2?\n" \
                          "a: 4\n" \
                          "b: 3\n" \
                          "c: 2\n" \
                          "d: 5\n"
        self.game.print_current_question()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_load_game_with_save(self, mock_input):
        self.game.data_manager.load_game_state = lambda name: {"points": 10, "currentQuestion": 5, "currentHelp": 2}
        self.game.data_manager.get_player_data = lambda name: {"name": "John", "points": 10}
        self.game.data_manager.leaderboard = lambda: None
        self.game.data_manager.update_player = lambda name, points: None
        self.game.load_game()
        self.assertEqual(self.game.points, 10)
        self.assertEqual(self.game.questions_count, 5)
        self.assertEqual(self.game.player_help_count, 2)

    @patch('builtins.input', side_effect=["no"])
    def test_load_game_without_save(self, mock_input):
        self.game.load_game()
        self.assertEqual(self.game.points, 0)
        self.assertEqual(self.game.questions_count, 0)
        self.assertEqual(self.game.player_help_count, 10)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=["John"])
    def test_lose_game(self, mock_input, mock_stdout):
        self.game.data_manager.get_player_data = lambda name: None
        self.game.data_manager.add_player = lambda name, points: None
        self.game.data_manager.leaderboard = lambda: None
        self.game.data_manager.update_player = lambda name, points: None
        self.game.lose_game()
        self.assertIn("Game over! You scored 0 points.", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
