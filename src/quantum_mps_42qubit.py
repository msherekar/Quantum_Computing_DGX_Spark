"""Run a 42-qubit tensor-network (MPS) simulation with CUDA-Q.
Implements section 4.1-4.2 from the DGX Spark guide."""

import argparse, time
import cudaq

DEFAULT_QUBITS = 42
DEFAULT_SHOTS = 1000
DEFAULT_TARGET = "tensornet-mps"


@cudaq.kernel
def large_mps_circuit():
    """42-qubit circuit with nearest-neighbor entanglement."""
    qubits = cudaq.qvector(DEFAULT_QUBITS)
    for i in range(DEFAULT_QUBITS):
        h(qubits[i])
        if i > 0:
            x.ctrl(qubits[i - 1], qubits[i])
    mz(qubits)


def run_simulation(target: str, shots: int) -> tuple[float, cudaq.SampleResult]:
    """Execute MPS kernel and return elapsed time and result."""
    cudaq.set_target(target)
    start = time.time()
    result = cudaq.sample(large_mps_circuit, shots_count=shots)
    elapsed = time.time() - start
    return elapsed, result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate a 42-qubit MPS circuit.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="CUDA-Q backend target")
    parser.add_argument("--shots", type=int, default=DEFAULT_SHOTS, help="Measurement shots")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Running 42-qubit MPS simulation (tensor-network backend)...")
    print("Best for nearest-neighbor / low-entanglement circuits.\n")
    elapsed, result = run_simulation(args.target, args.shots)
    print(f"Simulation completed in {elapsed:.2f} seconds")
    print("\nResults:")
    result.dump()


if __name__ == "__main__":
    main()
