import numpy as np


# Multiply the Digital Number (DN) values in each band by the TOA reflectance coefficients
def convert (spectral_bands, coefficients):
	reflectances = {}
	print coefficients
	for key, value in spectral_bands.items():
		if coefficients[key]:
			reflectance = {}
			reflectance['band_blue_reflectance'] = spectral_bands[key]['band_blue_radiance'] * coefficients[key][1]
			reflectance['band_green_reflectance'] = spectral_bands[key]['band_green_radiance'] * coefficients[key][2]
			reflectance['band_red_reflectance'] = spectral_bands[key]['band_red_radiance'] * coefficients[key][3]
			reflectance['band_nir_reflectance'] = spectral_bands[key]['band_nir_radiance'] * coefficients[key][4]

			#print "Red band radiance is from {} to {}".format(np.amin(band_red_radiance), np.amax(band_red_radiance))
			#print "Red band reflectance is from {} to {}".format(np.amin(band_red_reflectance), np.amax(band_red_reflectance))
		reflectances[key] = reflectance
	return reflectances

