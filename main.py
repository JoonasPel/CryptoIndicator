# pylint: disable=C0114, C0116, W0718
import numpy as np
import matplotlib.pyplot as plt
import utils
import data

def main():
    symbols_usdt = data.get_symbols(currency="USDT")
    start = utils.unix_n_hours_ago_ms(3)
    end = utils.unix_now_ms()

    for symbol in symbols_usdt:
        hist = data.get_price_history(symbol, "1m", start, end)
        if not hist:
            continue
        open_prices = [float(row[1]) for row in hist]
        chunks = np.array_split(open_prices, 10)
        sums = [sum(chunk) for chunk in chunks]
        if utils.is_almost_non_descending(sums, 2):
            print(f"ALERT: {symbol}")


if __name__ == "__main__":
    main()


# plt.plot(list(range(1, len(open_prices) + 1)), open_prices, color="red")
# plt.show()
