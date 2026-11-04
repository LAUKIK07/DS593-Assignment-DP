
from client import count, _pretty_print
from matplotlib import pyplot
import numpy as np
import sys
import math

# Return a random sample from a Laplace distribution.
def laplace(mu, b):
    return np.random.laplace(mu, b)

# Return a noised histogram that is epsilon-DP.
def dp_histogram(epsilon):
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("Epsilon must be finite and positive")

    # Add/remove-one neighboring datasets:
    # One person's data affects exactly one histogram bin.
    sensitivity = 1
    mu = 0
    b = sensitivity / epsilon

    # This follows the assignment's returned-bin stencil. A formal end-to-end
    # DP release also requires public, fixed bins, including empty bins: adding
    # noise to counts alone does not protect data-dependent group labels.
    # Get the exact histogram without noise.
    headers, rows = count(["age", "music"], False)

    noised_rows = []
    for age, music, value in rows:
        noise = laplace(mu, b)
        noised_value = round(int(value) + noise)

        noised_rows.append((age, music, noised_value))

    return headers, noised_rows

# Plot the distribution of the first histogram count.
def plot(epsilon):
    ITERATIONS = 150
    d = {}

    for i in range(ITERATIONS):
        headers, rows = dp_histogram(epsilon)
        value = round(rows[0][-1])
        d[value] = d.get(value, 0) + 1

    vmin, vmax = min(d.keys()) - 3, max(d.keys()) + 3
    xs = list(range(vmin, vmax + 1))
    ys = [d.get(x, 0) / ITERATIONS for x in xs]

    pyplot.figure()
    pyplot.plot(xs, ys, 'o-', drawstyle='steps-mid')
    pyplot.xlabel("Count value")
    pyplot.ylabel("Frequency")
    pyplot.title(f"DP Histogram: epsilon = {epsilon}")
    pyplot.savefig("dp-plot.png")
    pyplot.close()

if __name__ == "__main__":
    epsilon = 0.5

    if len(sys.argv) > 1:
        epsilon = float(sys.argv[1])

    print("Using epsilon =", epsilon)

    headers, rows = dp_histogram(epsilon)
    _pretty_print(headers, rows)

    print("Plotting, this may take a minute ...")
    plot(epsilon)
    print("Plot saved at 'dp-plot.png'")
