# CutSolver

This is used to solve the "Cutting Stock Problem", which is NP-hard.  
It can be reduced to the Bin-Packing-Problem (BPP).

Brute Force(best solution) for small n, Heuristic(fast solution) für larger n

# Usage
Start flask service locally using `flask run` in project folder.

# Roadmap
Host as backend
Make a nice UI with Bootstrap?

## Declined
Having workers and a queue with pending jobs was considered but seemed useless, 
as ideally all requests have their own thread and a (by comparison) short calculation time.
This makes a queue useless. The same argumentation also holds for a result-buffer.

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