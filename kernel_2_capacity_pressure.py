"""
Kernel 2 — Borrow–Return + Capacity + Pressure

Adds:
- Capacity C_t
- Pressure P_t = F_t - C_t

Flow is defined as F_t = I_t - O_t.
Capacity adjusts slowly toward F_t:

C_{t+1} = C_t + k * (F_t - C_t)
"""

from dataclasses import dataclass
from typing import List, Callable


@dataclass
class Kernel2State:
    t: int
    stock: float
    inflow: float
    outflow: float
    flow: float
    capacity: float
    pressure: float


def kernel2_step(
    stock: float,
    capacity: float,
    inflow: float,
    outflow: float,
    k_capacity: float,
):
    """
    One step of Kernel 2.

    Parameters
    ----------
    stock : float
        S_t
    capacity : float
        C_t
    inflow : float
        I_t
    outflow : float
        O_t
    k_capacity : float
        Speed of capacity adjustment k

    Returns
    -------
    (stock_next, capacity_next, flow, pressure)
    """
    flow = inflow - outflow
    pressure = flow - capacity
    stock_next = stock + inflow - outflow          # Borrow–Return
    capacity_next = capacity + k_capacity * (flow - capacity)
    return stock_next, capacity_next, flow, pressure


def simulate_kernel2(
    T: int,
    S0: float,
    C0: float,
    k_capacity: float,
    inflow_rule: Callable[[int, float, float], float],
    outflow_rule: Callable[[int, float, float], float],
) -> List[Kernel2State]:
    """
    Simulate Kernel 2 for T steps.

    inflow_rule(t, S_t, C_t), outflow_rule(t, S_t, C_t)
    define I_t and O_t.
    """

    states: List[Kernel2State] = []
    S = S0
    C = C0

    for t in range(T):
        I_t = inflow_rule(t, S, C)
        O_t = outflow_rule(t, S, C)

        S_next, C_next, F_t, P_t = kernel2_step(
            stock=S,
            capacity=C,
            inflow=I_t,
            outflow=O_t,
            k_capacity=k_capacity,
        )

        states.append(
            Kernel2State(
                t=t,
                stock=S,
                inflow=I_t,
                outflow=O_t,
                flow=F_t,
                capacity=C,
                pressure=P_t,
            )
        )

        S, C = S_next, C_next

    return states
