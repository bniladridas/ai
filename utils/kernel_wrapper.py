import ctypes
from pathlib import Path

# Load the C library (assuming compiled to benchmark.so)
lib_path = Path(__file__).parent.parent / "kernel" / "benchmark.so"
if lib_path.exists():
    kernel_lib = ctypes.CDLL(str(lib_path))
    kernel_lib.get_elapsed_time.restype = ctypes.c_double
else:
    kernel_lib = None


def get_elapsed_time():
    """Get elapsed time from C kernel."""
    if kernel_lib:
        return kernel_lib.get_elapsed_time()
    else:
        return 0.0  # Fallback


def reset_timer():
    """Reset the timer (placeholder)."""
    pass
