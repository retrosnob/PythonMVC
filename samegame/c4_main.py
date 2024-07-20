# c4main.py

import c4_model

if __name__ == '__main__':
    model = c4_model.C4_Model()
    while not model.getstatus()["GAME OVER"]:
        column = input('Enter column: ')
        model.makemove(int(column))
        model.print()
    winner = model.getstatus()["WINNER"]
    if winner:
        print("Winner: Player {}".format(winner))
    else:
        print("Draw")