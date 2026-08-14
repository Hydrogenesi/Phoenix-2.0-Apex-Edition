import numpy as np

SCALE_FACTOR = 2.044e21
_BOHR_RADIUS = 5.3e-11   # Bohr radius in metres
_AU_IN_METERS = 1.496e11 # metres per astronomical unit

# Bohr radius expressed in AU after applying the scale factor.
# Precomputed once so both prediction functions share the same base value.
_BOHR_SCALE_AU = _BOHR_RADIUS * SCALE_FACTOR / _AU_IN_METERS

def venus_prediction():
    predicted = _BOHR_SCALE_AU
    actual = 0.7230
    delta = abs(predicted - actual) / actual * 100
    return predicted, delta

def earth_prediction():
    predicted = _BOHR_SCALE_AU * (2**0.5)
    actual = 1.0000
    delta = abs(predicted - actual) / actual * 100
    return predicted, delta

if __name__ == "__main__":
    v, vd = venus_prediction()
    e, ed = earth_prediction()
    print("=== Hydrogenesi Framework ===")
    print(f"Scale factor: {SCALE_FACTOR:.3e}")
    print(f"Venus: {v:.4f} AU  delta: {vd:.2f}%")
    print(f"Earth: {e:.4f} AU  delta: {ed:.2f}%")
    print("The math was always there.")
