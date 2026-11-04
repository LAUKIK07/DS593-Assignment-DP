
from client import avg, count, count0, _pretty_print
from dp import dp_histogram

# Estimate the original aggregate using repeated noisy queries.
def expose(query_func):
    headers, many_results = None, []

    print("Making 200 queries with noise. This may take a minute...")

    for i in range(200):
        current_headers, results = query_func()
        if headers is None:
            headers = current_headers
        elif current_headers != headers:
            raise ValueError("Query headers changed between releases")
        keyed_results = {tuple(row[:-1]): float(row[-1]) for row in results}
        if len(keyed_results) != len(results):
            raise ValueError("Duplicate group labels in a query result")
        if many_results and keyed_results.keys() != many_results[0].keys():
            raise ValueError("Query groups changed between releases")
        many_results.append(keyed_results)

    # Combine the noisy results.
    exposed_result = []
    num_iterations = len(many_results)
    for labels in many_results[0]:
        # Each query returns a noisy version of the same value.
        # Averaging reduces the effect of zero-mean noise.
        total = 0

        for i in range(num_iterations):
            total += many_results[i][labels]

        value = total / num_iterations

        # Keep the estimates as floats so both averages and
        # histogram counts can be handled by the same function.
        exposed_result.append(labels + (value,))

    return headers, exposed_result


if __name__ == "__main__":

    print("TESTING: the two histograms should be (almost) equal.\n")

    print("Non-noised histogram (from part 1):")
    headers, result = count(["age", "music"], False)
    _pretty_print(headers, result)

    print("\nExposed histogram:")
    headers, result = expose(lambda: dp_histogram(0.5))
    _pretty_print(headers, result)

    # Question 9: Expose average ages.
    print("\nExposing average age by programming experience:")
    headers, result = expose(
        lambda: avg(["programming"], "age", True)
    )
    _pretty_print(headers, result)

    # Question 10: Expose counts.
    print("\nExposing counts by age group and programming experience:")
    headers, result = expose(
        lambda: count0(["agegroup", "programming"], True)
    )
    _pretty_print(headers, result)
