"""Convert latitude/longitude coordinates to ZIP codes in Python.

Uses `pgeocode` for the postal-code dataset (downloaded from GeoNames once,
then cached locally) and a vectorized nearest-postal-area search to map a
coordinate to its ZIP code. No API keys or per-request network calls.

Install:  python3 -m pip install pgeocode
Example:  python3 latlon_to_zipcode.py
"""

import math

import numpy as np
import pgeocode

_COUNTRY_MIN_MAX = {
    "us": (-180, -60, 15, 75),  # lon_min, lon_max, lat_min, lat_max bounds
}

_zip_index = {}


def _load_index(country):
    """Build numpy arrays of (postal_code, lat, lon) for a country once."""
    key = country.lower()
    if key in _zip_index:
        return _zip_index[key]

    nomi = pgeocode.Nominatim(key)
    df = nomi._data_frame

    # Drop rows with unusable coordinates (GeoNames files contain glitches
    # such as latitude/longitude recorded as 0).
    valid = (df.latitude.abs() > 0.01) & (df.longitude.abs() > 0.01)
    if key in _COUNTRY_MIN_MAX:
        lon_min, lon_max, lat_min, lat_max = _COUNTRY_MIN_MAX[key]
        valid &= (
            df.longitude.between(lon_min, lon_max)
            & df.latitude.between(lat_min, lat_max)
        )

    df = df[valid]
    index = (
        df.postal_code.to_numpy(str),
        df.latitude.to_numpy(float),
        df.longitude.to_numpy(float),
    )
    _zip_index[key] = index
    return index


def _haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance (km) between arrays of coordinate pairs."""
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(np.minimum(a, 1.0)))


def coords_to_zip(latitude, longitude, country="us", max_distance_km=None):
    """Return the ZIP code nearest to (latitude, longitude).

    Args:
        latitude: coordinate latitude.
        longitude: coordinate longitude.
        country: two-letter country code (default 'us').
        max_distance_km: if set, return None when the nearest postal area is
            farther than this many kilometers (e.g. a point in the ocean).

    Returns:
        ZIP code as a string, or None if nothing is within range.
    """
    codes, zlats, zlons = _load_index(country)
    lat = np.asarray([latitude], dtype=float)
    lon = np.asarray([longitude], dtype=float)

    dist = _haversine(lat, lon, zlats, zlons)
    idx = int(np.argmin(dist))

    if max_distance_km is not None and dist[idx] > max_distance_km:
        return None
    return codes[idx]


def coords_to_zips(latitudes, longitudes, country="us", max_distance_km=None):
    """Return ZIP codes for iterables of (latitude, longitude) pairs.

    Args:
        latitudes: iterable of latitudes.
        longitudes: iterable of longitudes, same length as latitudes.
        country: two-letter country code (default 'us').
        max_distance_km: if set, returns None for rows whose nearest postal
            area is farther than this many kilometers away.

    Returns:
        List of ZIP codes (strings or None) aligned with the inputs.
    """
    codes, zlats, zlons = _load_index(country)
    lats = np.asarray(list(latitudes), dtype=float)
    lons = np.asarray(list(longitudes), dtype=float)

    # Compute in chunks to keep the distance matrix small. A single chunk of
    # C points against all ~41k postal areas only needs C * 41000 floats.
    chunk_size = 250
    zips = []
    for start in range(0, len(lats), chunk_size):
        c_lats = lats[start : start + chunk_size]
        c_lons = lons[start : start + chunk_size]

        dist = _haversine(
            c_lats[:, None], c_lons[:, None], zlats[None, :], zlons[None, :]
        )
        idx = np.argmin(dist, axis=1)
        min_dist = dist[np.arange(len(c_lats)), idx]

        for i, d in zip(idx, min_dist):
            if max_distance_km is not None and d > max_distance_km:
                zips.append(None)
            else:
                zips.append(codes[i])
    return zips


def add_zipcodes(df, lat_col, lon_col, country="us", max_distance_km=None):
    """Return a copy of DataFrame `df` with a new 'zipcode' column added."""
    out = df.copy()
    out["zipcode"] = coords_to_zips(
        df[lat_col], df[lon_col], country=country, max_distance_km=max_distance_km
    )
    return out


def main(argv=None):
    import argparse

    import pandas as pd

    parser = argparse.ArgumentParser(
        description="Add a ZIP code column to a CSV containing latitudes and "
        "longitudes."
    )
    parser.add_argument("csv", help="Path to the input CSV file")
    parser.add_argument(
        "-lat",
        "--lat-col",
        default="latitude",
        help="Name of the latitude column (default: 'latitude')",
    )
    parser.add_argument(
        "-lon",
        "--lon-col",
        default="longitude",
        help="Name of the longitude column (default: 'longitude')",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path for the output CSV (default: <input>_with_zipcodes.csv)",
    )
    parser.add_argument(
        "-c",
        "--country",
        default="us",
        help="Two-letter country code (default: 'us')",
    )
    parser.add_argument(
        "-d",
        "--max-distance-km",
        type=float,
        help="Only assign a ZIP code when the nearest postal area is within "
        "this many km; otherwise leave the cell blank",
    )
    args = parser.parse_args(argv)

    df = pd.read_csv(args.csv)
    if args.lat_col not in df.columns or args.lon_col not in df.columns:
        raise SystemExit(
            f"CSV has columns: {list(df.columns)}. "
            f"Could not find '{args.lat_col}' or '{args.lon_col}'. "
            "Use -lat/-lon to pick the right ones."
        )

    result = add_zipcodes(
        df,
        args.lat_col,
        args.lon_col,
        country=args.country,
        max_distance_km=args.max_distance_km,
    )

    out_path = args.output or args.csv.rsplit(".", 1)[0] + "_with_zipcodes.csv"
    result.to_csv(out_path, index=False)

    matched = result["zipcode"].notna().sum()
    print(f"Processed {len(result):,} rows -> {matched:,} ZIP codes assigned")
    print(f"Output written to: {out_path}")


if __name__ == "__main__":
    main()