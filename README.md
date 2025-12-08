Flow Theory Engines (v1.0)

Reference implementation of Flow Theory Engines A, B, and C by GhostDog.

Flow Theory provides a general dynamic-systems architecture built around the variables Flow, Capacity, Pressure, Drift, and Trust.

These engines implement the core update rules:

Engine A: Single-system dynamics

Engine B: Fast/slow multi-layer recursion

Engine C: System-of-systems contagion via pressure coupling

All engines are general, parameter-driven, and domain-agnostic.

Open Research Framework

Flow Theory is released as an open, extensible research framework.

You are free to break, improve, extend, fork, rebuild, adapt, or evolve the engines in any direction you find valuable.

All I ask is that you preserve attribution to:

GhostDog — “The Flow Architecture: A Unified Model of Adaptive Cycles” (SSRN, 2025).

Files Included

engine_a.py
Single-system engine implementing Flow–Capacity–Pressure–Drift–Trust dynamics.

engine_b.py
Two-layer engine modeling fast/slow system interactions and recursive feedback.

engine_c.py
Multi-system contagion engine using pressure-coupling matrices.

License

Released under the MIT License to support unrestricted academic and research use.
You may use, modify, redistribute, or extend this work freely with attribution.
