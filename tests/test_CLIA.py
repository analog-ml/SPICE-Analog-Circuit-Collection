import os
from extract_perf import PerformanceExtractor
import time
import pandas as pd


def test_CLIA():
    cwd = os.getcwd()
    os.chdir("circuits/CLIA")

    # remove previously generated file
    if os.path.exists("ac.csv"):
        os.remove("ac.csv")

    if os.path.exists("dc.csv"):
        os.remove("dc.csv")
    os.system("ngspice -b " + "CLIA.cir")
    os.chdir(cwd)

    performance_extractor = PerformanceExtractor("circuits/CLIA")
    result = performance_extractor.extract()
    print(result)

    assert result["gain"] == 1659973.9474416797
    assert result["ugbw"] == 2169897.212368708
    assert result["pm"] == 116.34214569243828
    assert result["power"] == 1.5690802e-05


def test_CLIA_get_PM_via_meas_command():
    cwd = os.getcwd()
    os.chdir("circuits/CLIA")

    # remove previously generated file
    delete_files = ["ac.csv", "dc.csv", "CLIA_GBW_PM"]
    for f in delete_files:
        if os.path.exists(f):
            os.remove(f)

    os.system("ngspice -b " + "CLIA-get-pm-directly.cir")
    os.chdir(cwd)

    data = pd.read_csv(
        "circuits/CLIA/CLIA_GBW_PM",
        sep=r"\s+",
        # names=["freq", "gbw", "freq", "pm"],
        # skiprows=0,
        # header=None,
    )
    print(data)
    assert data.iloc[0]["gain_bandwidth_product"] == 2189211.0
    assert data.iloc[0]["phase_margin"] == -63.62661
