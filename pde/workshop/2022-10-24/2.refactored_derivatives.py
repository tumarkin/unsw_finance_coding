from collections import namedtuple

# Stock parameters
strike = 50
rf = 0.10
sigma = 0.3
# dividend_yield = 0.05
t_to_expiration = 1

# Grid parameters
s_min = 1
s_max = 100
s_steps = 99
t_steps = 5000

delta_t = t_to_expiration / t_steps
delta_x = (s_max - s_min)/s_steps

# Tuple to store grid data
#   ix: index point
#   x:  stock price
#   fx: call option price
GridPoint = namedtuple('GridPoint', 'ix x fx')

def dfdx_left(values, grid_index):
    if grid_index > 0:
       return (values[grid_index].fx -values[grid_index-1].fx) / delta_x
    else:
       return 0

def dfdx_right(values, grid_index):
    if grid_index < s_steps:
       return (values[grid_index+1].fx -values[grid_index].fx) / delta_x
    else:
       return 1

def dfdx(values, grid_index):
    return 0.5  * (dfdx_left(values, grid_index)+ dfdx_right(values, grid_index))

def d2fdx2(values, grid_index):
    return (dfdx_right(values, grid_index) - dfdx_left(values, grid_index)) / delta_x

def step(values):
    values_back = []
    for i in range(0, s_steps + 1):
        # C(S,t)
        gp_current = values[i]
        _dfdx = dfdx(values, i)
        _d2fdx2 = d2fdx2(values, i)
    
        # Solve for dCdT in PDE
        dCdT = rf * gp_current.fx - \
               _dfdx * gp_current.x * rf - \
               0.5 * _d2fdx2 * sigma ** 2 * gp_current.x ** 2
        
        # Numerical derivatives to get C(S,t-delta t)
        c_back = gp_current.fx - delta_t * dCdT
        
        gp_back = GridPoint(ix = i, x = gp_current.x, fx = c_back)
        
        values_back.append(gp_back)
    
    return (values_back)

def initialize():
    values = []
    for i in range(0, s_steps + 1):
        stock = s_min + i * (s_max - s_min)/s_steps
        call = max(stock - strike, 0)
        gp = GridPoint(ix = i, x = stock, fx = call)
        values.append(gp)
    return (values)


# Set up a loop
if __name__ == '__main__':
    values = initialize()
    for _ in range(0, t_steps):
        values = step(values)

    print(values[50])
