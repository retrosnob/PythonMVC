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