"""
Kernel 3 — Borrow–Return + Pressure + Drift

Adds drift D_t as an exponentially weighted memory of pressure:

    D_{t+1} = (1 - delta) * D_t + alpha * P_t

Flow, capacity, and pressure follow the same structure as Kernel 2.
This is the smallest kernel that generates
expansion–imbalance–correction–renewal cycles.
"""

from dataclasses import dataclass
from typing import List, Callable


@dataclass
class Kernel3State:
    t: int
    stock: float
    inflow: float
    outflow: float
    flow: float
    capacity: float
    pressure: float
    drift: float


def kernel3_step(
    stock: float,
    capacity: float,
    drift: float,
    inflow: float,
    outflow: float,
    k_capacity: float,
    alpha: float,
    delta: float,
):
    """
    One step of Kernel 3.

    Parameters
    ----------
    stock : float
        S_t
    capacity : float
        C_t
    drift : float
        D_t
    inflow : float
        I_t
    outflow : float
        O_t
    k_capacity : float
        Speed of capacity adjustment k
    alpha : float
        Drift accumulation rate
    delta : float
        Drift decay rate

    Returns
    -------
    stock_next : float
    capacity_next : float
    drift_next : float
    flow : float
    pressure : float
    """
    # Net flow and pressure
    flow = inflow - outflow
    pressure = flow - capacity

    # Borrow–Return
    stock_next = stock + inflow - outflow

    # Capacity adjustment
    capacity_next = capacity + k_capacity * (flow - capacity)

    # Drift accumulation (exponentially weighted memory of pressure)
    drift_next = (1.0 - delta) * drift + alpha * pressure

    return stock_next, capacity_next, drift_next, flow, pressure


def simulate_kernel3(
    T: int,
    S0: float,
    C0: float,
    D0: float,
    k_capacity: float,
    alpha: float,
    delta: float,
    inflow_rule: Callable[[int, float, float, float], float],
    outflow_rule: Callable[[int, float, float, float], float],
) -> List[Kernel3State]:
    """
    Simulate Kernel 3 for T steps.

    inflow_rule(t, S_t, C_t, D_t) and outflow_rule(t, S_t, C_t, D_t)
    define I_t and O_t.

    Parameters
    ----------
    T : int
        Number of time steps
    S0 : float
        Initial stock S_0
    C0 : float
        Initial capacity C_0
    D0 : float
        Initial drift D_0
    k_capacity : float
        Speed of capacity adjustment
    alpha : float
        Drift accumulation rate
    delta : float
        Drift decay rate
    inflow_rule : callable
        Function (t, S_t, C_t, D_t) -> I_t
    outflow_rule : callable
        Function (t, S_t, C_t, D_t) -> O_t

    Returns
    -------
    List[Kernel3State]
        Time series of kernel states
    """

    states: List[Kernel3State] = []
    S = S0
    C = C0
    D = D0

    for t in range(T):
        I_t = inflow_rule(t, S, C, D)
        O_t = outflow_rule(t, S, C, D)

        S_next, C_next, D_next, F_t, P_t = kernel3_step(
            stock=S,
            capacity=C,
            drift=D,
            inflow=I_t,
            outflow=O_t,
            k_capacity=k_capacity,
            alpha=alpha,
            delta=delta,
        )

        states.append(
            Kernel3State(
                t=t,
                stock=S,
                inflow=I_t,
                outflow=O_t,
                flow=F_t,
                capacity=C,
                pressure=P_t,
                drift=D,
            )
        )

        S, C, D = S_next, C_next, D_next

    return states
