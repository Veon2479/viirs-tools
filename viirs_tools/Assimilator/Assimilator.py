import subprocess as sp
import os
from datetime import timedelta
from concurrent.futures import ProcessPoolExecutor


def _test_cmrfetch():
    """
        Test for availability of cmrfetch
        Test was unsuccessfull in the case
            of any exception
    """
    cf = 'cmrfetch'
    try:
        sp.run(
            [cf, "--version"], check=True,
            stdout=sp.DEVNULL, stderr=sp.DEVNULL
        )
    except FileNotFoundError:
        raise Exception(
            f'{cf} is not accessible'
        )
    except sp.CalledProcessError as e:
        if e.returncode != 0:
            raise Exception(
                f"{cf} was found, failed to execute"
            )


def _get_data_for_interval(
    path,
    start_d, end_d,
    names,
    geobox,
    dconc=4
):
    """
        Worker function for downloading data itself
    Args:
        path (string): path for saving downloaded files
        start_d (datetime.datetime): start of the
            time selection interval (including)
        end_d (datetime.datetime): end of the
            time selection interval (excluding)
        names (list of string): shortnames for
            desired collections
        geobox (string): bounding box for selecting granules
            for format information check cmrfetch docs
        dconc (int): number of concurrently
            downloading connections
    """
    snames = ''
    for i in names:
        snames += f'-s {i} '
    x = 1
    cnt = 0
    while (x != 0):
        # really robust solution, timeouts are handled by cmrfetch
        # so they cannot be recognized as runtime error below
        # TODO: cmrfetch output analysis for re-downloading failed files
        fetch_cli = f'cmrfetch granules {snames} -t {start_d},{end_d} --bounding-box {geobox} --download {path} --download-concurrency {dconc}'
        r = sp.run(fetch_cli.split())
        x = r.returncode
        cnt += 1
        if (cnt == 5):
            raise RuntimeError(f'Cannot download data for {start_d},{end_d}')


def assimilate(
    names, geobox,
    start_d, end_d,
    path,
    workers, max_queue=0,
    assim_callback=(lambda path: None),
    dconc=4
):
    """
        Performs data assimilation - download it using cmrfetch
            per day intervals and then perform callback function
            on it (for compression purposes mainly)
    Args:
        names (list of string): shortnames for
            desired collections
        geobox (string): bounding box for selecting granules
            for format information check cmrfetch docs
        start_d (datetime.datetime): start of the
            time selection interval (including)
        end_d (datetime.datetime): end of the
            time selection interval (excluding)
        path (string): path for saving downloaded files
        workers (int): max num of the processes
            performing callbacks
        max_queue (int): max num of the queued callback
            tasks, used for downloading throttling
            (for avoiding disk filling)
        assim_callback (function(path)): callback to perform
            on the each set of data per single day
        dconc (int): number of concurrently
            downloading connections
    """
    _test_cmrfetch()

    if (max_queue == 0):
        max_queue = 2 * workers

    if (not os.path.exists(path)):
        os.mkdir(path)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []
        cur_d = end_d
        next_d = end_d + timedelta(days=1)
        while (cur_d >= start_d):
            cur_d_s = cur_d.strftime('%Y-%m-%d')
            next_d_s = next_d.strftime('%Y-%m-%d')
            step_path = os.path.join(path, f'{cur_d_s}')

            _get_data_for_interval(
                step_path,
                cur_d_s, next_d_s,
                names,
                geobox,
                dconc
            )

            task = executor.submit(assim_callback, step_path)
            futures.append(task)

            next_d = cur_d
            cur_d -= timedelta(days=1)

            # Throttling data downloading
            if (len(futures) > max_queue):
                while (len(futures) > max_queue):
                    futures = [f for f in futures if not f.done()]
                    if (len(futures) != 0):
                        futures[0].result()
