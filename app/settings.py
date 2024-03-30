from pydantic import PositiveInt
from pydantic_settings import BaseSettings

# constant; used for git tags
version = "v1.0.1"


class SolverSettings(BaseSettings):
    # Desktop with Ryzen 2700X:
    # (4, 3, 2)=1260 => 0.1s, (4, 3, 3)=4200 => 0.8s, (5, 3, 3)=9240 => 8s
    bruteforce_max_combinations: PositiveInt = 5000
    # that is already unusable x100, but the solver takes it easily
    solver_n_max: PositiveInt = 2000


# defaults can be overwritten via env
solverSettings = SolverSettings()
