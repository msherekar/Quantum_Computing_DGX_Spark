"""Run a 15-qubit GHZ circuit simulation with CUDA-Q.
This script mirrors section 2.2-2.3 of the DGX Spark guide."""

import argparse, time
import cudaq

DEFAULT_QUBITS = 15
DEFAULT_SHOTS = 10_000
DEFAULT_TARGET = "nvidia"


@cudaq.kernel
def ghz_15_qubit():
    """Create and measure a 15-qubit GHZ state."""
    qubits = cudaq.qvector(DEFAULT_QUBITS)
    h(qubits[0])
    for i in range(DEFAULT_QUBITS - 1):
        x.ctrl(qubits[i], qubits[i + 1])
    mz(qubits)


def run_simulation(target: str, shots: int) -> tuple[float, cudaq.SampleResult]:
    """Execute GHZ kernel and return elapsed time and result."""
    cudaq.set_target(target)
    start = time.time()
    result = cudaq.sample(ghz_15_qubit, shots_count=shots)
    elapsed = time.time() - start
    return elapsed, result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate a 15-qubit GHZ circuit.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="CUDA-Q backend target")
    parser.add_argument("--shots", type=int, default=DEFAULT_SHOTS, help="Measurement shots")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Simulating 15-qubit GHZ circuit...")
    elapsed, result = run_simulation(args.target, args.shots)
    print(f"Simulation completed in {elapsed:.2f} seconds")
    print("\nResults:")
    result.dump()


if __name__ == "__main__":
    main()
