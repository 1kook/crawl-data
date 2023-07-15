from pandas import DataFrame

from src.service.indicator.indicator import Indicator


class EmaTrategy:
    def __init__(self, df: DataFrame) -> None:
        pass

    def signal(df, dtf):
        indicator = Indicator(df, dtf)
        indicator.ema(5).ema(25)

        # find cross point
        ema5 = indicator.emas[5]
        ema25 = indicator.emas[25]

        # find cross point
        cross = cross_point(ema5, ema25)


def cross_point(ema5, ema25):
    for i in range(len(ema25)-1):
        for j in range(len(ema5)-1):
            # 2 line cross
            if ema5[j] > ema25[i] and ema5[j+1] < ema25[i+1]:
                return j
            elif ema5[j] < ema25[i] and ema5[j+1] > ema25[i+1]:
                return j
    return -1
