from dataclasses import dataclass
from typing import Optional


@dataclass
class EngineAState:
    """
    State of a single Flow Theory system.

    F = Flow / activity / load
    C = Capacity / limit
    T = Trust (0–1)
    D = Drift / accumulated fragility
    """
    F: float
    C: float
    T: float
    D: float


@dataclass
class EngineAParams:
    """
    Parameters for Engine A dynamics.

    r               = strength of trust → flow reinforcement
    alpha           = pressure → drift (fragility build-up)
    delta           = drift decay / self-correction
    lambda_trust    = pressure → trust loss
    rho_trust       = baseline trust recovery
    kappa_capacity  = speed of capacity adjustment toward flow
    """
    r: float
    alpha: float
    delta: float
    lambda_trust: float
    rho_trust: float
    kappa_capacity: float


def engine_a_step(
    state: EngineAState,
    params: EngineAParams,
    shock_F: float = 0.0,
    shock_C: float = 0.0,
) -> EngineAState:
    """
    One time step update for a single system.

    All shocks are exogenous. Pressure is endogenous:
        P_t = max(0, F_t - C_t)
    """
    F, C, T, D = state.F, state.C, state.T, state.D

    # Structural overload
    P = max(0.0, F - C)

    # Drift (fragility) update
    D_next = D + params.alpha * P - params.delta * D

    # Trust update, clamped to [0, 1]
    T_next = T + params.rho_trust - params.lambda_trust * P
    T_next = max(0.0, min(1.0, T_next))

    # Capacity slowly adjusts toward flow
    C_next = C + params.kappa_capacity * (F - C) + shock_C

    # Flow responds to trust, pressure, and shocks
    F_next = F + params.r * T_next + shock_F - P

    return EngineAState(F=F_next, C=C_next, T=T_next, D=D_next)


def run_engine_a(
    state: EngineAState,
    params: EngineAParams,
    steps: int,
    shocks_F: Optional[list[float]] = None,
    shocks_C: Optional[list[float]] = None,
) -> list[EngineAState]:
    """
    Run Engine A for a fixed number of steps.
    shocks_F / shocks_C are optional lists of exogenous shocks.
    """
    history = [state]

    for t in range(steps):
        sF = shocks_F[t] if shocks_F is not None and t < len(shocks_F) else 0.0
        sC = shocks_C[t] if shocks_C is not None and t < len(shocks_C) else 0.0
        state = engine_a_step(state, params, shock_F=sF, shock_C=sC)
        history.append(state)

    return history
