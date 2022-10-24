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

# Tuple to store grid data
GridPoint = namedtuple('GridPoint', 'ix s c')


def derivatives(values, i):
    gp = values[i]

    if i > 0 and i < s_steps:
        # We know grid point above and below i
        # First get numerical derivatives
        gp_up = values[i + 1]
        gp_down = values[i - 1]

        dCdS_up = (gp_up.c - gp.c)/(gp_up.s - gp.s)
        dCdS_down = (gp.c - gp_down.c)/(gp.s - gp_down.s)

        dCdS = 0.5  * (dCdS_up + dCdS_down)
        d2CdS2 = (dCdS_up - dCdS_down)/(gp_up.s - gp.s)

    elif i == 0:
        dCdS = 0
        d2CdS2 = 0
    else:
        dCdS = 1
        d2CdS2 = 0
    
    return (dCdS, d2CdS2)


def step(values):
    values_back = []
    for i in range(0, s_steps + 1):
        # C(S,t)
        gp_current = values[i]
        dCdS, d2CdS2 = derivatives(values, i)
    
        # Solve for dCdT in PDE
        dCdT = rf * gp_current.c - \
               dCdS * gp_current.s * rf - \
               0.5 * d2CdS2 * sigma ** 2 * gp_current.s ** 2
        
        # Numerical derivatives to get C(S,t-delta t)
        c_back = gp_current.c - delta_t * dCdT
        
        gp_back = GridPoint(ix = i, c = c_back, s = gp_current.s)
        
        values_back.append(gp_back)
    
    return (values_back)

def initialize():
    values = []
    for i in range(0, s_steps + 1):
        s = s_min + i * (s_max - s_min)/s_steps
        c = max(s - strike, 0)
        gp = GridPoint(ix = i, s = s, c = c)
        values.append(gp)
    return (values)


# Set up a loop
if __name__ == '__main__':
    values = initialize()
    for _ in range(0, t_steps):
        values = step(values)

    print(values[50])
    
    
