import random

board = [" " for _ in range(9)]

def print_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

def check_winner(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_draw():
    return " " not in board

def player_move():
    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Invalid move. Try again.")
        except:
            print("Enter a number between 1 and 9.")

def find_winning_move(player):
    for i in range(9):
        if board[i] == " ":
            board[i] = player
            if check_winner(player):
                board[i] = " "
                return i
            board[i] = " "
    return None

def ai_move():
    move = find_winning_move("O")
    if move is not None:
        board[move] = "O"
        print(f"AI wins by choosing {move+1}")
        return
    move = find_winning_move("X")
    if move is not None:
        board[move] = "O"
        print(f"AI blocks at {move+1}")
        return
    available = [i for i in range(9) if board[i] == " "]
    move = random.choice(available)
    board[move] = "O"
    print(f"AI chose position {move+1}")

while True:
    print_board()
    player_move()
    if check_winner("X"):
        print_board()
        print("You win!")
        break
    if is_draw():
        print_board()
        print("It's a draw!")
        break
    ai_move()
    if check_winner("O"):
        print_board()
        print("AI wins!")
        break
    if is_draw():
        print_board()
        print("It's a draw!")
        break