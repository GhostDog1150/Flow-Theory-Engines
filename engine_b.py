from dataclasses import dataclass
from typing import Optional
from engine_a import EngineAState


@dataclass
class EngineBLayerParams:
    """
    Parameters for a single layer in Engine B.
    Same structure as Engine A, plus:
    beta_drift_from_other = how much pressure from the other layer
                            leaks into this layer's drift.
    """
    r: float
    alpha: float
    delta: float
    lambda_trust: float
    rho_trust: float
    kappa_capacity: float
    beta_drift_from_other: float  # coupling from other layer's pressure


@dataclass
class EngineBParams:
    """
    Full Engine B parameters:

    fast  = fast layer (markets, AI, short-term system)
    slow  = slow layer (institutions, oversight, infrastructure)
    gamma_fs = slow trust → fast flow reinforcement
    """
    fast: EngineBLayerParams
    slow: EngineBLayerParams
    gamma_fs: float  # impact of slow trust on fast flow


@dataclass
class EngineBState:
    fast: EngineAState
    slow: EngineAState


def engine_b_step(
    state: EngineBState,
    params: EngineBParams,
    shock_F_fast: float = 0.0,
    shock_C_fast: float = 0.0,
    shock_F_slow: float = 0.0,
    shock_C_slow: float = 0.0,
) -> EngineBState:
    """
    One time step of a two-layer fast/slow system.

    - Fast and slow each have Engine A–style dynamics.
    - Both layers feel their own pressure.
    - Slow drift also responds to fast pressure (beta_drift_from_other).
    - Fast flow also responds to slow trust (gamma_fs).
    """

    # Unpack
    Ff, Cf, Tf, Df = state.fast.F, state.fast.C, state.fast.T, state.fast.D
    Fs, Cs, Ts, Ds = state.slow.F, state.slow.C, state.slow.T, state.slow.D

    # Pressures
    Pf = max(0.0, Ff - Cf)
    Ps = max(0.0, Fs - Cs)

    # --- FAST LAYER ---

    # Drift (fast)
    Df_next = Df + params.fast.alpha * Pf - params.fast.delta * Df

    # Trust (fast)
    Tf_next = Tf + params.fast.rho_trust - params.fast.lambda_trust * Pf
    Tf_next = max(0.0, min(1.0, Tf_next))

    # Capacity (fast)
    Cf_next = Cf + params.fast.kappa_capacity * (Ff - Cf) + shock_C_fast

    # Flow (fast) – responds to its own trust plus slow trust
    Ff_next = (
        Ff
        + params.fast.r * Tf_next
        + params.gamma_fs * Ts   # slow trust stabilizing influence
        + shock_F_fast
        - Pf
    )

    # --- SLOW LAYER ---

    # Drift (slow) – gets its own pressure plus some from fast
    Ds_next = Ds + (
        params.slow.alpha * Ps
        + params.slow.beta_drift_from_other * Pf
        - params.slow.delta * Ds
    )

    # Trust (slow)
    Ts_next = Ts + params.slow.rho_trust - params.slow.lambda_trust * Ps
    Ts_next = max(0.0, min(1.0, Ts_next))

    # Capacity (slow)
    Cs_next = Cs + params.slow.kappa_capacity * (Fs - Cs) + shock_C_slow

    # Flow (slow)
    Fs_next = Fs + params.slow.r * Ts_next + shock_F_slow - Ps

    fast_next = EngineAState(F=Ff_next, C=Cf_next, T=Tf_next, D=Df_next)
    slow_next = EngineAState(F=Fs_next, C=Cs_next, T=Ts_next, D=Ds_next)

    return EngineBState(fast=fast_next, slow=slow_next)


def run_engine_b(
    state: EngineBState,
    params: EngineBParams,
    steps: int,
) -> list[EngineBState]:
    """
    Simple runner with no exogenous shocks.
    You can extend this to add shock sequences like in Engine A.
    """
    history = [state]
    for _ in range(steps):
        state = engine_b_step(state, params)
        history.append(state)
    return history
