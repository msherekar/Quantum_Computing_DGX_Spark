"""Analyze memory scaling for state-vector quantum simulation.
Implements section 3.1 feasibility checks from the DGX Spark guide."""

import argparse
import psutil

BYTES_PER_AMPLITUDE = 16
DEFAULT_BUFFER = 1.10
DEFAULT_QUBITS = [15, 20, 25, 30, 33, 34]


def required_bytes(num_qubits: int) -> int:
    return (2 ** num_qubits) * BYTES_PER_AMPLITUDE


def check_memory_feasibility(num_qubits: int, buffer_factor: float) -> bool:
    req = required_bytes(num_qubits)
    avail = psutil.virtual_memory().available
    feasible = (req * buffer_factor) < avail
    print(f"Qubits: {num_qubits}")
    print(f"Required: {req / 1e9:.2f} GB")
    print(f"Available: {avail / 1e9:.2f} GB")
    print(f"Status: {'FEASIBLE ✓' if feasible else 'INSUFFICIENT MEMORY ✗'}\n")
    return feasible


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="State-vector memory feasibility report.")
    parser.add_argument("--buffer", type=float, default=DEFAULT_BUFFER, help="Safety margin factor")
    parser.add_argument("--qubits", type=int, nargs="+", default=DEFAULT_QUBITS, help="Qubit counts")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for qubits in args.qubits:
        check_memory_feasibility(qubits, args.buffer)


if __name__ == "__main__":
    main()
