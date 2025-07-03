---
title: Don't forget about help() and vars()
date: 2025-07-03 13:39:53.174955
description: I was working on a project and learned a lot using the REPL and two commands that can be used ALL the time.
tags:
  - python
---

While working on my [plant-tracker](https://github.com/kjaymiller/plant-tracker), I wanted to learn more about what was available in my grow sensors... Good thing they did documentation.

Using `help(Moisture)`.  I learned that I was looking at data backwards (Lower moisture settings are better, not higher).

Using `vars` I was able to learn about all the data that I had in my

```python
>>> from grow.moisture import Moisture
>>> vars(Moisture(1))
  {
    '_gpio_pin': 23,
    '_count': 0,
    '_reading': 0,
    '_history': [],
    '_history_length': 200,
    '_last_pulse': 1751564749.6594245,
    '_new_data': False,
    '_wet_point': 0.7,
    '_dry_point': 27.6,
    '_time_last_reading': 1751564749.6594367,
    '_time_start': 1751564749.6804533,
  }
  ```

I saw `_new_data': Fase` and that pushed me to check `help` again and I saw there was an `active` parameter.

This allowed me to update my plant tracker code to work with devices that would only collect sensor data from sensors that are active.
That means if remove a sensor (often to water a plant) I don't get misleading `0` data points anymore.

This is just a reminder that Python code is examinable. It's also a reminder that you should write great doc strings (that said don't look at the functions in `db_store`).
