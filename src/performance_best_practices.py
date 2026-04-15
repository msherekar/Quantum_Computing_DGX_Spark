"""Backend selection and memory monitoring helpers for CUDA-Q workflows.
Implements section 5.1-5.2 guidance from the DGX Spark guide."""

import argparse
import psutil

BYTES_PER_AMPLITUDE = 16
DEFAULT_BUFFER = 1.10
DEFAULT_QUBITS = [15, 20, 25, 30, 33, 34]


def recommend_backend(num_qubits: int, noisy: bool) -> str:
    if noisy or num_qubits <= 16:
        return "density-matrix-cpu"
    if num_qubits > 33:
        return "tensornet-mps"
    return "nvidia"


def check_memory_feasibility(num_qubits: int, buffer_factor: float) -> bool:
    required_bytes = (2 ** num_qubits) * BYTES_PER_AMPLITUDE
    available_bytes = psutil.virtual_memory().available
    feasible = (required_bytes * buffer_factor) < available_bytes
    print(f"Qubits: {num_qubits}")
    print(f"Required: {required_bytes / 1e9:.2f} GB")
    print(f"Available: {available_bytes / 1e9:.2f} GB")
    print(f"Status: {'FEASIBLE ✓' if feasible else 'INSUFFICIENT MEMORY ✗'}")
    return feasible


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Section 5 performance checks.")
    parser.add_argument("--qubits", type=int, nargs="+", default=DEFAULT_QUBITS, help="Qubit counts to evaluate")
    parser.add_argument("--buffer", type=float, default=DEFAULT_BUFFER, help="Safety margin for feasibility")
    parser.add_argument("--noisy", action="store_true", help="Prefer noisy-circuit backend recommendations")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Backend strategy:")
    print("- nvidia: full state vector, up to ~33 qubits")
    print("- tensornet-mps: low-entanglement 1D circuits, 40+ qubits")
    print("- density-matrix-cpu: noisy/decoherence-focused workloads\n")
    for q in args.qubits:
        backend = recommend_backend(q, args.noisy)
        print(f"Recommended backend for {q} qubits: {backend}")
        check_memory_feasibility(q, args.buffer)
        print()


if __name__ == "__main__":
    main()
