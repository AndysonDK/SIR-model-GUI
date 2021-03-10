#!/usr/bin/env python3

# I've taken a lot of code from this URL as a starting example for how to use 
# tkinter with matplotlib:
# https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from eulers_method import _configure_plot


root = Tk()
root.title("SIR modelling")

# These initial values have the purpose to show the user an example
population=10000
infected=1
recovered=0
alpha=0.0002
gamma=0.3
days=50
step=0.5

# Define the figure to contain the SIR-model data
canvas = FigureCanvasTkAgg(_configure_plot(population,
                                           infected,
                                           recovered,
                                           alpha,
                                           gamma,
                                           days,
                                           step),
                           root
                           )

canvas.draw()
canvas.get_tk_widget().grid(row=0, column=1, rowspan=2)

# Define a graph_frame for the matplotlib toolbar
graph_frame = Frame(root)

# Define the toolbar beneath the figure
toolbar = NavigationToolbar2Tk(canvas, graph_frame)
toolbar.update()

# Display the graph_frame which contains the matplotlib toolbar
graph_frame.grid(row=2, column=1)

# Connect tkinter user input with matplotlib, to make the graph interactable
canvas.mpl_connect("key_press_event", lambda event: key_press_handler(event, canvas, toolbar))


# Define the frames that are going to contain the modelling configurations and buttons
SIR_model_frame = LabelFrame(root, text="SIR-model configurations", pady=7)
eulers_method_frame = LabelFrame(root, text="Eulers method configurations", pady=7)
button_frame = Frame(root)

# Define the population field 
population_label = Label(SIR_model_frame, text="N:")
population_field = Entry(SIR_model_frame, width=15)
population_field.insert(0, population)

# Display the population field
population_label.grid(row=0, column=0, padx=(10, 0))
population_field.grid(row=0, column=1, padx=(0, 10))

# Define the initial infected field 
infected_label = Label(SIR_model_frame, text="I(0):")
infected_field = Entry(SIR_model_frame, width=15)
infected_field.insert(0, infected)

# Display the initial infected field 
infected_label.grid(row=1, column=0, padx=(10, 0))
infected_field.grid(row=1, column=1, padx=(0, 10))

# Define the initial recovered field 
recoverd_label = Label(SIR_model_frame, text="R(0):")
recovered_field = Entry(SIR_model_frame, width=15)
recovered_field.insert(0, recovered)

# Display the initial recovered field
recoverd_label.grid(row=2, column=0, padx=(10, 0))
recovered_field.grid(row=2, column=1, padx=(0, 10))

# Define the alpha field 
alpha_label = Label(SIR_model_frame, text="α:")
alpha_field = Entry(SIR_model_frame, width=15)
alpha_field.insert(0, alpha)

# Display the alpha field
alpha_label.grid(row=3, column=0, padx=(10, 0))
alpha_field.grid(row=3, column=1, padx=(0, 10))

# Define the gamma field 
gamma_label = Label(SIR_model_frame, text="γ:")
gamma_field = Entry(SIR_model_frame, width=15)
gamma_field.insert(0, gamma)

# Display the gamma field
gamma_label.grid(row=4, column=0, padx=(10, 0))
gamma_field.grid(row=4, column=1, padx=(0, 10))

# Define the days/number of iterations field for eulers method
days_label = Label(eulers_method_frame, text="t:")
days_field = Entry(eulers_method_frame, width=15)
days_field.insert(0, days)

# Display the days/number of iterations field
days_label.grid(row=0, column=0, padx=(10, 0))
days_field.grid(row=0, column=1, padx=(0, 10))

# Define the length of the step field for eulers method
step_label = Label(eulers_method_frame, text="h:")
step_field = Entry(eulers_method_frame, width=15)
step_field.insert(0, step)

# Display the length of the step field
step_label.grid(row=1, column=0, padx=(10, 0))
step_field.grid(row=1, column=1, padx=(0, 10))


def submit():
    # You can submit scientific notation values to alpha, gamma, days and step
    # input fields, since those fields have their values transformed by float().
    # See this for reference: 
    # https://stackoverflow.com/questions/23636509/python-convert-string-in-scientific-notation-to-float
    try:
        population_value = int(population_field.get())
        infected_value = int(infected_field.get())
        recovered_value = int(recovered_field.get())
        alpha_value = float(alpha_field.get())
        gamma_value = float(gamma_field.get())
        days_value = float(days_field.get())
        step_value = float(step_field.get())

        # Right now we are making a new figure everytime we submit new values.
        # Don't know if this should be different, like just changing one 
        # global figure variable. Maybe this: 
        # https://stackoverflow.com/questions/12124350/how-to-update-the-contents-of-a-figurecanvastkagg
        fig = _configure_plot(population=population_value,
                             infected=infected_value,
                             recovered=recovered_value,
                             alpha=alpha_value,
                             gamma=gamma_value,
                             days=days_value,
                             step=step_value
                             )

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=2)
    except ValueError:
        print("The input values MUST be either floats or ints!")


def quit():
    # stops mainloop
    root.quit()
    # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    root.destroy()


# Define the submit button
button = Button(button_frame, text="Submit", command=submit)
button.grid(row=0, column=0)

# Define the quit button
button = Button(button_frame, text="Quit", command=quit)
button.grid(row=0, column=1)

# Display the frames that are going to contain the modelling configurations
SIR_model_frame.grid(row=0, column=0, padx=10)
eulers_method_frame.grid(row=1, column=0, padx=10)
button_frame.grid(row=2, column=0)


if __name__ == '__main__':
    root.mainloop()

