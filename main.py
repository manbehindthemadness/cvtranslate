"""
This will perform a translation of all the datamodels within the models folder and output the translated information
into the output folder.
"""

import os
import csv
import datetime
from pathlib import Path


timeframes = ['15MINUTE', '30MINUTE', '1HOUR', '4HOUR', '1DAY']


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
    d = datetime.datetime.strptime(timestamp, "%Y-%m-%d-%H-%M")
    t0 = datetime.datetime(1970, 1, 1,
                           # tzinfo=datetime.timezone.utc
                           )
    ticks = (d - t0).total_seconds()
    return int(ticks)


def translate_fields(fields: dict) -> dict:
    """
    This will translate our field data from:
        {'stamp': '2021-07-18-01-53', 'bar': [0.91, 0.91, 0.84, 0.84, 1.443], 'alts': {'ada': 1.9, 'busd': 0.46, 'bnb': 0.66, 'trx': 0.66, 'doge': 1.86, 'xrp': 0.24}}
    into:
        {'timestamp': val, 'open': val, 'high': val, 'low': val, 'close': val, 'volume': val, 'diversity': val}
    """
    f = fields
    o, c, h, l, v = f['bar']
    d = len(f['alts'])
    timestamp = f['stamp']
    try:
        timestamp = string_to_ticks(timestamp)
    except ValueError:
        pass
    result = {
        'timestamp': timestamp,
        'open': o,
        'high': h,
        'low': l,
        'close': c,
        'volume': v,
        'diversity': d,
    }
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
            for quote in frame_data:
                try:
                    row = translate_fields(quote)
                    writer.writerow(row)
                except ValueError as err:
                    print(row, '\n', err)
                    pass
            csv_file.close()

