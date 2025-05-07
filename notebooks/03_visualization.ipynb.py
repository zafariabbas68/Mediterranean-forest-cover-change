import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the reprojected file
file_path = "/Users/ghulamabbaszafari/Downloads/rest/reclassification/OneDrive_1_04-04-2025/reclass_data/ESA_CCI_LC_reprojected_3035/reprojected_3035_C3S-LC-L4-LCCS-Map-300m-P1Y-2016-v2.1.1.area-subset.48.40.30.-10_reclass_clean.nc"
ds = xr.open_dataset(file_path)
lc = ds['lccs_class'].isel(time=0)

# Define MOLCA color mapping
molca_code_to_color = {
    5: '#966400',    # Shrubland
    7: '#FFB432',    # Grassland
    8: '#FFFF64',    # Cropland
    9: '#00A884',    # Wetland
    11: '#FFDCD2',   # Lichens & Mosses
    12: '#FFF5D7',   # Bareland
    13: '#C31400',   # Built-up
    15: '#0046C8',   # Water
    16: '#FFFFFF',   # Ice/Snow
    20: '#006400'    # Forest
}

# Create RGB image from classified data
rgb_image = np.zeros((*lc.shape, 3), dtype=np.float32)
for code, color in molca_code_to_color.items():
    mask = lc.values == code
    rgb_image[mask] = plt.cm.colors.to_rgb(color)

# Create figure with LAEA Europe projection
fig = plt.figure(figsize=(16, 12))
ax = plt.axes(projection=ccrs.epsg(3035))

# Calculate extent in LAEA coordinates
extent = [lc.x.min(), lc.x.max(), lc.y.min(), lc.y.max()]

# Plot using pcolormesh instead of imshow for proper projection handling
ax.pcolormesh(lc.x, lc.y, lc.values,
             transform=ccrs.epsg(3035),
             cmap=plt.cm.colors.ListedColormap(list(molca_code_to_color.values())),
             norm=plt.cm.colors.BoundaryNorm(list(molca_code_to_color.keys()) + [220], len(molca_code_to_color)))

# Add map features
ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.5)
ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':', linewidth=0.5)
ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)

# Set title
plt.title('ESA CCI Land Cover 2016 (Reprojected to EPSG:3035)', fontsize=14, pad=20)

# Create legend
legend_elements = [plt.Line2D([0], [0], marker='s', color='w', label='Shrubland',
                   markerfacecolor='#966400', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Grassland',
                   markerfacecolor='#FFB432', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Cropland',
                   markerfacecolor='#FFFF64', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Wetland',
                   markerfacecolor='#00A884', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Lichens & Mosses',
                   markerfacecolor='#FFDCD2', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Bareland',
                   markerfacecolor='#FFF5D7', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Built-up',
                   markerfacecolor='#C31400', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Water',
                   markerfacecolor='#0046C8', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Ice/Snow',
                   markerfacecolor='#FFFFFF', markersize=10),
                  plt.Line2D([0], [0], marker='s', color='w', label='Forest',
                   markerfacecolor='#006400', markersize=10)]

ax.legend(handles=legend_elements,
         loc='lower center',
         bbox_to_anchor=(0.5, -0.1),
         ncol=5,
         frameon=True,
         title='Land Cover Classes')

plt.tight_layout()
plt.show()


