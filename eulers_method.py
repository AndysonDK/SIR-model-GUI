# I've taken some code from this URL as a starting example for how to make 
# matplotlib plot SIR-model data:
# https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/

import sys
from matplotlib.figure import Figure
  
# This is suppose to set the recursion limit higher than the default,
# to make sure that we can cope with very large user input
sys.setrecursionlimit(10**6) 


def _euler_algorithm(population, infected, recovered, alpha, gamma, count, step):
    if count == 0:
        T_0 = count
        S_0 = population - infected - recovered
        I_0 = infected
        R_0 = recovered
        return [T_0], [S_0], [I_0], [R_0]
    else:
        val = _euler_algorithm(population, infected, recovered, alpha, gamma, count-1, step)

        # Here we do the calculations specified by the differential equations
        T_next = val[0][count-1] + step
        S_next = -alpha * val[1][count-1] * val[2][count-1] * step + val[1][count-1]
        I_next = (alpha * val[1][count-1] * val[2][count-1] - gamma * val[2][count-1]) * step + val[2][count-1]
        R_next = gamma * val[2][count-1] * step + val[3][count-1]

        # Append the values to the end of the sequence
        val[0].append(T_next)
        val[1].append(S_next)
        val[2].append(I_next)
        val[3].append(R_next)

        return val


# Right now we are making a new figure everytime we submit new values.
# I don't know if this should be different, like just changing one global figure variable.
# Maybe this: 
# https://stackoverflow.com/questions/12124350/how-to-update-the-contents-of-a-figurecanvastkagg
def _configure_plot(population, infected, recovered, alpha, gamma, days, step):
    fig = Figure()
    # "1x1 grid, first subplot" got it from here:
    # https://stackoverflow.com/questions/3584805/in-matplotlib-what-does-the-argument-mean-in-fig-add-subplot111
    ax = fig.add_subplot(1, 1, 1)

    # Set labels
    ax.set_xlabel('Time/Days')
    ax.set_ylabel('Number of people')

    # Insert a grid
    ax.grid(b=True)

    # Remove the ticks along the axis
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)

    # Amount of iterations to do.
    # Use int() to round down the potential float value of the division
    count = int(days / step)
    val = _euler_algorithm(population, infected, recovered, alpha, gamma, count, step)

    ax.plot(val[0], val[1], 'b', label='Susceptible')
    ax.plot(val[0], val[2], 'r', label='Infected')
    ax.plot(val[0], val[3], 'g', label='Recovered')
    ax.legend()

    return fig



