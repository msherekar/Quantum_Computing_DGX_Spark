"""Run a 15-qubit Quantum Fourier Transform simulation with CUDA-Q.
This script mirrors section 2.4 of the DGX Spark guide."""

import argparse, time
import numpy as np
import cudaq

DEFAULT_QUBITS = 15
DEFAULT_SHOTS = 5_000
DEFAULT_TARGET = "nvidia"


@cudaq.kernel
def qft_15_qubit():
    """Build and measure a 15-qubit QFT-style circuit."""
    qubits = cudaq.qvector(DEFAULT_QUBITS)
    for i in range(3):
        x(qubits[i])
    for j in range(DEFAULT_QUBITS):
        h(qubits[j])
        for k in range(j + 1, DEFAULT_QUBITS):
            angle = np.pi / (2 ** (k - j))
            r1.ctrl(angle, qubits[k], qubits[j])
    for i in range(DEFAULT_QUBITS // 2):
        swap(qubits[i], qubits[DEFAULT_QUBITS - 1 - i])
    mz(qubits)


def run_simulation(target: str, shots: int) -> tuple[float, cudaq.SampleResult]:
    """Execute QFT kernel and return elapsed time and result."""
    cudaq.set_target(target)
    start = time.time()
    result = cudaq.sample(qft_15_qubit, shots_count=shots)
    elapsed = time.time() - start
    return elapsed, result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate a 15-qubit QFT circuit.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="CUDA-Q backend target")
    parser.add_argument("--shots", type=int, default=DEFAULT_SHOTS, help="Measurement shots")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Simulating 15-qubit QFT circuit...")
    elapsed, result = run_simulation(args.target, args.shots)
    print(f"Simulation completed in {elapsed:.2f} seconds")
    print("\nResults:")
    result.dump()


if __name__ == "__main__":
    main()
