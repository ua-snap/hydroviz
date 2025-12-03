#!/usr/bin/env python3
"""
Quality control script to verify combined NetCDF files against source files.

This script randomly samples coordinate combinations from the combined file
and verifies that the values match the corresponding source files.

Usage:
    python qc_combined_netcdf.py <combined_file> <source_dir> [--samples N]
"""

import sys
import argparse
import random
from pathlib import Path
import xarray as xr
import numpy as np


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="QC combined NetCDF file against source files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "combined_file",
        type=str,
        help="Path to the combined NetCDF file"
    )
    
    parser.add_argument(
        "source_dir",
        type=str,
        help="Directory containing source NetCDF files"
    )
    
    parser.add_argument(
        "--samples",
        type=int,
        default=10,
        help="Number of random samples to test"
    )
    
    return parser.parse_args()


def find_source_file(landcover, model, scenario, variant, source_dir):
    """Find the source NetCDF file for given parameters."""
    # The combined file has lowercase model names, but source files may have mixed case
    # Try different case variations to find the actual file
    
    pattern_base = f"{landcover}_*_{scenario}_{variant}_doy_mmm_by_era.nc"
    
    # First try exact match (lowercase)
    filename = f"{landcover}_{model}_{scenario}_{variant}_doy_mmm_by_era.nc"
    source_path = source_dir / filename
    
    if source_path.exists():
        return source_path
    
    # If not found, search for files matching the pattern but with different model case
    matching_files = list(source_dir.glob(pattern_base))
    
    for file_path in matching_files:
        # Extract model name from the actual filename
        parts = file_path.stem.split('_')
        if len(parts) >= 4:
            file_model = parts[1]  # Second part should be the model
            # Check if this matches our model (case insensitive)
            if file_model.lower() == model.lower():
                print(f"Found file with different case: {file_path.name} (expected: {filename})")
                return file_path
    
    print(f"WARNING: Source file not found for {landcover}_{model}_{scenario}_{variant}")
    print(f"  Tried: {filename}")
    print(f"  Available files matching pattern: {[f.name for f in matching_files]}")
    return None


def get_random_sample(combined_ds, n_samples=10):
    """Generate random coordinate combinations from the combined dataset."""
    samples = []
    
    # Get available coordinate values
    landcovers = list(combined_ds.landcover.values)
    models = list(combined_ds.model.values)
    scenarios = list(combined_ds.scenario.values)
    eras = list(combined_ds.era.values)
    doys = list(combined_ds.doy.values)
    stream_ids = list(combined_ds.stream_id.values)
    
    print(f"Available coordinates:")
    print(f"  Landcovers: {landcovers}")
    print(f"  Models: {len(models)} total")
    print(f"  Scenarios: {scenarios}")
    print(f"  Eras: {eras}")
    print(f"  DOYs: {len(doys)} total")
    print(f"  Stream IDs: {len(stream_ids)} total")
    print()
    
    # Find valid scenario-era combinations by checking what actually exists in the data
    # Also apply logical constraints: historical only with 1976-2005, future scenarios only with future eras
    valid_scenario_era_combos = []
    for scenario in scenarios:
        for era in eras:
            # Apply logical constraints
            is_historical = scenario.lower() == 'historical'
            is_historical_era = '1976-2005' in str(era)
            
            # Skip invalid combinations
            if is_historical and not is_historical_era:
                continue  # Historical only goes with 1976-2005
            if not is_historical and is_historical_era:
                continue  # Future scenarios don't go with historical era
            
            # Check if this combination exists in the dataset
            try:
                subset = combined_ds.sel(scenario=scenario, era=era)
                if subset.sizes['model'] > 0:  # Has at least one model for this combo
                    valid_scenario_era_combos.append((scenario, era))
            except:
                continue
    
    print(f"Valid scenario-era combinations: {valid_scenario_era_combos}")
    print()
    
    if not valid_scenario_era_combos:
        raise ValueError("No valid scenario-era combinations found!")
    
    for i in range(n_samples):
        # Pick a valid scenario-era combination
        scenario, era = random.choice(valid_scenario_era_combos)
        
        sample = {
            'landcover': random.choice(landcovers),
            'model': random.choice(models),
            'scenario': scenario,
            'era': era,
            'doy': random.choice(doys),
            'stream_id': random.choice(stream_ids)
        }
        samples.append(sample)
    
    return samples


