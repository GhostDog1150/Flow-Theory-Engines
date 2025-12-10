"""
Two-System Contagion Kernel

Minimal demonstration of:
- Overshoot in a fast subsystem (1)
- Drift accumulation in both subsystems
- Shared trust as a stabilizing resource
- Contagion from system 1 into system 2

This kernel corresponds to the two-system contagion example in the
mechanical foundations paper (Paper 2). It is not a full Engine B/C
implementation, but a compact illustration of how overshoot in a
fast-moving system can transmit strain into a slower system.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TwoSystemState:
    t: int
    # System 1 (fast)
    F1: float
    C1: float
    P1: float
    D1: float
    # System 2 (slow)
    F2: float
    C2: float
    P2: float
    D2: float
    # Shared trust
    T: float


def two_system_step(
    F1: float,
    C1: float,
    D1: float,
    F2: float,
    C2: float,
    D2: float,
    T: float,
    # Parameters
    k1: float,
    k2: float,
    alpha1: float,
    alpha2: float,
    delta1: float,
    delta2: float,
    r1: float,
    r2: float,
    lambda_T: float,
    coupling: float,
    shock1: float,
):
    """
    Single update step for the two-system kernel.

    Parameters
    ----------
    F1, C1, D1 : float
        Flow, capacity, and drift for system 1 (fast subsystem)
    F2, C2, D2 : float
        Flow, capacity, and drift for system 2 (slow subsystem)
    T : float
        Shared trust level for the combined system
    k1, k2 : float
        Capacity adjustment speeds for systems 1 and 2
    alpha1, alpha2 : float
        Drift accumulation rates for systems 1 and 2
    delta1, delta2 : float
        Drift decay rates for systems 1 and 2
    r1, r2 : float
        Trust sensitivity parameters for systems 1 and 2
    lambda_T : float
        Rate at which pressure erodes shared trust
    coupling : float
        Strength of strain transmission from system 1 to system 2
    shock1 : float
        Exogenous disturbance applied to flow in system 1

    Returns
    -------
    F1_next, C1_next, D1_next,
    F2_next, C2_next, D2_next,
    T_next, P1, P2
    """

    # Local pressures
    P1 = F1 - C1
    P2 = F2 - C2

    # Drift updates: system 2 imports part of system 1's pressure
    D1_next = (1.0 - delta1) * D1 + alpha1 * P1
    D2_next = (1.0 - delta2) * D2 + alpha2 * (P2 + coupling * P1)

    # Shared trust update: eroded by total absolute pressure
    total_pressure = abs(P1) + abs(P2)
    T_next = max(0.0, T - lambda_T * total_pressure)

    # Flow updates: trust supports flow; drift and pressure reduce it
    F1_next = F1 + r1 * T - D1 - P1 + shock1
    F2_next = F2 + r2 * T - D2 - P2

    # Capacity updates: slow adaptation toward observed flow
    C1_next = C1 + k1 * (F1 - C1)
    C2_next = C2 + k2 * (F2 - C2)

    return F1_next, C1_next, D1_next, F2_next, C2_next, D2_next, T_next, P1, P2


def simulate_two_system_kernel(
    T_steps: int,
    # Initial states
    F1_0: float,
    C1_0: float,
    D1_0: float,
    F2_0: float,
    C2_0: float,
    D2_0: float,
    T0: float,
    # Parameters
    k1: float = 0.2,
    k2: float = 0.05,
    alpha1: float = 0.4,
    alpha2: float = 0.2,
    delta1: float = 0.1,
    delta2: float = 0.05,
    r1: float = 0.8,
    r2: float = 0.5,
    lambda_T: float = 0.1,
    coupling: float = 0.3,
    # Shock path
    bubble_steps: int = 10,
    bubble_shock: float = 0.5,
) -> List[TwoSystemState]:
    """
    Simulate the two-system contagion kernel for T_steps.

    By default, an early "bubble" is injected into system 1 for
    `bubble_steps` periods via a positive flow shock. After that,
    shock1 = 0 and the system is allowed to correct and transmit
    strain into system 2.

    Parameters
    ----------
    T_steps : int
        Number of time steps to simulate
    F1_0, C1_0, D1_0 : float
        Initial flow, capacity, drift for system 1
    F2_0, C2_0, D2_0 : float
        Initial flow, capacity, drift for system 2
    T0 : float
        Initial shared trust level
    Other parameters : float
        Structural parameters as described in two_system_step
    bubble_steps : int
        Number of periods in which system 1 receives a positive bubble shock
    bubble_shock : float
        Magnitude of the bubble shock applied to system 1 during bubble_steps

    Returns
    -------
    List[TwoSystemState]
        Time series of states for both systems and shared trust.
    """

    states: List[TwoSystemState] = []

    F1, C1, D1 = F1_0, C1_0, D1_0
    F2, C2, D2 = F2_0, C2_0, D2_0
    T = T0

    for t in range(T_steps):
        # Early bubble in system 1, then zero shock
        shock1 = bubble_shock if t < bubble_steps else 0.0

        F1, C1, D1, F2, C2, D2, T, P1, P2 = two_system_step(
            F1=F1,
            C1=C1,
            D1=D1,
            F2=F2,
            C2=C2,
            D2=D2,
            T=T,
            k1=k1,
            k2=k2,
            alpha1=alpha1,
            alpha2=alpha2,
            delta1=delta1,
            delta2=delta2,
            r1=r1,
            r2=r2,
            lambda_T=lambda_T,
            coupling=coupling,
            shock1=shock1,
        )

        states.append(
            TwoSystemState(
                t=t,
                F1=F1,
                C1=C1,
                P1=P1,
                D1=D1,
                F2=F2,
                C2=C2,
                P2=P2,
                D2=D2,
                T=T,
            )
        )

    return states
