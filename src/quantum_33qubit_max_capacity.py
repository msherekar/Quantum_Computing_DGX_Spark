"""Run a 33-qubit maximum-capacity GHZ-style simulation with CUDA-Q.
Implements section 3.2 from the DGX Spark guide with memory safety checks."""

import argparse, time
import psutil, cudaq

DEFAULT_QUBITS = 33
DEFAULT_SHOTS = 1000
DEFAULT_TARGET = "nvidia"
STATE_VECTOR_BYTES = 16


@cudaq.kernel
def max_capacity_circuit():
    qubits = cudaq.qvector(DEFAULT_QUBITS)
    h(qubits[0])
    for i in range(DEFAULT_QUBITS - 1):
        x.ctrl(qubits[i], qubits[i + 1])
    mz(qubits)


def estimate_required_gb(num_qubits: int) -> float:
    return ((2 ** num_qubits) * STATE_VECTOR_BYTES) / 1e9


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate a 33-qubit max-capacity circuit.")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="CUDA-Q backend target")
    parser.add_argument("--shots", type=int, default=DEFAULT_SHOTS, help="Measurement shots")
    parser.add_argument("--force", action="store_true", help="Run even when memory appears tight")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    available_gb = psutil.virtual_memory().available / 1e9
    required_gb = estimate_required_gb(DEFAULT_QUBITS)
    print("WARNING: This will use ~128GB of memory")
    print(f"Estimated required memory: {required_gb:.1f} GB")
    print(f"Available memory: {available_gb:.1f} GB\n")
    if available_gb < required_gb * 1.05 and not args.force:
        print("Aborting: available memory is below recommended threshold.")
        print("Re-run with --force to attempt anyway.")
        return

    cudaq.set_target(args.target)
    print("Starting 33-qubit simulation...")
    start = time.time()
    result = cudaq.sample(max_capacity_circuit, shots_count=args.shots)
    end = time.time()
    print(f"\nCompleted in {end - start:.2f} seconds")
    print(f"Current used memory: {psutil.virtual_memory().used / 1e9:.1f} GB")
    print("\nResults:")
    result.dump()


if __name__ == "__main__":
    main()
