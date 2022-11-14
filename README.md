# cvtranslate
Historical data translator for cv data models

Setup: ``pip install -r requirements.txt``

Usage: ``python main.py <arguments>``

Arguments:

``-b --baseline <int>`` Baseline average used in conjunction with EMA to resample the output for easier charting.
``-ema --exponential_moving_average <int>`` Aptly named.
``-tt --time_to_ticks <bool>`` When set `True` time stamps are returned in seconds from 1970.1.1 otherwise in YYYY-MM-DD HH:mm:ss.
``-f --fix_dates <bool>`` When set `True` missing dates are recalculated and filled in from a lower timeframe.
``-t --trim_days <int>`` As the sample data is a full/raw set there are some anomalies early on, this will trim N days to refine the output.

EMA resampling is calculated as (baseline_average - exponential moving average)

A smattering of information on the idea behind the system can be found in the `<project root>/reference` folder.

In addition to the output data, the delivery tool that is being used for this experiment is in the form of a discord bot.

For additional information and experimentation it can be accessed using the following procedure:
* Join `https://discord.gg/Sy6RKHqE`
* Private message `MagicFeed Beta #5726`
* Activate using the public researcher promo code: `412186895428711041`
* See the integrated bot help for further instructions.