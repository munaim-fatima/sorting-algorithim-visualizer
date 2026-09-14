def bubble_sort(array):
    arr = array.copy()
    steps = []
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # Comparison
            steps.append({
                "array": arr.copy(),
                "comparing": [j, j + 1],
                "swapping": [],
                "sorted": list(range(n - i, n))
            })
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                steps.append({
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [j, j + 1],
                    "sorted": list(range(n - i, n))
                })
        steps.append({
            "array": arr.copy(),
            "comparing": [],
            "swapping": [],
            "sorted": list(range(n - i - 1, n))
        })
        if not swapped:
            break
    return steps
def selection_sort(array):
    arr = array.copy()
    steps = []
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            # Comparison
            steps.append({
                "array": arr.copy(),
                "comparing": [min_index, j],
                "swapping": [],
                "sorted": list(range(i))
            })
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            steps.append({
                "array": arr.copy(),
                "comparing": [],
                "swapping": [i, min_index],
                "sorted": list(range(i))
            })
        steps.append({
            "array": arr.copy(),
            "comparing": [],
            "swapping": [],
            "sorted": list(range(i + 1))
        })
    return steps
def insertion_sort(array):
    arr = array.copy()
    steps = []
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        steps.append({
            "array": arr.copy(),
            "comparing": [i],
            "swapping": [],
            "sorted": list(range(i))
        })
        while j >= 0:
            # Comparison
            steps.append({
                "array": arr.copy(),
                "comparing": [j, j + 1],
                "swapping": [],
                "sorted": list(range(i))
            })
            if arr[j] > key:        
                arr[j + 1] = arr[j]
                steps.append({
                    "array": arr.copy(),
                    "comparing": [],
                    "swapping": [j, j + 1],
                    "sorted": list(range(i))
                })
                j -= 1
            else:
                break
        arr[j + 1] = key
        steps.append({
            "array": arr.copy(),
            "comparing": [],
            "swapping": [],
            "sorted": list(range(i + 1))
        })
        
    steps.append({
        "array": arr.copy(),
        "comparing": [],
        "swapping": [],
        "sorted": list(range(n))
    })
    return steps
def get_sorting_steps(array, algorithm):
    if algorithm == "Bubble Sort":
        return bubble_sort(array)
    elif algorithm == "Selection Sort":
        return selection_sort(array)
    elif algorithm == "Insertion Sort":
        return insertion_sort(array)
    else:
        return []