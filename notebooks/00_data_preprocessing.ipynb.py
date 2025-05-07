import os
import xarray as xr
import rioxarray
from rasterio.enums import Resampling
import numpy as np
from pyproj import CRS

# === Define directories ===
input_dir = "/Users/ghulamabbaszafari/Downloads/rest/reclassification/OneDrive_1_04-04-2025/reclass_data/ESA_CCI_LC_reclass_clean"
output_dir = "/Users/ghulamabbaszafari/Downloads/rest/reclassification/OneDrive_1_04-04-2025/reclass_data/ESA_CCI_LC_reprojected_3035"
os.makedirs(output_dir, exist_ok=True)

# === Target CRS ===
target_crs = "EPSG:3035"

# === Reprojection parameters ===
target_resolution = 300  # meters
resampling_method = Resampling.nearest

# === Process each NetCDF file ===
for filename in os.listdir(input_dir):
    if filename.endswith(".nc"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"reprojected_3035_{filename}")

        print(f"\n🔍 Processing: {filename}")

        # Open the dataset
        ds = xr.open_dataset(input_path)

        # Select the land cover variable and set its CRS
        lc = ds['lccs_class'].isel(time=0)
        lc.rio.write_crs("EPSG:4326", inplace=True)

        # Set appropriate nodata value
        flag_values = lc.attrs.get('flag_values', [])
        nodata_value = 255 if 0 in flag_values else 0

        # Remove any existing _FillValue from attributes
        lc.attrs.pop('_FillValue', None)

        # Reproject to EPSG:3035
        print("Reprojecting to EPSG:3035...")
        lc_reprojected = lc.rio.reproject(
            target_crs,
            resolution=target_resolution,
            resampling=resampling_method,
            nodata=nodata_value
        )

        # Ensure proper CRS metadata
        lc_reprojected.rio.write_crs(target_crs, inplace=True)
        lc_reprojected.attrs['grid_mapping'] = 'spatial_ref'

        # Create new dataset with reprojected data
        ds_reprojected = xr.Dataset()
        ds_reprojected['lccs_class'] = lc_reprojected.expand_dims('time')

        # Add CRS variable with CF-compliant attributes
        crs_attrs = CRS.from_epsg(3035).to_cf()
        ds_reprojected['spatial_ref'] = xr.DataArray(0, attrs=crs_attrs)

        # Copy and update attributes
        ds_reprojected.attrs = ds.attrs
        ds_reprojected['lccs_class'].attrs = ds['lccs_class'].attrs

        # Clean up attributes
        ds_reprojected['lccs_class'].attrs.pop('_FillValue', None)
        ds_reprojected['lccs_class'].attrs.pop('grid_mapping', None)

        # Update metadata
        ds_reprojected.attrs['spatial_ref'] = target_crs
        ds_reprojected.attrs['spatial_resolution'] = f"{target_resolution}m"
        ds_reprojected.attrs['history'] = ds.attrs.get('history', '') + \
                                          f"; Reprojected to {target_crs} with {resampling_method.name} resampling"

        # Prepare encoding
        encoding = {
            'lccs_class': {
                'zlib': True,
                'complevel': 5,
                '_FillValue': nodata_value,
                'dtype': 'uint8'
            },
            'spatial_ref': {
                'zlib': True,
                'complevel': 5
            }
        }

        # Save the reprojected dataset
        print(f"Saving to: {output_path}")
        ds_reprojected.to_netcdf(output_path, encoding=encoding)

        print(f"✅ Successfully reprojected {filename} to EPSG:3035")

print("\nAll files processed successfully!")


# === Verification function ===
def verify_reprojection(file_path):
    print(f"\n🔍 Verifying: {os.path.basename(file_path)}")
    ds = xr.open_dataset(file_path)

    try:
        print("CRS from rioxarray:", ds['lccs_class'].rio.crs)
    except Exception as e:
        print(f"CRS check error: {e}")

    print("Grid mapping:", ds['lccs_class'].attrs.get('grid_mapping', 'Not found'))
    print("X coordinates (first 5):", ds['lccs_class'].x.values[:5])
    print("Y coordinates (first 5):", ds['lccs_class'].y.values[:5])

    if 'spatial_ref' in ds:
        print("Spatial ref exists with attributes:", list(ds['spatial_ref'].attrs.keys()))
    else:
        print("No spatial_ref variable found")


# === Example verification ===
output_files = [f for f in os.listdir(output_dir) if f.endswith(".nc")]
if output_files:
    sample_file = os.path.join(output_dir, output_files[0])
    verify_reprojection(sample_file)
else:
    print("No files found in output directory for verification")






