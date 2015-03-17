import time
import math

from htu21d import HTU21D


def calc_dew_pt(temp_c, rel_hum):
    A, B, C = 8.1332, 1762.39, 235.66

    pp_amb = 10 ** (A - (B / (temp_c + C)))
    return -(C + (B / (math.log10(rel_hum * pp_amb / 100) - A ))), pp_amb


if __name__ == '__main__':
    sensor = HTU21D()
    sensor.reset()
    temp = sensor.get_temp()
    hum = sensor.get_rel_humidity()
    print(time.time(), temp , hum)

    temp_f = temp * 9/5 + 32
    dew_pt, pp_amb = calc_dew_pt(temp, hum)

    import statsd
    from local_settings import STATSD_HOST, STATSD_PORT, STATSD_PREFIX
    client = statsd.StatsClient(STATSD_HOST, STATSD_PORT, prefix=STATSD_PREFIX)

    with client.pipeline() as pipe:
        pipe.gauge('deg_f', 0)
        pipe.gauge('deg_c', 0)
        pipe.gauge('rel_hum', 0)
        pipe.gauge('pp_ambient', 0)
        pipe.gauge('dew_pt', 0)

        pipe.gauge('deg_f', round(temp_f, 2))
        pipe.gauge('deg_c', round(temp, 2))
        pipe.gauge('rel_hum', round(hum, 2))
        pipe.gauge('pp_ambient', round(pp_amb, 2))
        pipe.gauge('dew_pt', round(dew_pt, 2))

