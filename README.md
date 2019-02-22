# CutSolver

This is used to solve the "Cutting Stock Problem", which is NP-hard.  
It can be reduced to the Bin-Packing-Problem (BPP).

Brute Force(best solution) for small n, Heuristic(fast solution) für larger n

# Usage
Start flask service locally using `flask run` in project folder.

# Roadmap
Host as backend
Make a nice UI with Bootstrap?


# Visualisation
// This should definitely be a svg.
<pre>
XXXXXXXXXXXXXXXX  
XXXXX
     I  
      XXXXXX
            I
             XXX  
</pre>

# Troubleshooting

## My results are missing decimals
This Solver is using ints exclusively, try to use whole numbers instead.

# External links
https://scipbook.readthedocs.io/en/latest/bpp.html