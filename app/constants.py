from pydantic import BaseModel

# used for git tags
version = "v1.0.1"


class SolverSettings(BaseModel):
    bruteforce_max_combinations: int
    n_max: int


# TODO should be startup parameter
solverSettings = SolverSettings(
    # Desktop with Ryzen 2700X:
    # (4, 3, 2)=1260 => 0.1s, (4, 3, 3)=4200 => 0.8s, (5, 3, 3)=9240 => 8s
    bruteforce_max_combinations=5000,
    # that is already unusable x100, but the solver takes it easily
    n_max=2000
)
