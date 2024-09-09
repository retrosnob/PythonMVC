# c4main.py

import c4_model

import c4_model
import c4_view
import c4_controller

if __name__ == "__main__":
    model = c4_model.C4_Model()
    view = c4_view.C4_View(model)
    controller = c4_controller.C4_Controller(model, view)
    view.redraw()
    view.blit()

    while controller.running:
        controller.process_input()



    # model = c4_model.C4_Model()
    # while not model.getstatus()["GAME OVER"]:
    #     column = input('Enter column: ')
    #     model.makemove(int(column))
    #     model.print()
    # winner = model.getstatus()["WINNER"]
    # if winner:
    #     print("Winner: Player {}".format(winner))
    # else:
    #     print("Draw")