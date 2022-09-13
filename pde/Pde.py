import abc
from fractions import Fraction
from collections import namedtuple

GridPoint = namedtuple('GridPoint', 'ix x fx')
GridParameters = namedtuple('GridParameters', 'x_steps x_min x_max t t_steps')

class PdeSlice:

    def __init__(self, params):
        delta_x = (params.x_max - params.x_min)/(params.x_steps - 1)

        grid = []
        for i in range(0, params.x_steps):
            x =  params.x_min + delta_x * i
            fx = self.initialize_value(x)
            point = GridPoint(ix = i, x=x, fx = fx)
            grid.append(point)

        self.params = params
        self.grid = grid
        self.delta_x = delta_x
        self.t = Fraction(params.t, 1)
        self.delta_t = Fraction(params.t, params.t_steps)


    def ddx_right(self, grid_point):
        if grid_point < self.params.x_steps - 1:
            return (self.grid[grid_point + 1].fx - self.grid[grid_point].fx)/self.delta_x
        else:
            return self.ddx_upper_bound()

    def ddx_left(self, grid_point):
        if grid_point > 0:
            return (self.grid[grid_point].fx - self.grid[grid_point - 1].fx)/self.delta_x
        else:
            return self.ddx_lower_bound()

    def ddx(self, grid_point):
        return (self.ddx_right(grid_point) + self.ddx_left(grid_point))/2

    def d2dx2(self, grid_point):
        return (self.ddx_right(grid_point) - self.ddx_left(grid_point))/self.delta_x

    def step_backwards(self):
        new_grid = []
        for gp in self.grid:
            dt = self.pde_dt(gp)
            fx_new = gp.fx - dt * self.delta_t
            gp_new = GridPoint(ix = gp.ix, x = gp.x, fx= fx_new)
            new_grid.append(gp_new)

        self.grid = new_grid
        self.t = self.t - self.delta_t

    def solve(self):
        while self.t > Fraction(0, 1):
            self.step_backwards()



    ### This is an abstract method that is called by the
    ### __init__ method to set the intial function value for
    ### grid point x.
    @abc.abstractmethod
    def initialize_value(self, x):
        pass

    ### This is an abstract method that is called by the
    ### __init__ method to set the derivative value at the
    ### upper value for x.
    @abc.abstractmethod
    def ddx_upper_bound(self):
        pass

    ### This is an abstract method that is called by the
    ### __init__ method to set the derivative value at the
    ### lower value for x.
    @abc.abstractmethod
    def ddx_lower_bound(self):
        pass
