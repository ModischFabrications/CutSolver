# CutSolver

This is used to solve the "Cutting Stock Problem", which is NP-hard.  
It can be reduced to the Bin-Packing-Problem (BPP).

Brute Force(best solution) for small n, Heuristic(fast solution) für larger n

# Usage
Make sure that you have installed Docker.  

1. Build this image using `docker_build.sh`
1. Start using `docker_start.sh`
1. Send POST-Requests to `[localhost]/solve`, see `/docs` for further informations.

# Roadmap
1. Make a nice UI with Bootstrap?

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

# Dependencies
*Everything should be handled by Docker*

This project uses:
1. [pipenv](https://github.com/pypa/pipenv): library management
1. [FastAPI](https://github.com/tiangolo/fastapi): easy webservice (this includes much more!)

# Troubleshooting

## My results are missing decimals
This Solver is using ints exclusively, try to use whole numbers instead.

# External links
https://scipbook.readthedocs.io/en/latest/bpp.html


