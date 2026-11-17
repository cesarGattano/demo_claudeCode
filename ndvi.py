"""Carte NDVI à partir de la scène Sentinel-2 L2A la moins nuageuse sur une zone.

Recherche la scène via le catalogue STAC Earth Search, lit uniquement l'emprise
demandée dans les COG (lecture fenêtrée), calcule le NDVI et enregistre une
figure PNG : couleurs naturelles à gauche, NDVI à droite.
"""

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from pystac_client import Client
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

# --- Paramètres ------------------------------------------------------------
STAC_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION = "sentinel-2-l2a"
BBOX = (1.40, 48.30, 1.50, 48.36)  # lon min, lat min, lon max, lat max (WGS84)
DATES = "2025-07-01/2025-07-31"
MAX_CLOUD = 20  # couverture nuageuse maximale (%)
OUTPUT = "ndvi.png"
# ---------------------------------------------------------------------------


def find_least_cloudy_item():
    """Renvoie la scène la moins nuageuse correspondant aux paramètres."""
    catalog = Client.open(STAC_URL)
    search = catalog.search(
        collections=[COLLECTION],
        bbox=BBOX,
        datetime=DATES,
        query={"eo:cloud_cover": {"lt": MAX_CLOUD}},
    )
    items = list(search.items())
    if not items:
        raise SystemExit("Aucune scène trouvée : élargir les dates ou le seuil de nuages.")
    return min(items, key=lambda item: item.properties["eo:cloud_cover"])


def read_band(item, band):
    """Lit une bande sur l'emprise BBOX et renvoie la réflectance (float32)."""
    asset = item.assets[band]
    with rasterio.open(asset.href) as src:
        # La bbox est en WGS84, l'image en UTM : on reprojette l'emprise.
        bounds = transform_bounds("EPSG:4326", src.crs, *BBOX)
        data = src.read(1, window=from_bounds(*bounds, transform=src.transform))
        nodata = src.nodata

    reflectance = data.astype("float32")
    # Earth Search fournit l'échelle et le décalage dans les métadonnées STAC.
    band_info = (asset.extra_fields.get("raster:bands") or [{}])[0]
    reflectance = reflectance * band_info.get("scale", 1e-4) + band_info.get("offset", 0.0)
    if nodata is not None:
        reflectance[data == nodata] = np.nan
    return reflectance


def main():
    item = find_least_cloudy_item()
    date = item.datetime.date()
    cloud = item.properties["eo:cloud_cover"]
    print(f"Scène retenue : {item.id} ({date}, {cloud:.1f} % de nuages)")

    red, green, blue, nir = (read_band(item, b) for b in ("red", "green", "blue", "nir"))

    with np.errstate(divide="ignore", invalid="ignore"):
        ndvi = (nir - red) / (nir + red)

    # Couleurs naturelles : étirement entre les percentiles 2 et 98 pour l'affichage.
    rgb = np.dstack([red, green, blue])
    low, high = np.nanpercentile(rgb, (2, 98))
    rgb = np.clip((rgb - low) / (high - low), 0, 1)

    fig, (ax_rgb, ax_ndvi) = plt.subplots(1, 2, figsize=(14, 6))
    ax_rgb.imshow(rgb)
    ax_rgb.set_title("Couleurs naturelles")
    im = ax_ndvi.imshow(ndvi, cmap="RdYlGn", vmin=-0.2, vmax=0.9)
    ax_ndvi.set_title("NDVI")
    fig.colorbar(im, ax=ax_ndvi, label="NDVI")
    for ax in (ax_rgb, ax_ndvi):
        ax.set_axis_off()
    fig.suptitle(f"Sentinel-2 L2A, Beauce, {date} ({cloud:.1f} % de nuages)")
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=120)
    print(f"Figure enregistrée : {OUTPUT}")


if __name__ == "__main__":
    main()
