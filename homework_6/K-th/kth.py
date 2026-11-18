from random import randint


def find_kth_largest(nums, k):
    if not isinstance(k, int):
        raise TypeError("k должно быть целым числом")
    if not 1 <= k <= len(nums):
        raise ValueError("k должно быть от 1 до длины списка включительно")

    values = nums.copy()
    target = k - 1
    low, high = 0, len(values) - 1
    while low < high:
        pivot = values[randint(low, high)]
        first = scan = low
        last = high
        while scan <= last:
            if values[scan] > pivot:
                values[first], values[scan] = values[scan], values[first]
                first += 1
                scan += 1
            elif values[scan] < pivot:
                values[scan], values[last] = values[last], values[scan]
                last -= 1
            else:
                scan += 1

        if target < first:
            high = first - 1
        elif target > last:
            low = last + 1
        else:
            return pivot
    return values[low]


if __name__ == "__main__":
    for nums, k in [([3, 2, 1, 5, 6, 4], 2), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)]:
        print(f"nums = {nums}, k = {k} -> {find_kth_largest(nums, k)}")
