import numpy as np

def simulate_mass_spectrum(chemicals, isolation_window, mz_tol, rt_tol):
    # Calculate the number of points in the isolation window
    num_points = int(1000 * isolation_window)
    
    # Initialize mass spectrum with zeros
    mass_spectrum = np.zeros(num_points)
    
    for chemical in chemicals:
        precursor_mz = chemical['mz']
        precursor_rt = chemical['rt']
        precursor_intensity = chemical['intensity']
        
        # Select precursor ions based on isolation window, mass tolerance, and retention time tolerance
        if (precursor_mz - mz_tol / 2 <= precursor_mz <= precursor_mz + mz_tol / 2) and \
           (precursor_rt - rt_tol / 2 <= precursor_rt <= precursor_rt + rt_tol / 2):
            
            # Calculate the starting index for the precursor ion in the mass spectrum
            mz_shift = int(1000 * (precursor_mz - (precursor_mz - isolation_window / 2)))
            
            # Generate simulated intensity values for the selected precursor ions
            intensity_values = np.random.normal(precursor_intensity, precursor_intensity / 10, size=num_points)
            
            # Ensure that the intensity values do not exceed the maximum intensity of the mass spectrum
            max_index = min(mz_shift + len(intensity_values), len(mass_spectrum))
            mass_spectrum[mz_shift:max_index] += intensity_values[:max_index - mz_shift]
    
    return mass_spectrum

def test_simulate_mass_spectrum():
    # Test case 1: Single chemical within isolation window
    chemicals = [{'mz': 100, 'rt': 500, 'intensity': 10000}]
    isolation_window = 1
    mz_tol = 10
    rt_tol = 100
    expected_spectrum_length = int(1000 * isolation_window)
    spectrum = simulate_mass_spectrum(chemicals, isolation_window, mz_tol, rt_tol)
    assert len(spectrum) == expected_spectrum_length, "Test case 1 failed"
    
    # Test case 2: No chemicals within isolation window
    chemicals = [{'mz': 200, 'rt': 500, 'intensity': 10000}]
    isolation_window = 1
    mz_tol = 10
    rt_tol = 100
    expected_spectrum_length = 0
    spectrum = simulate_mass_spectrum(chemicals, isolation_window, mz_tol, rt_tol)
    assert len(spectrum) == expected_spectrum_length, "Test case 2 failed"

def main():
    # List of chemicals with known m/z, retention time, and intensity values
    chemicals = [
        {'mz': 123.45, 'rt': 500, 'intensity': 10000},
        {'mz': 234.56, 'rt': 600, 'intensity': 5000},
        # Add more chemicals as needed
    ]

    # Parameters for precursor ion selection
    isolation_window = 0.7
    mz_tol = 10
    rt_tol = 120

    # Generate simulated mass spectrum
    mass_spectrum = simulate_mass_spectrum(chemicals, isolation_window, mz_tol, rt_tol)
    print(mass_spectrum)

if __name__ == "__main__":
    test_simulate_mass_spectrum()
    main()