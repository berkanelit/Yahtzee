import tkinter as tk
from tkinter import messagebox
import random

class YahtzeeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Yahtzee Game")

        self.dice_values = [0, 0, 0, 0, 0]
        self.selected_dice = [False, False, False, False, False]

        self.roll_button = tk.Button(master, text="Roll Dice", command=self.roll_dice)
        self.roll_button.grid(row=0, column=0, pady=10)

        self.dice_labels = [tk.Label(master, text="", font=("Helvetica", 16)) for _ in range(5)]
        for i, label in enumerate(self.dice_labels):
            label.grid(row=1, column=i, padx=5)
        
        self.keep_label = tk.Label(master, text="Select dice to keep (0-4, comma-separated):", font=("Helvetica", 12))
        self.keep_label.grid(row=2, column=0, pady=5)

        self.keep_entry = tk.Entry(master, font=("Helvetica", 12))
        self.keep_entry.grid(row=2, column=1, pady=5)

        self.category_label = tk.Label(master, text="Choose a category (1-13):", font=("Helvetica", 12))
        self.category_label.grid(row=3, column=0, pady=5)

        self.category_entry = tk.Entry(master, font=("Helvetica", 12))
        self.category_entry.grid(row=3, column=1, pady=5)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_turn)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.total_score_label = tk.Label(master, text="Total Score: 0", font=("Helvetica", 14))
        self.total_score_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.total_score = 0
        self.turn = 1
        self.categories = [
            "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "ThreeOfAKind", "FourOfAKind", "FullHouse", "SmallStraight",
            "LargeStraight", "Yahtzee", "Chance"
        ]

        self.roll_dice()

    def roll_dice(self):
        for i in range(5):
            if not self.selected_dice[i]:
                self.dice_values[i] = random.randint(1, 6)
        self.update_dice_labels()

    def update_dice_labels(self):
        for i, label in enumerate(self.dice_labels):
            label.config(text=f"{self.dice_values[i]}")

    def reroll_dice(self):
        reroll_indices = [int(i) for i in self.keep_entry.get().split(",")]
        for index in reroll_indices:
            self.dice_values[index] = random.randint(1, 6)
        self.update_dice_labels()

    def submit_turn(self):
        self.reroll_dice()

        selected_category_index = int(self.category_entry.get()) - 1
        if 0 <= selected_category_index < len(self.categories):
            selected_category = self.categories[selected_category_index]
            category_score = self.calculate_score(selected_category)
            self.total_score += category_score
            messagebox.showinfo("Turn Result", f"You scored {category_score} points for {selected_category}. Total score: {self.total_score}")

            self.turn += 1
            if self.turn > 13:
                messagebox.showinfo("Game Over", f"Game over. Your final score is {self.total_score}.")
                self.master.destroy()
            else:
                self.roll_dice()
        else:
            messagebox.showwarning("Invalid Category", "Invalid category selected. Please choose a category between 1 and 13.")

        self.total_score_label.config(text=f"Total Score: {self.total_score}")

    def calculate_score(self, category):
        def calculate_score(dice, category):
            if category == "Ones":
                return sum([die for die in dice if die == 1])
            elif category == "Twos":
                return sum([die for die in dice if die == 2])
            elif category == "Threes":
                return sum([die for die in dice if die == 3])
            elif category == "Fours":
                return sum([die for die in dice if die == 4])
            elif category == "Fives":
                return sum([die for die in dice if die == 5])
            elif category == "Sixes":
                return sum([die for die in dice if die == 6])
            elif category == "ThreeOfAKind":
                if any(dice.count(die) >= 3 for die in dice):
                    return sum(dice)
                else:
                    return 0
            elif category == "FourOfAKind":
                if any(dice.count(die) >= 4 for die in dice):
                    return sum(dice)
                else:
                    return 0
            elif category == "FullHouse":
                if any(dice.count(die) == 3 for die in dice) and any(dice.count(die) == 2 for die in dice):
                    return 25
                else:
                    return 0
            elif category == "SmallStraight":
                if {1, 2, 3, 4}.issubset(set(dice)) or {2, 3, 4, 5}.issubset(set(dice)) or {3, 4, 5, 6}.issubset(set(dice)):
                    return 30
                else:
                    return 0
            elif category == "LargeStraight":
                if {1, 2, 3, 4, 5}.issubset(set(dice)) or {2, 3, 4, 5, 6}.issubset(set(dice)):
                    return 40
                else:
                    return 0
            elif category == "Yahtzee":
                if any(dice.count(die) == 5 for die in dice):
                    return 50
                else:
                    return 0
            elif category == "Chance":
                return sum(dice)
            else:
                return 0

        return calculate_score(self.dice_values, category)

if __name__ == "__main__":
        root = tk.Tk()
        app = YahtzeeGame(root)
        root.mainloop()
