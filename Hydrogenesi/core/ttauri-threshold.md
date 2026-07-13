# T Tauri Gate — Physical Threshold

## The Problem With The Current Code

The shell_cleared parameter is a continuous dial from 0 to 1.
That is not physical. A threshold needs a specific condition.

## The Physical Condition

The CNO cycle split requires the outer envelope mass to drop
below a critical fraction of total stellar mass.

Standard T Tauri mass loss rates: 1e-8 to 1e-6 solar masses per year
T Tauri phase duration: 1 to 10 million years
Total mass shed: 0.01 to 0.1 solar masses

The threshold condition:

M_envelope / M_total < 0.01

When the envelope drops below 1% of total mass, the CNO cycle
has access to the core temperature gradient required for bilateral
operation. This is physically motivated by the opacity drop
at the envelope boundary.

## Testable Prediction

Stars that exit T Tauri phase should show:
1. Luminosity increase above standard models at threshold crossing
2. CNO isotope ratio shift at envelope clearing
3. Rotation rate change as angular momentum redistributes

These are checkable against existing T Tauri survey data.

## Implementation

Replace shell_cleared continuous parameter with:

def ttauri_threshold(M_envelope, M_total):
    fraction = M_envelope / M_total
    if fraction > 0.01:
        return "SHEDDING", False
    elif fraction > 0.001:
        return "CLEARING", False
    else:
        return "STABILIZED", True

Three discrete states. One physical threshold. Testable.
