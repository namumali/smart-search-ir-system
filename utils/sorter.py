"""
Merge Sort Implementation
Used for sorting search results by relevance score in descending order.
"""


def merge(left, right):
    """
    Merge two sorted lists into one sorted list (descending order).
    
    Args:
        left (list): First sorted list of result dictionaries.
        right (list): Second sorted list of result dictionaries.
        
    Returns:
        list: Merged sorted list.
    """
    result = []
    i = j = 0
    
    # Merge while both lists have elements
    while i < len(left) and j < len(right):
        # Compare by score (descending order - higher scores first)
        if left[i]['score'] >= right[j]['score']:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements from left list
    while i < len(left):
        result.append(left[i])
        i += 1
    
    # Add remaining elements from right list
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result


def merge_sort(arr):
    """
    Sort a list using merge sort algorithm (divide and conquer).
    Sorts in descending order based on the 'score' field of result dictionaries.
    
    Args:
        arr (list): List of result dictionaries, each containing at least a 'score' field.
        
    Returns:
        list: Sorted list in descending order of scores.
    """
    # Base case: list with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr
    
    # Divide: split the list into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Conquer: recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    
    # Combine: merge the sorted halves
    return merge(left_sorted, right_sorted)


def sort_results(results_list):
    """
    Sort search results in descending order based on their relevance score.
    
    Args:
        results_list (list): List of result dictionaries. Each dictionary should have:
            - 'doc_id': Document identifier
            - 'score': Relevance score (float)
            - Other metadata fields (title, file_path, etc.)
            
    Returns:
        list: Sorted list of results with highest scores first.
    """
    if not results_list:
        return []
    
    # Use merge sort to sort the results
    return merge_sort(results_list)