def compare_values(combined_ds, source_ds, sample):
    """Compare values between combined and source datasets for a sample."""
    try:
        # Get values from combined dataset
        combined_min = combined_ds['doy_min'].sel(**sample).values
        combined_mean = combined_ds['doy_mean'].sel(**sample).values
        combined_max = combined_ds['doy_max'].sel(**sample).values
        
        # Check if all combined values are NaN (indicating no source data)
        all_nan = np.isnan(combined_min) and np.isnan(combined_mean) and np.isnan(combined_max)
        
        if all_nan:
            # If combined values are all NaN, there should be no source file
            # This is expected for missing scenario/model combinations
            return {
                'all_match': True,
                'min_match': True,
                'mean_match': True, 
                'max_match': True,
                'combined_values': (combined_min, combined_mean, combined_max),
                'source_values': None,
                'note': 'Combined values all NaN - no source data expected (PASS)'
            }
        
        # Get values from source dataset
        # Note: source dataset has single values for model, scenario, landcover
        source_sample = {
            'era': sample['era'],
            'doy': sample['doy'],
            'stream_id': sample['stream_id']
        }
        
        source_min = source_ds['doy_min'].sel(**source_sample).values
        source_mean = source_ds['doy_mean'].sel(**source_sample).values
        source_max = source_ds['doy_max'].sel(**source_sample).values
        
        # Check if values are equal (handle NaN values)
        def values_equal(a, b, tolerance=1e-6):
            if np.isnan(a) and np.isnan(b):
                return True
            elif np.isnan(a) or np.isnan(b):
                return False
            else:
                return abs(a - b) < tolerance
        
        min_match = values_equal(combined_min, source_min)
        mean_match = values_equal(combined_mean, source_mean)
        max_match = values_equal(combined_max, source_max)
        
        return {
            'min_match': min_match,
            'mean_match': mean_match,
            'max_match': max_match,
            'combined_values': (combined_min, combined_mean, combined_max),
            'source_values': (source_min, source_mean, source_max)
        }
        
    except Exception as e:
        print(f"ERROR comparing values: {e}")
        print(f"DIAGNOSTIC INFO:")
        print(f"  Combined dataset dimensions: {combined_ds.dims}")
        print(f"  Source dataset dimensions: {source_ds.dims}")
        print(f"  Combined eras: {list(combined_ds.era.values)}")
        print(f"  Source eras: {list(source_ds.era.values)}")
        print(f"  Trying to select from source with: {source_sample}")
        return None


def main():
    """Main QC function."""
    args = parse_arguments()
    
    print("=== NetCDF Combined File Quality Control ===\n")
    
    # File paths from command line arguments
    combined_file = Path(args.combined_file)
    source_dir = Path(args.source_dir)
    n_samples = args.samples
    
    # Check if files/directories exist
    if not combined_file.exists():
        print(f"ERROR: Combined file not found: {combined_file}")
        sys.exit(1)
        
    if not source_dir.exists():
        print(f"ERROR: Source directory not found: {source_dir}")
        sys.exit(1)
    
    print(f"Combined file: {combined_file}")
    print(f"Source directory: {source_dir}")
    print(f"Number of samples: {n_samples}")
    print()
    
    # Open combined dataset
    print("Opening combined dataset...")
    try:
        combined_ds = xr.open_dataset(combined_file)
        print(f"Combined dataset dimensions: {combined_ds.dims}")
        print(f"Combined dataset variables: {list(combined_ds.data_vars)}")
        print()
    except Exception as e:
        print(f"ERROR opening combined file: {e}")
        sys.exit(1)
    
    # Generate random samples
    print("Generating random samples...")
    samples = get_random_sample(combined_ds, n_samples=n_samples)
    
    # Test each sample
    passed = 0
    failed = 0
    
    for i, sample in enumerate(samples, 1):
        print(f"--- Sample {i}/{n_samples} ---")
        print(f"Coordinates: {sample}")
        
        # First check if this sample should have all NaN values
        # Get a quick peek at the combined data to see if it's all NaN
        try:
            combined_min_peek = combined_ds['doy_min'].sel(**sample).values
            combined_mean_peek = combined_ds['doy_mean'].sel(**sample).values
            combined_max_peek = combined_ds['doy_max'].sel(**sample).values
            all_nan = np.isnan(combined_min_peek) and np.isnan(combined_mean_peek) and np.isnan(combined_max_peek)
        except:
            all_nan = False
        
        # Find source file
        # Use fixed variant for now (all files seem to use r1i1p1)
        variant = "r1i1p1"
        source_file = find_source_file(
            sample['landcover'], 
            sample['model'], 
            sample['scenario'], 
            variant,
            source_dir
        )
        
        if source_file is None:
            if all_nan:
                print("PASSED: Combined values all NaN and no source file exists (expected - scenario is likely missing for this model)\n")
                passed += 1
                continue
            else:
                print("FAILED: Source file not found but combined values are not NaN\n")
                failed += 1
                continue
        
        if all_nan:
            print("FAILED: Source file exists but combined values are all NaN\n") 
            failed += 1
            continue
            
        print(f"Source file: {source_file.name}")
        
        # Open source dataset
        try:
            source_ds = xr.open_dataset(source_file)
        except Exception as e:
            print(f"FAILED: Could not open source file: {e}\n")
            failed += 1
            continue
        
        # Compare values
        result = compare_values(combined_ds, source_ds, sample)
        
        if result is None:
            print("FAILED: Could not compare values\n")
            failed += 1
            source_ds.close()
            continue
        
        # Check results
        all_match = result['min_match'] and result['mean_match'] and result['max_match']
        
        if all_match:
            print("PASSED: All values match")
            passed += 1
        else:
            print("FAILED: Values don't match")
            print(f"  Combined (min, mean, max): {result['combined_values']}")
            print(f"  Source   (min, mean, max): {result['source_values']}")
            print(f"  Matches: min={result['min_match']}, mean={result['mean_match']}, max={result['max_match']}")
            failed += 1
        
        source_ds.close()
        print()
    
    # Summary
    print("=== QC SUMMARY ===")
    print(f"Total samples: {len(samples)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed/len(samples)*100:.1f}%")
    
    if failed == 0:
        print("🎉 All QC checks passed! Combined file appears correct.")
        sys.exit(0)
    else:
        print(f"❌ {failed} QC checks failed. There may be issues with the combined file.")
        sys.exit(1)
    
    # Clean up
    combined_ds.close()


if __name__ == "__main__":
    main()