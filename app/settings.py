from pydantic import PositiveInt
from pydantic_settings import BaseSettings

# constant; used for git tags
version = "v1.1.0"


class SolverSettings(BaseSettings):
    # print n_combinations from tests to find the limit
    bruteforce_max_combinations: PositiveInt = 9000
    # that is already unusable x100, but the solver takes it easily
    solver_n_max: PositiveInt = 2000


# defaults can be overwritten via env
solverSettings = SolverSettings()
