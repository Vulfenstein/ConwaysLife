import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

# Returns random grid of NxN values
def randomGrid(N):
    # choice between ON 20% and OFF 80%, reshape 1D into NxN
    return np.random.choice(vals, N*N).reshape(N, N)

#Add glider with top-left cenn at (i, j)
def addGlider(i, j, grid):
    
    glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])

    grid[i:i+3, j:j+3] = glider

# Copy grid since we require 8 neighbors for calculation
# Line by line
def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            #compute 8-neighbor sum using toroidal boundary calculation
            #x and y wrap around so that the simulation takes place on a torodial surface
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            # Apply Conway Rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # Update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main function
def main():
    #parse command line
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life Simulation")
    #parse arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # Set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # Set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # Declare grid
    grid = np.array([])
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    else:
        grid = randomGrid(N)

    # Set animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), 
                                frames=10, interval=updateInterval, save_count=50)

    # number of frames? 
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    # Build
    plt.show()

if __name__ == '__main__':
    main()