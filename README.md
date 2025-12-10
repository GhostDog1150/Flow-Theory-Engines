# Flow Theory Engines & Kernels (v1.1)
### Reference Implementation by GhostDog

Flow Theory introduces a unified dynamic-systems architecture built on five core variables:

**Flow — Capacity — Pressure — Drift — Trust**

These variables generate adaptive cycles observed across financial markets, institutional systems, technological environments, ecological networks, and interconnected multi-system structures.

This repository provides the official minimal reference implementation for:

- Engines A–C (full Flow Architecture)
- Kernels 1–3 (mechanical foundations)
- The Two-System Contagion Kernel

These files correspond directly to the models described in the Flow Theory papers released on SSRN (2025).


# 🚀 What’s Included

## ENGINES — Full Flow Architecture

### Engine A — Single-System Dynamics
A compact model of one adaptive system evolving through:
- expansion  
- overshoot  
- drift accumulation  
- contraction  
- stabilization  
- renewal  

**File:** `engine_a.py`


### Engine B — Fast/Slow Recursive Dynamics
A two-layer structure where:
- a fast subsystem reacts immediately (e.g., markets)  
- a slow subsystem adjusts gradually (e.g., institutions)  

Structural feedback links the layers.

**File:** `engine_b.py`


### Engine C — System-of-Systems Contagion
Multiple interacting systems coupled through pressure-transmission parameters. Models:
- contagion  
- synchronization  
- structural divergence  
- cascading stress  
- network-level fragility  

**File:** `engine_c.py`



# 🔬 MINIMAL KERNELS — Foundational Building Blocks

These kernels isolate the smallest possible structures capable of generating Flow Theory dynamics. They are intentionally simple and support reproducibility, clarity, and experimentation.


### Kernel 1 — Borrow–Return Identity
Pure conservation:

**Sₜ₊₁ = Sₜ + Iₜ − Oₜ**

No capacity, no drift, no trust — the structural backbone of the entire theory.

**File:** `kernel_1_borrow_return.py`


### Kernel 2 — Capacity + Pressure
Adds:
- capacity lag  
- overshoot  
- pressure Pₜ = Fₜ − Cₜ  

This is the first kernel where imbalance becomes possible.

**File:** `kernel_2_capacity_pressure.py`


### Kernel 3 — Drift + Adaptive Cycle
Adds drift as structural memory:

**Dₜ₊₁ = (1 − δ)Dₜ + αPₜ**

This is the smallest kernel that produces the full Flow Theory cycle:
- expansion  
- overshoot  
- drift accumulation  
- correction  
- renewal  

**File:** `kernel_3_drift_cycle.py`


### Two-System Contagion Kernel
Minimal demonstration of:
- overshoot in a fast subsystem  
- drift accumulation  
- shared trust  
- contagion into a slower subsystem  

Models cross-system stress propagation without behavioral assumptions.

**File:** `two_system_contagion_kernel.py`



# 💡 Philosophy

Flow Theory is released as an **open research framework**.

You are encouraged to:
- explore  
- modify  
- extend  
- break  
- rebuild  

…in any direction that advances understanding of adaptive systems or systemic behavior.

The engines and kernels prioritize:
- **clarity over complexity**  
- **structure over noise**  
- **generality over narrow assumptions**



# ⚡ Quick Start

Run any engine directly:
python engine_a.py
python engine_b.py
python engine_c.py


Run any kernel:


Or import into your own project:
```python
from engine_a import engine_A
output = engine_A(F0=1.3, C0=1.0, T0=0.8, D0=0.1, steps=50)


No dependencies beyond standard Python.

📚 Citation

If you use or extend this work, please cite:

GhostDog (2025).
The Flow Architecture: A Unified Model of Adaptive Cycles. SSRN Preprint.

GhostDog (2025).
Flow Theory: Mechanical Foundations, Borrow–Return Dynamics, and Minimal Kernels. SSRN Preprint.

GhostDog (2025).
Flow Theory Across Domains: Universality, Structural Mapping, and Stress-Test Demonstrations. SSRN Preprint.


📝 License — MIT

You may use, modify, distribute, or extend this code freely.
Attribution to GhostDog is the only requirement.

🎯 Purpose

This repository supports:

academic research

system modeling

replication

stress testing

teaching

code validation

open theoretical development

Flow Theory is designed to evolve.
These engines and kernels represent the first reference implementation, not a final boundary.


