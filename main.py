"""
This will perform a translation of all the datamodels within the models folder and output the translated information
into the output folder.
"""

import os
import csv
import datetime
from pathlib import Path
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baseline', action="store_true", help='Baseline normalization average', default=1)
parser.add_argument('-ema', '--exponential_moving_average', store="store_true", help='exponential moving average', default=20)
parser.add_argument('-tt', '--time_to_ticks', action="store_true", help='Process timestamps in ticks or human readable', default=False)


args = parser.parse_args()


timeframes = ['15MINUTE', '30MINUTE', '1HOUR', '4HOUR', '1DAY']
AL = args.exponential_moving_average
BL = args.baseline
TT = args.time_to_ticks

for arg in [AL, BL]:
    if not isinstance(arg, int):
        raise TypeError
if not isinstance(TT, bool):
    raise TypeError
if BL < AL:
    print('baseline cannot be less than moving average')
    raise ValueError

here = Path(os.path.abspath(os.path.join(os.path.dirname(__file__))))
models = here / Path('models')
output = here / Path('output')
ext = '.csv'
model_files = os.listdir(models)
old_files = os.listdir(output)
for o_file in old_files:
    os.remove(output / Path(o_file))  # noqa
output_files = list()


def open_file(filename: str, as_list: bool = False):
    """
    Opens a text file.
    :param filename: File to open.
    :type filename: Str
    :param as_list: This will return readlines instead of read.
    :return: Contents of file.
    :rtype: list
    """
    filename = Path(filename)
    filename.touch()  # Create file if it doesn't exist.
    file = open(filename, 'r+')
    if as_list:
        lst = list()
        for f in file.readlines():
            lst.append(eval(f))
        return lst
    else:
        return file.read()


def string_to_ticks(timestamp: str) -> int:
    """
    This will convert our timestamps into standard ticks format.
    """
    _d = datetime.datetime.strptime(timestamp, "%Y-%m-%d-%H-%M")
    t0 = datetime.datetime(1970, 1, 1)
    ticks = (_d - t0).total_seconds()
    return int(ticks)


def translate_fields(fields: [dict, list]) -> tuple:
    """
    This will translate our field data from:
        {'stamp': '2021-07-18-01-53', 'bar': [0.91, 0.91, 0.84, 0.84, 1.443], 'alts': {'ada': 1.9, 'busd': 0.46, 'bnb': 0.66, 'trx': 0.66, 'doge': 1.86, 'xrp': 0.24}}
    into:
        {'timestamp': val, 'open': val, 'high': val, 'low': val, 'close': val, 'volume': val, 'diversity': val}
    """
    f = fields
    if isinstance(fields, dict):
        _o, _c, _h, _l, _v = f['bar']
        _d = len(f['alts'])
        timestamp = f['stamp']
    elif isinstance(fields, list):
        timestamp, _o, _h, _l, _c, _v, _d = fields
    else:
        raise ValueError
    try:
        timestamp = string_to_ticks(timestamp)
    except (ValueError, TypeError):
        pass
    result = {
        'timestamp': timestamp,
        'open': _o,
        'high': _h,
        'low': _l,
        'close': _c,
        'volume': _v,
        'diversity': _d,
    }, [
        _o, _h, _l, _c
    ]
    return result


def normalize_quotes(_quotes: list, average_length: int, average_base: int):
    """
    This will produce a moving average of the incoming data, then subtract it from itself, so we have a nice
    horizontal chart plot.
    """

    def ema(_q, al) -> np.ndarray:
        """
        Yup EMA..
        """
        ret = np.cumsum(_q, dtype=float)
        ret[al:] = ret[al:] - ret[:-al]
        ays = ret[al - 1:] / al
        padding = np.subtract(al, 1)
        average = np.pad(ays, (padding, 0))
        average = np.array(average)
        return average

    _qu = np.transpose(_quotes)
    transposed_averages = list()
    for _q in _qu:
        ma = ema(_q, average_base)
        normal = ema(_q, average_length)
        transposed_averages.append(np.subtract(normal, ma))
    result = np.transpose(transposed_averages)
    return result


for idx, m_file in enumerate(model_files):
    target = Path('charts/aaa_floating.dat')
    prefix = Path(m_file)  # noqa
    output_name = str(prefix.as_posix())
    output_files.append(output_name)
    model_files[idx] = Path('models') / prefix / target
pass  # debug hook

for idx, m_file in enumerate(model_files):
    raw_data = open_file(m_file.as_posix(), as_list=True)[0]  # noqa
    for timeframe in timeframes:
        frame_data = raw_data[timeframe]
        output_name = f'output/{output_files[idx]}_{timeframe}_{ext}'
        output_file = Path(output_name)
        if not output_file.is_file():
            output_file.touch()
        fieldnames = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'diversity']
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            quotes = list()
            for quote in frame_data:
                try:
                    row, quote = translate_fields(quote)
                    writer.writerow(row)
                    quotes.append(quote)
                except ValueError as err:
                    print(row, '\n', err)
                    pass
            csv_file.close()
        output_name = f'output/{output_files[idx]}_{timeframe}_PROCESSED{ext}'
        output_file = Path(output_name)
        normalized_quotes = normalize_quotes(
            quotes,
            AL,
            BL,  # len(quotes)
        )

        if not output_file.is_file():
            output_file.touch()
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for quote, normalized_quote in zip(frame_data, normalized_quotes):
                q, _ = translate_fields(quote)
                t = q['timestamp']
                v = q['volume']
                d = q['diversity']
                o, h, l, c = normalized_quote
                row = [t, o, h, l, c, v, d]
                try:
                    row, _ = translate_fields(row)
                    writer.writerow(row)
                except ValueError as err:
                    print(row, '\n', err)
                    pass
            csv_file.close()
