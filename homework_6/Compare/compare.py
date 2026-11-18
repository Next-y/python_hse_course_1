from functools import wraps
from statistics import median
from time import perf_counter_ns


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()
        result = func(*args, **kwargs)
        elapsed = perf_counter_ns() - start
        return result, elapsed

    return wrapper


def mergesort(nums):
    if len(nums) < 2:
        return nums.copy()

    mid = len(nums) // 2
    left = mergesort(nums[:mid])
    right = mergesort(nums[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _partition(values, low, high):
    pivot = values[high]
    first = scan = low
    last = high
    while scan <= last:
        if values[scan] < pivot:
            values[first], values[scan] = values[scan], values[first]
            first += 1
            scan += 1
        elif values[scan] > pivot:
            values[scan], values[last] = values[last], values[scan]
            last -= 1
        else:
            scan += 1
    return first, last


def quicksort(nums):
    values = nums.copy()

    def sort(low, high):
        while low < high:
            first, last = _partition(values, low, high)
            if first - low < high - last:
                sort(low, first - 1)
                low = last + 1
            else:
                sort(last + 1, high)
                high = first - 1

    sort(0, len(values) - 1)
    return values


def benchmark(size=2000, repeats=5):
    cases = [
        ("По возрастанию", list(range(size))),
        ("Все равны", [7] * size),
    ]
    print(f"n = {size}, число запусков = {repeats}")
    for label, nums in cases:
        print(label)
        for sort in (mergesort, quicksort):
            measure = timed(sort)
            times = []
            for _ in range(repeats):
                _, elapsed = measure(nums)
                times.append(elapsed)
            print(f"  {sort.__name__}: {median(times) / 1_000_000:.3f} мс")


if __name__ == "__main__":
    benchmark()
