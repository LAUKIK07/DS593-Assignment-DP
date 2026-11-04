
from client import avg, count, count0, _pretty_print
import math

# Every query consumes epsilon = 0.5
EPSILON = 0.5

class BudgetTracker:

    def __init__(self, budget):
        if not math.isfinite(budget) or budget < 0:
            raise ValueError("Budget must be finite and nonnegative")
        self.budget = budget

    def check_and_update_budget(self):
        # Reject queries that exceed the remaining budget.
        if self.budget < EPSILON:
            raise ValueError("Out of budget")

        # Deduct the privacy cost of the query.
        self.budget -= EPSILON
        return True

    def avg(self, group_by, averaged_column):
        self.check_and_update_budget()
        return avg(group_by, averaged_column, True)

    def count(self, group_by):
        self.check_and_update_budget()
        return count(group_by, True)

    def count0(self, group_by):
        self.check_and_update_budget()
        return count0(group_by, True)


if __name__ == "__main__":

    # Starting budget = 2.0
    tracker = BudgetTracker(2.0)

    # These four queries should succeed.
    _pretty_print(*tracker.avg(["programming"], "age"))
    _pretty_print(*tracker.count(["age", "music"]))
    _pretty_print(*tracker.count0(["programming"]))
    _pretty_print(*tracker.count(["programming"]))

    # This fifth query should fail.
    _pretty_print(*tracker.avg(["sport"], "age"))
