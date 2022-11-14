# cvtranslate
Historical data translator for cv data models<br />

Setup: ``pip install -r requirements.txt``<br />

Usage: ``python main.py <arguments>``<br />

Arguments:

``-b --baseline <int>`` Baseline average used in conjunction with EMA to resample the output for easier charting.<br />
``-ema --exponential_moving_average <int>`` Aptly named.<br />
``-tt --time_to_ticks <bool>`` When set `True` time stamps are returned in seconds from 1970.1.1 otherwise in YYYY-MM-DD HH:mm:ss.<br />
``-f --fix_dates <bool>`` When set `True` missing dates are recalculated and filled in from a lower timeframe.<br />
``-t --trim_days <int>`` As the sample data is a full/raw set there are some anomalies early on, this will trim N days to refine the output.<br />

EMA resampling is calculated as (baseline_average - exponential moving average)<br />

A smattering of information on the idea behind the system can be found in the `<project root>/reference` folder.<br />

In addition to the output data, the delivery tool that is being used for this experiment is in the form of a discord bot.<br />

For additional information and experimentation it can be accessed using the following procedure:<br />
* Join `https://discord.gg/Sy6RKHqE`
* Private message `MagicFeed Beta #5726`
* Activate using the public researcher promo code: `412186895428711041`
* * If you feel this is useful and want to toss some litecoin at me for server costs, that's cool as well ;)
* See the integrated bot help for further instructions.