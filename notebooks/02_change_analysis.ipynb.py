import grass.script as gs
import pandas as pd
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import os
import re

# MOLCA color mapping
molca_colors = {
    5: '#966400',  # Shrubland
    7: '#FFB432',  # Grassland
    8: '#FFFF64',  # Cropland
    9: '#00A884',  # Wetland
    11: '#FFDCD2',  # Lichens & Mosses
    12: '#FFF5D7',  # Bareland
    13: '#C31400',  # Built-up
    15: '#0046C8',  # Water
    16: '#FFFFFF',  # Ice/Snow
    20: '#006400'  # Forest
}

# Get all landcover rasters and extract years
raster_list = gs.list_strings('raster', pattern='landcover_*')
years = sorted(list(set(
    int(re.search(r'landcover_(\d+)', r).group(1))
    for r in raster_list
    if re.match(r'landcover_\d+', r)
)))

# Create output directory
os.makedirs('landcover_stats', exist_ok=True)

# Process all years
all_stats = []
for year in tqdm(years, desc='Processing years'):
    raster_name = f"landcover_{year}"

    # Check if raster exists with or without @PERMANENT
    if raster_name not in raster_list:
        raster_name = f"{raster_name}@PERMANENT"
        if raster_name not in raster_list:
            print(f"Skipping {year} - raster not found")
            continue

    try:
        # Get pixel counts
        stats = gs.read_command('r.stats', input=raster_name, flags='cn', quiet=True).strip()

        # Parse results
        data = []
        for line in stats.split('\n'):
            if line.strip():
                try:
                    code, count = line.split()
                    data.append({
                        'year': year,
                        'code': int(code),
                        'count': int(count)
                    })
                except ValueError as e:
                    print(f"Error parsing line '{line}' for {year}: {e}")
                    continue

        # Create DataFrame
        df = pd.DataFrame(data)
        df['class'] = df['code'].map({
            5: 'Shrubland',
            7: 'Grassland',
            8: 'Cropland',
            9: 'Wetland',
            11: 'Lichens & Mosses',
            12: 'Bareland',
            13: 'Built-up',
            15: 'Water',
            16: 'Ice/Snow',
            20: 'Forest'
        })

        # Calculate metrics
        total_pixels = df['count'].sum()
        df['area_km2'] = df['count'] * 0.09  # 300m resolution (0.3km × 0.3km)
        df['pct'] = df['count'] / total_pixels * 100
        all_stats.append(df)

        # Save yearly stats
        df.to_csv(f'landcover_stats/{year}.csv', index=False)

    except Exception as e:
        print(f"Error processing {year}: {e}")
        continue

# Combine all years if data was processed
if all_stats:
    full_df = pd.concat(all_stats)
    full_df.to_csv('landcover_stats/complete_stats.csv', index=False)

    # Create visualization
    plt.figure(figsize=(16, 10), dpi=150)
    pivot_df = full_df.pivot(index='year', columns='class', values='pct')
    pivot_df.plot(kind='area',
                  color=[molca_colors.get(k, '#000000') for k in [5, 7, 8, 9, 11, 12, 13, 15, 16, 20]],
                  stacked=True,
                  alpha=0.8)

    plt.title('Land Cover Change (1992-2022)', fontsize=16)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xlabel('Year', fontsize=12)
    plt.legend(title='Land Cover Class', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('landcover_stats/trends.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Display sample table
    if len(years) > 0:
        sample_year = years[-1]
        sample_df = full_df[full_df['year'] == sample_year]
        print(f"\nSample Statistics for {sample_year}:")
        display(sample_df[['class', 'count', 'area_km2', 'pct']]
                .sort_values('pct', ascending=False)
                .style.format({'count': '{:,}', 'area_km2': '{:,.1f}', 'pct': '{:.2f}%'}))
else:
    print("No valid data was processed.")



