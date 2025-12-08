from dataclasses import dataclass
from typing import List, Optional
from engine_a import EngineAState, EngineAParams, engine_a_step


@dataclass
class EngineCState:
    """
    State of N coupled systems.
    Each element in 'systems' is an EngineAState.
    """
    systems: List[EngineAState]


@dataclass
class EngineCParams:
    """
    Parameters for Engine C:

    params_per_system = list of EngineAParams, one for each system
    W                 = coupling matrix (N x N),
                        where W[i][j] is impact of j's pressure on i's flow.
    """
    params_per_system: List[EngineAParams]
    W: List[List[float]]  # size N x N


def engine_c_step(
    state: EngineCState,
    params: EngineCParams,
    shocks_F: Optional[List[float]] = None,
    shocks_C: Optional[List[float]] = None,
) -> EngineCState:
    """
    One time step of the system-of-systems engine.

    - Each system has Engine A dynamics.
    - Pressure from each system j contributes to an endogenous shock to i:
          S_i = sum_j W[i][j] * P_j
      where P_j = max(0, F_j - C_j).
    - This S_i is added to any exogenous shock_F[i].
    """

    N = len(state.systems)
    assert len(params.params_per_system) == N
    assert len(params.W) == N and all(len(row) == N for row in params.W)

    # Compute pressures for all systems
    pressures = []
    for s in state.systems:
        P = max(0.0, s.F - s.C)
        pressures.append(P)

    # Compute endogenous shocks from coupling
    endogenous_shocks_F = [0.0] * N
    for i in range(N):
        total = 0.0
        for j in range(N):
            total += params.W[i][j] * pressures[j]
        endogenous_shocks_F[i] = total

    # Apply dynamics to each system
    new_systems: List[EngineAState] = []
    for i in range(N):
        s = state.systems[i]
        p = params.params_per_system[i]

        exo_F = shocks_F[i] if shocks_F is not None and i < len(shocks_F) else 0.0
        exo_C = shocks_C[i] if shocks_C is not None and i < len(shocks_C) else 0.0

        total_F_shock = exo_F + endogenous_shocks_F[i]

        new_s = engine_a_step(
            state=s,
            params=p,
            shock_F=total_F_shock,
            shock_C=exo_C,
        )
        new_systems.append(new_s)

    return EngineCState(systems=new_systems)


def run_engine_c(
    state: EngineCState,
    params: EngineCParams,
    steps: int,
) -> List[EngineCState]:
    """
    Run Engine C forward without exogenous shocks.
    (You can extend this to pass shock sequences.)
    """
    history = [state]
    for _ in range(steps):
        state = engine_c_step(state, params)
        history.append(state)
    return history
