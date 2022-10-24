# Overview

This folder contains a refactoring of the source code from 
the original workshop dated 2022-10-10. The steps of the
refactoring are as follows:

## Step 0

`0.initial_code.py` is simply a reference file, unchanged, except for the name,
from `main.py` in the 2022-10-10 workshop.

## Step 1: Variable renaming

`1.renamed_variables.py` renames variables such that they are more general for
PDEs and not named after the Black Scholes PDE variables. The finite differences
grid is indexed by `ix`, with point values `x`, and function values `fx`. Other
variable renaming follows suit.

## Step 2: Derivative functions

`2.refactored_derivatives.py` improves the single derivative function by
splitting the logic into derivatives from the left and from the right. Other
derivatives are rewritten in terms of these and the logic becomes more
simple. This implementation was selected for clarity. It is not an efficient
implementation as dfdx and d2fdx2 each call the same underlying first order
derivatives.

## Step 3: Refactoring

`3.refactoring_by_function_type.py` splits the PDE functions into two groups. One
consists of functions that perform the finite differences. The other is
functions specific to Black Scholes option pricing. Separating the logic will allow
us to group everything into a single meta object first and then use inheritance
to separate the finite differences method from the Black Scholes option, which is
just one possible PDE.

### Step 4: Meta Object

`4.meta_object.py` lays out a single object containing the functions from the 
refactoring step.

### Step 5: Inheritance

`5.inheritance.py` splits the meta object into a Pde object, which handles
setting up the grid and execute finite differences, and the Call Option
object, which specifies the terminal value, boundary conditions, and Black
Scholes PDE.

### Step 6: Final

The pieces from step 5 are split into a `pde.py,` a module that houses
the finite differences solver, and `call.py`, which does a Black Scholes
call. The Black Scholes object now includes a dividend yield. The PDE
object allows for a virtual stopping function. When overwritten
in the Call object, we get the ability for early exercise.

