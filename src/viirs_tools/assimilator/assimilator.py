import os
import subprocess as sp
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timedelta


def _test_cmrfetch():
    """Test for availability of cmrfetch
    Test was unsuccessfull in the case of any exception
    """
    cf = "cmrfetch"
    try:
        sp.run([cf, "--version"], check=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    except FileNotFoundError as e:
        raise Exception(f"{cf} is not accessible") from e
    except sp.CalledProcessError as e:
        if e.returncode != 0:
            raise Exception(f"{cf} was found, failed to execute") from e


def _get_data_for_interval(
    path: str,
    start_d: str,
    end_d: str,
    names: list[str],
    geobox: str,
    dconc: int = 4,
):
    """Worker function for downloading data itself

    Args:
        path : path for saving downloaded files
        start_d : start of the time selection interval (including)
        end_d : end of the time selection interval (excluding)
        names : shortnames for desired collections
        geobox : bounding box for selecting granules for format information check cmrfetch docs
        dconc : number of concurrently downloading connections
    """
    snames = ""
    for i in names:
        snames += f"-s {i} "
    x = 1
    cnt = 0
    while x != 0:
        # really rough solution, timeouts are handled by cmrfetch
        # so they cannot be recognized as runtime error below
        # TODO: cmrfetch output analysis for re-downloading failed files
        fetch_cli = [
            "cmrfetch",
            "granules",
            str(snames),
            "-t",
            str(start_d),
            ",",
            str(end_d),
            "--bounding-box",
            str(geobox),
            "--download",
            str(path),
            "--download-concurrency",
            str(dconc),
        ]
        r = sp.run(fetch_cli, check=True)
        x = r.returncode
        cnt += 1
        if cnt == 5:
            raise RuntimeError(f"Cannot download data for {start_d},{end_d}")


def assimilate(
    names: list[str],
    geobox: str,
    start_d: datetime,
    end_d: datetime,
    path: str,
    workers: int,
    max_queue: int = 0,
    assim_callback: Callable[[str], None] = (lambda path: None),
    dconc: int = 4,
):
    """Performs data assimilation - download it using cmrfetch
    per day intervals and then perform callback function
    on it (for compression purposes mainly)

    Args:
        names : shortnames for desired collections
        geobox: bounding box for selecting granules
            for format information check cmrfetch docs
        start_d : start of the time selection interval (including)
        end_d : end of the time selection interval (excluding)
        path : path for saving downloaded files
        workers : max num of the processes performing callbacks
        max_queue : max num of the queued callback
            tasks, used for downloading throttling
            (for avoiding disk filling)
        assim_callback : callback to perform
            on the each set of data per single day
        dconc : number of concurrently downloading connections
    """
    _test_cmrfetch()

    if max_queue == 0:
        max_queue = 2 * workers

    if not os.path.exists(path):
        os.mkdir(path)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []
        cur_d = end_d
        next_d = end_d + timedelta(days=1)
        while cur_d >= start_d:
            cur_d_s = cur_d.strftime("%Y-%m-%d")
            next_d_s = next_d.strftime("%Y-%m-%d")
            step_path = os.path.join(path, f"{cur_d_s}")

            _get_data_for_interval(step_path, cur_d_s, next_d_s, names, geobox, dconc)

            task = executor.submit(assim_callback, step_path)
            futures.append(task)

            next_d = cur_d
            cur_d -= timedelta(days=1)

            # Throttling data downloading
            if len(futures) > max_queue:
                while len(futures) > max_queue:
                    futures = [f for f in futures if not f.done()]
                    if len(futures) != 0:
                        futures[0].result()
