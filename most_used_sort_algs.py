import itertools


def merge_sort(lst: list) -> None:
    def merge(initial: list, left: list, right: list) -> None:
        left_idx = right_idx = init_idx = 0

        while left_idx < len(left) and right_idx < len(right):
            if left[left_idx] < right[right_idx]:
                initial[init_idx] = left[left_idx]
                left_idx += 1
            else:
                initial[init_idx] = right[right_idx]
                right_idx += 1
            init_idx += 1

        while left_idx < len(left):
            initial[init_idx] = left[left_idx]
            left_idx += 1
            init_idx += 1
        while right_idx < len(right):
            initial[init_idx] = right[right_idx]
            right_idx += 1
            init_idx += 1

    if (list_length := len(lst)) == 1:
        return

    partition_on = list_length // 2
    left, right = lst[partition_on:], lst[:partition_on]

    merge_sort(left)
    merge_sort(right)

    merge(lst, left, right)


def quick_sort(lst: list) -> None:
    def quick_sort_r(lst: list, start: int, end: int) -> None:
        if start >= end:
            return

        pivot = partition(lst, start, end)
        quick_sort_r(lst, start, pivot - 1)
        quick_sort_r(lst, pivot + 1, end)

    def partition(lst: list, start: int, end: int) -> int:
        pivot = lst[end]
        low_idx = start

        for i in range(start, end):
            if lst[i] < pivot:
                lst[low_idx], lst[i] = lst[i], lst[low_idx]
                low_idx += 1

        lst[end], lst[low_idx] = lst[low_idx], lst[end]
        return low_idx

    quick_sort_r(lst, 0, len(lst) - 1)


def heap_sort(lst: list) -> None:
    def heapify(lst: list, n: int, i: int) -> None:
        largest_idx = i
        left_child_idx = i * 2 + 1
        right_child_idx = left_child_idx + 1

        if left_child_idx < n and lst[largest_idx] < lst[left_child_idx]:
            largest_idx = left_child_idx

        if right_child_idx < n and lst[largest_idx] < lst[right_child_idx]:
            largest_idx = right_child_idx

        if largest_idx != i:
            lst[i], lst[largest_idx] = lst[largest_idx], lst[i]
            heapify(lst, n, largest_idx)

    list_length = len(lst)

    for i in range(list_length // 2 - 1, -1, -1):
        heapify(lst, list_length, i)

    for i in range(list_length - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        heapify(lst, i, 0)


def bubble_sort(lst: list) -> None:
    it_count: int = 0
    swapped: bool = True
    list_length: int = len(lst)

    while swapped:
        swapped = False
        for j in range(list_length - it_count - 1):
            if lst[j + 1] < lst[j]:
                lst[j + 1], lst[j] = lst[j], lst[j + 1]
                swapped = True
        it_count += 1

        if not swapped:
            break
