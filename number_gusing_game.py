import random
import os
import json

class NumberGuessingGame:
    def __init__(self, lower_bound=1, upper_bound=100, max_attempts=10):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_attempts = max_attempts
        self.secret_number = random.randint(self.lower_bound, self.upper_bound)
        self.guesses = 0
        self.is_game_over = False
        self.score = 0
        self.high_scores = self.load_high_scores()

    def reset_game(self):
        """Resets the game with a new secret number and score."""
        self.secret_number = random.randint(self.lower_bound, self.upper_bound)
        self.guesses = 0
        self.is_game_over = False
        print("Game has been reset. A new number has been generated!")

    def make_guess(self, guess):
        """Processes the player's guess."""
        self.guesses += 1
        if guess < self.lower_bound or guess > self.upper_bound:
            return "Your guess is out of bounds!"
        if self.guesses > self.max_attempts:
            self.is_game_over = True
            return f"Game over! You've exceeded the maximum number of attempts. The correct number was {self.secret_number}."
        if guess < self.secret_number:
            return "Too low!"
        elif guess > self.secret_number:
            return "Too high!"
        else:
            self.is_game_over = True
            self.score = max(0, 100 - (self.guesses - 1) * 10)  # Score calculation
            self.update_high_scores(self.score)  # Update high scores
            return (f"Congratulations! You've guessed the number {self.secret_number} in {self.guesses} tries. "
                    f"Your score is {self.score}.")

    def get_hint(self):
        """Gives the player a hint about the secret number."""
        if self.is_game_over:
            return "Game is already over. Please reset to play again."
        hint_range = 10
        hint = random.randint(max(self.lower_bound, self.secret_number - hint_range), 
                              min(self.upper_bound, self.secret_number + hint_range))
        return f"Here's a hint: The secret number is around {hint}."

    def load_high_scores(self):
        """Loads the high scores from a file."""
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as file:
                data = json.load(file)
                return data.get("high_scores", [])
        return []

    def save_high_scores(self):
        """Saves the high scores to a file."""
        with open("high_scores.json", "w") as file:
            json.dump({"high_scores": self.high_scores}, file)

    def update_high_scores(self, score):
        """Updates the list of high scores."""
        self.high_scores.append(score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:3]  # Keep top 3 scores
        self.save_high_scores()

    def display_high_scores(self):
        """Displays the top three high scores."""
        print("\nTop Three High Scores:")
        for index, score in enumerate(self.high_scores, start=1):
            print(f"{index}. {score}")


def main():
    print("Welcome to the Number Guessing Game!")
    game = NumberGuessingGame()

    while not game.is_game_over:
        try:
            guess = int(input(f"Guess a number between {game.lower_bound} and {game.upper_bound} (Max attempts: {game.max_attempts}): "))
            result = game.make_guess(guess)
            print(result)

            if not game.is_game_over:
                if input("Do you want a hint? (yes/no): ").lower() == 'yes':
                    print(game.get_hint())
        except ValueError:
            print("Please enter a valid integer.")

    game.display_high_scores()  # Display high scores after the game ends

    if input("Do you want to play again? (yes/no): ").lower() == 'yes':
        game.reset_game()
        main()

if __name__ == "__main__":
    main()