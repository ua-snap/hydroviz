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
    # Construct expected filename
    filename = f"{landcover}_{model}_{scenario}_{variant}_doy_mmm_by_era.nc"
    source_path = source_dir / filename
    
    if source_path.exists():
        return source_path
    else:
        print(f"WARNING: Source file not found: {filename}")
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
    print(f"  Models: {len(models)} total: {models[:3]}...")
    print(f"  Scenarios: {scenarios}")
    print(f"  Eras: {eras}")
    print(f"  DOYs: {len(doys)} (range: {min(doys)}-{max(doys)})")
    print(f"  Stream IDs: {len(stream_ids)} total")
    print()
    
    for i in range(n_samples):
        sample = {
            'landcover': random.choice(landcovers),
            'model': random.choice(models),
            'scenario': random.choice(scenarios),
            'era': random.choice(eras),
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
            print("FAILED: Source file not found\n")
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