import gc
import os
import re
import time
from datetime import UTC, datetime

import satpy
from pyresample.geometry import AreaDefinition

from viirs_tools.assimilator.assimilator import assimilate
from viirs_tools.assimilator.reading import read_npp_cldmsk_l2

area_by = AreaDefinition(
    area_id="Belarus",
    description="The region of Belarus (WGS 84 / UTM zone 35N Projection)",
    projection="EPSG:32635",
    proj_id="EPSG:32635",
    # width = 700,  # resolution=1000
    # height = 600, # resolution=1000
    width=1400,  # resolution=500
    height=1200,  # resolution=500
    area_extent=(
        200000,
        5650000,
        900000,
        6250000,
    ),
)

DEBUG = True


def log(msg, debug=DEBUG):
    if debug:
        print(msg)


def generate_composits(prefix, i_file, c_file, ig_file, mg_file):
    gc.collect()

    if os.path.exists(prefix):
        os.system(f"rm -rf {prefix}")
    os.mkdir(prefix)

    # load i_file, ig_file, generate i-bands composits
    log("[LOG] Generating I-band data..")
    si = satpy.Scene(filenames=[i_file, ig_file], reader="viirs_l1b")

    is_day = "I01" in si.available_dataset_names()
    if is_day:
        si.load(["I01", "I02", "I03"])
    si.load(["I04", "I05", "i_lat", "i_lon"])

    rsi = si.resample(destination=area_by, resampler="nearest")

    log("[LOG] probing for enough amount of data..")
    mask = rsi["I05"].notnull()
    s = mask.sum()
    if s < 0.1 * mask.shape[0] * mask.shape[1]:
        log("[WARN] Not enough data, skipping..")
        os.rmdir(prefix)
        del rsi
        del si
        gc.collect()
    else:
        if is_day:
            rsi.save_dataset(
                "I01",
                writer="geotiff",
                enhance=False,
                filename=os.path.join(prefix, "i01_ref.tiff"),
            )
            rsi.save_dataset(
                "I02",
                writer="geotiff",
                enhance=False,
                filename=os.path.join(prefix, "i02_ref.tiff"),
            )
            rsi.save_dataset(
                "I03",
                writer="geotiff",
                enhance=False,
                filename=os.path.join(prefix, "i03_ref.tiff"),
            )
        rsi.save_dataset(
            "I04",
            writer="geotiff",
            enhance=False,
            filename=os.path.join(prefix, "i04_bt.tiff"),
        )
        rsi.save_dataset(
            "I05",
            writer="geotiff",
            enhance=False,
            filename=os.path.join(prefix, "i05_bt.tiff"),
        )
        log("[LOG] writing is done")

        del rsi
        del si
        gc.collect()

        # load c_file, mg_file, generate cm composit
        log("[LOG] Generating cloud mask data..")
        s = satpy.Scene(filenames=[mg_file], reader="viirs_l1b")
        s.load(["solar_zenith_angle", "m_lat", "m_lon"])
        d = s["solar_zenith_angle"]
        d.attrs["name"] = "integer_cloud_mask"
        d.attrs["standard_name"] = "integer_cloud_mask"
        d.attrs["long_name"] = "integer cloud mask"
        d.attrs["valid_min"] = 0
        d.attrs["valid_max"] = 1
        d.attrs["scale_factor"] = 1
        d.attrs["units"] = "none"
        d.attrs["file_key"] = ""
        d.attrs["file_units"] = "none"
        d.attrs["reader"] = ""
        cm_h = read_npp_cldmsk_l2(c_file)
        cm = cm_h["cloud_mask"]
        d.data = cm.astype(d.dtype)
        rs = s.resample(destination=area_by, resampler="nearest")
        rs.save_dataset(
            "solar_zenith_angle",
            writer="geotiff",
            enhance=False,
            filename=os.path.join(prefix, "mvcm.tiff"),
        )
        del rs
        del s
        gc.collect()
        log(f"[LOG] {prefix} is done")
        return True
    log(f"[LOG] {prefix} is cancelled")
    return False


def my_assim(path):
    i_files = []
    c_files = []
    mg_files = []
    ig_files = []

    files = os.listdir(path)
    for file in files:
        filepath = os.path.join(path, file)
        if re.match(r"VNP02IMG", file) is not None:
            i_files.append(filepath)
        if re.match(r"CLDMSK", file) is not None:
            c_files.append(filepath)
        if re.match(r"VNP03IMG", file) is not None:
            ig_files.append(filepath)
        if re.match(r"VNP03MOD", file) is not None:
            mg_files.append(filepath)

    k = 1
    for c_file in c_files:
        ts = re.search(r"A\d{7}\.\d{4}", c_file)[0]
        i_file = ""
        mg_file = ""
        ig_file = ""

        for file in i_files:
            if ts in file:
                i_file = file
                break

        for file in mg_files:
            if ts in file:
                mg_file = file
                break

        for file in ig_files:
            if ts in file:
                ig_file = file
                break

        if ig_file == "" or mg_file == "" or i_file == "":
            print(f"[WARN] [{k}/{len(c_files)}] Skipping timestamp {ts}")
        else:
            print(f"[LOG] [{k}/{len(c_files)}] Generating data for {ts}..")
            generate_composits(os.path.join(path, ts), i_file, c_file, ig_file, mg_file)
        k += 1

    print("[LOG] cleanup..")

    for i in i_files:
        os.remove(i)
    for i in c_files:
        os.remove(i)
    for i in mg_files:
        os.remove(i)
    for i in ig_files:
        os.remove(i)

    print(f"[LOG] {path} is done")


names = ["VNP02IMG", "VNP03IMG", "VNP03MOD", "CLDMSK_L2_VIIRS_SNPP"]
BY_BOX = "23.1774,51.256,32.7628,56.172"
sd = datetime(2012, 3, 1, tzinfo=UTC)
ed = datetime(2012, 11, 7, tzinfo=UTC)


t1 = time.time()
assimilate(names, sd, ed, "./2012", BY_BOX, 1, assim_callback=my_assim)
t2 = time.time()

print(f"Done in {t2 - t1}")
