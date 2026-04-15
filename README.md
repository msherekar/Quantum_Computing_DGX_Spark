# Quantum Computing on DGX Spark

This repository contains CUDA-Q Python scripts based on the guide in
`Quantum_Circuit_Simulation_Guide_DGX_Spark.txt`, organized by section for easy execution.
It is set up with `uv` + `pyproject.toml` and targets NVIDIA-accelerated quantum simulation workflows.

## Why This Repo Matters (Especially for Beginners)

If you are new to quantum computing, this repo gives you a practical learning path instead of
jumping straight into abstract theory. You can run real circuits, inspect outputs, and understand
how qubit count, memory, and backend choice affect what is feasible on actual hardware.

It is beginner-friendly because it:

- converts the guide into ready-to-run scripts by section
- uses a reproducible setup (`uv` + `pyproject.toml`) so environment issues are minimized
- starts with approachable 15-qubit examples before moving to larger simulations
- includes memory checks and backend recommendations to prevent common beginner mistakes
- demonstrates both full state-vector and tensor-network workflows in one place

## DGX Spark Advantage

DGX Spark is a strong platform for first-time and advanced users because it combines GPU
acceleration with large unified memory, which is critical for quantum simulation workloads.
In practice, this means:

- faster local iteration compared to CPU-only development
- ability to run larger state-vector circuits (up to around 33 qubits, memory dependent)
- support for tensor-network methods (40+ qubits in suitable low-entanglement circuits)
- less dependence on remote/cloud resources for daily experimentation
- a smoother bridge from learning examples to research-style workflows

## What This Project Includes

- Section 2: 15-qubit examples (GHZ and QFT)
- Section 3: memory scaling analysis and 33-qubit max-capacity simulation
- Section 4: tensor-network (MPS) simulation beyond 33 qubits
- Section 5: backend selection + memory monitoring best practices

## Project Structure

- `src/quantum_15qubit_ghz.py` - Section 2.2/2.3 GHZ simulation (15 qubits)
- `src/quantum_15qubit_qft.py` - Section 2.4 QFT-style simulation (15 qubits)
- `src/memory_scaling_analysis.py` - Section 3.1 memory feasibility checks
- `src/quantum_33qubit_max_capacity.py` - Section 3.2 33-qubit max-capacity run
- `src/quantum_mps_42qubit.py` - Section 4.1 MPS simulation (42 qubits)
- `src/performance_best_practices.py` - Section 5.1/5.2 backend + memory guidance
- `scripts/setup_github_repo.sh` - reusable git/GitHub bootstrap script
- `pyproject.toml` - dependencies and Python/uv configuration

## Prerequisites

- Linux with NVIDIA GPU support
- Python 3.11+
- `uv` installed ([docs](https://docs.astral.sh/uv/))
- CUDA drivers/toolkit compatible with CUDA Quantum runtime

## Environment Setup (uv)

From project root:

```bash
uv sync
```

This creates `.venv` and installs:

- `cudaq`
- `cuda-quantum-cu13`
- `numpy`
- `psutil`

Quick verification:

```bash
uv run python -c "import cudaq, numpy, psutil; print(cudaq.__version__)"
```

## Running Scripts

All commands are run from project root.

### Section 2 - 15-Qubit Simulations

GHZ:

```bash
uv run python src/quantum_15qubit_ghz.py --target nvidia --shots 10000
```

QFT:

```bash
uv run python src/quantum_15qubit_qft.py --target nvidia --shots 5000
```

For quick CPU smoke tests (non-GPU), use:

```bash
uv run python src/quantum_15qubit_ghz.py --target qpp-cpu --shots 100
```

### Section 3 - Scaling to Maximum Capacity

Memory scaling report:

```bash
uv run python src/memory_scaling_analysis.py --qubits 15 20 25 30 33 34 --buffer 1.10
```

33-qubit max-capacity simulation:

```bash
uv run python src/quantum_33qubit_max_capacity.py --target nvidia --shots 1000
```

If memory check blocks execution but you want to force a run:

```bash
uv run python src/quantum_33qubit_max_capacity.py --force
```

### Section 4 - Tensor Network (MPS) Simulation

```bash
uv run python src/quantum_mps_42qubit.py --target tensornet-mps --shots 1000
```

Use this backend for larger, low-entanglement circuits (nearest-neighbor style).

### Section 5 - Performance Best Practices

```bash
uv run python src/performance_best_practices.py --qubits 15 20 25 30 33 34
```

For noisy-circuit recommendation mode:

```bash
uv run python src/performance_best_practices.py --noisy
```

## Backend Guidance

- `nvidia`: full state-vector simulation, practical up to around 33 qubits (memory-limited)
- `tensornet-mps`: better for larger qubit counts with structured/limited entanglement
- `density-matrix-cpu`: useful for noisy/decoherence-focused small-to-medium circuits

## Docker (cuQuantum Appliance)

For ARM64/aarch64 systems (like your DGX Spark host), use ARM64 image tags.
Example:

```bash
docker pull nvcr.io/nvidia/cuquantum-appliance:25.11-cuda13.0.1-devel-ubuntu24.04-arm64
```

Do not use `...-x86_64` tags on ARM hosts.

## Git/GitHub Bootstrap Script

To initialize repo files/remotes quickly in new projects:

```bash
./scripts/setup_github_repo.sh "Quantum_Computing_DGX_Spark" "https://github.com/msherekar/Quantum_Computing_DGX_Spark.git"
```

Skip push:

```bash
./scripts/setup_github_repo.sh "Quantum_Computing_DGX_Spark" "https://github.com/msherekar/Quantum_Computing_DGX_Spark.git" --no-push
```

## Troubleshooting

- `ModuleNotFoundError: cudaq`
  - Run `uv sync` again
  - Ensure `cuda-quantum-cu13` is in dependencies
- Slow runs or failures on large circuits
  - Check memory availability before execution
  - Use MPS backend for larger low-entanglement circuits
- GPU issues
  - Validate NVIDIA driver/toolkit setup
  - Confirm backend target with `--target nvidia`

## Next Suggested Additions

- Section 5.3 batch parameter sweep script
- Section 6 application scripts (VQE, feature maps, QAOA)
- basic `tests/` smoke checks for each script
