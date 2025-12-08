Flow Theory Engines (v1.0)

Reference Implementation by GhostDog

Flow Theory introduces a unified dynamic-systems architecture built on five structural variables:

Flow — Capacity — Pressure — Drift — Trust

These variables generate adaptive cycles observed across markets, institutions, technologies, ecosystems, and interconnected system networks.

This repository provides the official, minimal reference engines used in:

GhostDog — “The Flow Architecture: A Unified Model of Adaptive Cycles” (SSRN, 2025)

What’s Included
Engine A — Single-System Dynamics

A compact model of one adaptive system evolving through expansion, strain, contraction, and renewal.

Engine B — Fast/Slow Recursive Dynamics

Two-layer interaction (fast markets ↔ slow institutions) with structural feedback between layers.

Engine C — System-of-Systems Contagion

Multi-system dynamics using pressure-coupling matrices to simulate contagion, synchronization, divergence, and network stress propagation.

Files
engine_a.py
engine_b.py
engine_c.py


All engines are:

parameter-driven

domain-agnostic

designed for research, extension, and experimentation

Philosophy

Flow Theory is released as an open research framework.

You are encouraged to:

explore

modify

extend

break

rebuild

…in any direction that advances understanding of adaptive cycles or systemic behavior.

The engines prioritize:

clarity over complexity

structure over noise

generality over narrow assumptions

Quick Start

Run any engine directly:

python engine_a.py
python engine_b.py
python engine_c.py


Or import into your own work:

from engine_a import engine_A
output = engine_A(F0=1.3, C0=1.0, T0=0.8, D0=0.1, steps=50)


No dependencies beyond standard Python.

Citation

If you use or extend this work, please cite:

GhostDog (2025)
The Flow Architecture: A Unified Model of Adaptive Cycles.
SSRN Preprint.

License — MIT

Flow Theory Engines are released under the MIT License.

You may use, modify, distribute, or extend the code freely.
Attribution to GhostDog is the only requirement.

Purpose

This repository exists to support:

academic research

system modeling

teaching

replication

stress testing

code validation

open theoretical development

Flow Theory is meant to evolve — this is only the first version.
