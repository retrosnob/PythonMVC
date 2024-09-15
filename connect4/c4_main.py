# c4main.py

import c4_model
import c4_view
import c4_controller

if __name__ == "__main__":
    # Note that the model has no reference to the View or Controller.
    # But the View needs to have a reference to the Model.
    # And the Controller has references to both the Model and the View.
    model = c4_model.C4_Model()
    view = c4_view.C4_View(model)
    controller = c4_controller.C4_Controller(model, view)
    view.draw()

    while controller.running:
        controller.process_input()