from osgeo import ogr, osr
import pandas as pd
import numpy as np

def transform_4326_to_3857(lat, long):
    # make spatial references
    # 4326 in
    InSR = osr.SpatialReference()
    InSR.ImportFromEPSG(4326)
    # 3857 out
    OutSR = osr.SpatialReference()
    OutSR.ImportFromEPSG(3857)

    # create the point
    Point = ogr.Geometry(ogr.wkbPoint)
    Point.AddPoint(lat, long)

    # assign the spacial reference to the point
    Point.AssignSpatialReference(InSR)

    # transform
    transform_error_code = Point.TransformTo(OutSR)

    # error check (eg, point is out of bounds, etc)
    if transform_error_code == 0:
        # success
        return Point.GetX(), Point.GetY()
    else:
        # failed
        print("Transform failed! Error {transform_error_code}")
        return None


# load data
pts_df = pd.read_csv("site-coordinates.csv", header=0)
# append transform columns
pts_df["lat 3857"] = np.nan
pts_df["lon 3857"] = np.nan

print(pts_df.head())

for e in pts_df.iterrows():
    e["lat 3857"], e["lon 3857"] = transform_4326_to_3857(e["lat"], e["lon"])

pts_df.to_csv("site-coordinates-3857")
