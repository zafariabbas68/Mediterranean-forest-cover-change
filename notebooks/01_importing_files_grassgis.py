import os
import grass.script as gs


def import_landcover_data():
    """Import all NetCDF files with standardized naming (landcover_YYYY)"""
    directory_path = '/Users/ghulamabbaszafari/Downloads/rest/reclassification/OneDrive_1_04-04-2025/reclass_data/ESA_CCI_LC_reprojected_3035'
    nc_files = [f for f in os.listdir(directory_path) if f.endswith('.nc') and not f.endswith('.aux.xml')]
    nc_files.sort()

    raster_dict = {}
    failed_imports = []

    for nc_file in nc_files:
        try:
            # Extract year from filename (handles both ESA_CCI and C3S formats)
            if "ESACCI" in nc_file:
                year = nc_file.split('-P1Y-')[1].split('-')[0]  # ESACCI files
            elif "C3S" in nc_file:
                year = nc_file.split('-P1Y-')[1].split('-')[0]  # C3S files
            else:
                print(f"Skipping {nc_file} (unknown format)")
                continue

            # Define GRASS raster name (e.g., "landcover_1992")
            raster_name = f"landcover_{year}"
            filepath = os.path.join(directory_path, nc_file)

            print(f"Importing {nc_file} as {raster_name}...")

            # Import using r.external (no reprojection, faster)
            gs.run_command('r.external',
                           input=filepath,
                           output=raster_name,
                           flags='o',  # Override projection check
                           overwrite=True)

            raster_dict[year] = raster_name
            print(f"Imported: {raster_name}")

        except Exception as e:
            print(f"FAILED: {nc_file} ({str(e)})")
            failed_imports.append(nc_file)

    # Print summary
    if failed_imports:
        print("\nFailed imports:")
        for f in failed_imports:
            print(f" - {f}")
    else:
        print("\nAll files imported successfully!")

    return raster_dict


def main():
    print("=== GRASS GIS NetCDF Importer ===")
    raster_dict = import_landcover_data()

    # Set computational region to the first imported raster
    if raster_dict:
        base_raster = next(iter(raster_dict.values()))
        print(f"\nSetting region to {base_raster}...")
        gs.run_command('g.region', raster=base_raster)
        print("Done! Use `g.list type=raster` to verify.")
    else:
        print("No rasters imported. Check errors above.")


if __name__ == "__main__":
    main()



