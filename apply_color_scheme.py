import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import extract_spectral_band
import extract_coefficients
import radiance_to_reflectance
import rasterio
import numpy as np

"""
The reflectance values will range from 0 to 1. You want to use a diverging color scheme to visualize the data,
and you want to center the colorbar at a defined midpoint. The class below allows you to normalize the colorbar.
"""

class MidpointNormalize(colors.Normalize):
    """
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)
    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    Credit: Joe Kington, http://chris35wills.github.io/matplotlib_diverging_colorbar/
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

def colorize (reflectances):
    for key,reflectance in reflectances.items():
        # Set min/max values from reflectance range for image (excluding NAN)
        min=np.nanmin(reflectance['band_nir_reflectance'])
        max=np.nanmax(reflectance['band_nir_reflectance'])
        mid=0.20

        fig = plt.figure(figsize=(20,10))
        ax = fig.add_subplot(111)

        # diverging color scheme chosen from https://matplotlib.org/users/colormaps.html
        # note that appending '_r' to the color scheme name reverses it!
        cmap = plt.cm.get_cmap('RdGy_r')

        cax = ax.imshow(reflectance['band_nir_reflectance'], cmap=cmap, clim=(min, max), norm=MidpointNormalize(midpoint=mid,vmin=min, vmax=max))

        ax.axis('off')
        ax.set_title('NIR Reflectance', fontsize=18, fontweight='bold')

        cbar = fig.colorbar(cax, orientation='horizontal', shrink=0.65)

        fig.savefig("images/" + key + "-fig.png", dpi=200, bbox_inches='tight', pad_inches=0.7)

        #plt.show()

spectral_bands_for_assets = extract_spectral_band.extract()
coefficients_for_assets = extract_coefficients.extract()

print spectral_bands_for_assets
print coefficients_for_assets

for spectral_bands in spectral_bands_for_assets:
    print spectral_bands.keys()
    for coefficients in coefficients_for_assets:
        print coefficients.keys()
        if coefficients.keys()[0] == spectral_bands.keys()[0]:
            reflectances = radiance_to_reflectance.convert(spectral_bands, coefficients)

            colorize(reflectances)
            break
            # save_rasters (reflectances)

