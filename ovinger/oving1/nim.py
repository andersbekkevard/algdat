import random


def main():
    matches = 32
    current_player = "user"  # User starts first

    print("Welcome to Nim!")
    print("Rules:")
    print("- There are 32 matches on the table")
    print("- You can pick 1-7 matches on your turn")
    print("- The player who picks the last match LOSES")
    print("- You start first!")
    print("-" * 40)

    while matches > 0:
        print(f"\nMatches remaining: {matches}")

        if current_player == "user":
            # User's turn
            while True:
                try:
                    user_pick = int(
                        input("How many matches do you want to pick (1-7)? ")
                    )
                    if 1 <= user_pick <= 7 and user_pick <= matches:
                        matches -= user_pick
                        print(f"You picked {user_pick} matches.")
                        break
                    elif user_pick > matches:
                        print(
                            f"You can't pick more matches than are available ({matches})!"
                        )
                    else:
                        print("Please pick between 1 and 7 matches!")
                except ValueError:
                    print("Please enter a valid number!")

            # Check if user lost
            if matches == 0:
                print("\nYou picked the last match! You lose!")
                print("Computer wins!")
                break
            print(matches, " matches left, mod 8 that becomes ", matches % 8)
            current_player = "computer"

        else:
            # Computer's turn
            # Computer uses random strategy
            max_pick = min(7, matches)
            computer_pick = random.randint(1, max_pick)
            matches -= computer_pick
            print(f"Computer picked {computer_pick} matches.")

            # Check if computer lost
            if matches == 0:
                print("\nComputer picked the last match! Computer loses!")
                print("You win!")
                break

            current_player = "user"


if __name__ == "__main__":
    # main()
    print((8) % 8)
