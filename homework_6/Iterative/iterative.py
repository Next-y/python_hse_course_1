def _merge(source, buffer, low, mid, high):
    i, j = low, mid
    for dest in range(low, high):
        if j == high or (i < mid and source[i] <= source[j]):
            buffer[dest] = source[i]
            i += 1
        else:
            buffer[dest] = source[j]
            j += 1


def mergesort(nums):
    source = nums.copy()
    n = len(source)
    buffer = [None] * n
    width = 1
    while width < n:
        for low in range(0, n, 2 * width):
            mid = min(low + width, n)
            high = min(low + 2 * width, n)
            _merge(source, buffer, low, mid, high)
        source, buffer = buffer, source
        width *= 2
    return source


def quicksort(nums):
    values = nums.copy()
    if len(values) < 2:
        return values

    stack = [(0, len(values) - 1)]
    while stack:
        low, high = stack.pop()
        pivot = values[(low + high) // 2]
        i, j = low, high
        while i <= j:
            while values[i] < pivot:
                i += 1
            while values[j] > pivot:
                j -= 1
            if i <= j:
                values[i], values[j] = values[j], values[i]
                i += 1
                j -= 1

        left, right = (low, j), (i, high)
        if j - low >= high - i:
            larger, smaller = left, right
        else:
            larger, smaller = right, left
        for start, end in (larger, smaller):
            if start < end:
                stack.append((start, end))
    return values


if __name__ == "__main__":
    nums = [6, 2, 5, 3, 1, 4, 3]
    print("Вход", nums)
    print("mergesort", mergesort(nums))
    print("quicksort", quicksort(nums))
