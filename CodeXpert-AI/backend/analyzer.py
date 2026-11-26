import re


def analyze_code(language, code):

    if not code.strip():
        return {
            "success": False,
            "error": "Please enter some code to analyze."
        }

    lines = code.splitlines()

    clean_lines = [
        line for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]

    # Detect loop nesting
    loop_indents = []
    loop_count = 0
    max_nested_depth = 0

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        while loop_indents and indent <= loop_indents[-1]:
            loop_indents.pop()

        if re.match(r'^(for|while)\b', stripped):
            loop_count += 1
            loop_indents.append(indent)

            max_nested_depth = max(
                max_nested_depth,
                len(loop_indents)
            )

    # Detect sorting
    sorting = bool(re.search(
        r'\bsorted\s*\(|\.\s*sort\s*\(',
        code
    ))

    # Detect logarithmic loops
    logarithmic_loop = bool(re.search(
        r'\bwhile\s+.*:',
        code
    ) and re.search(
        r'(\w+)\s*=\s*\1\s*//\s*2|'
        r'(\w+)\s*//=\s*2|'
        r'(\w+)\s*=\s*\1\s*/\s*2',
        code
    ))

    # Detect iterative binary search
    binary_search = bool(re.search(
        r'while\s+.*(?:low\s*<=?\s*high|'
        r'left\s*<=?\s*right|'
        r'start\s*<=?\s*end)',
        code,
        re.IGNORECASE
    ))
    # Detect optimized bubble sort
    optimized_bubble_sort = bool(
    re.search(r'\bswapped\b', code)
    and re.search(r'\bbreak\b', code)
    and loop_count >= 2
)
    # Detect recursive functions
    recursive_functions = []

    function_matches = list(re.finditer(
        r'def\s+(\w+)\s*\([^)]*\)\s*:',
        code
    ))
    # Detect insertion sort
    insertion_sort_pattern = bool(
    re.search(r'\bkey\s*=', code)
    and re.search(r'\bwhile\b', code)
    and re.search(r'\bj\s*[-+]=\s*1', code)
)

    # Detect selection sort
    selection_sort_pattern = bool(
    re.search(r'\bmin_index\b|\bmin_idx\b', code)
    and re.search(r'\bfor\b', code)
)

    # Detect merge sort
    merge_sort_pattern = bool(
    re.search(r'\bmerge\b', code)
    and re.search(r'\bmid\b', code)
)
    # Detect quick sort
    quick_sort_pattern = bool(
    re.search(r'\bpivot\s*=', code)
    and re.search(r'\bquick_sort\s*\(', code)
    and re.search(r'\breturn\b', code)
)
    # Detect heap sort
    heap_sort_pattern = bool(
    re.search(r'\bheap_sort\s*\(', code)
    and re.search(r'\bheapify\s*\(', code)
    and re.search(r'\bleft\s*=\s*2\s*\*\s*i\s*\+\s*1', code)
    and re.search(r'\bright\s*=\s*2\s*\*\s*i\s*\+\s*2', code)
)
    # Detect counting sort
    counting_sort_pattern = bool(
    re.search(r'\bcounting_sort\s*\(', code)
    and re.search(r'\bcount\s*=\s*\[0\]', code)
    and re.search(r'\bcount\s*\[\s*\w+\s*\]\s*\+=\s*1', code)
    and re.search(r'\bmax\s*\(', code)
)
    # Detect radix sort
    radix_sort_pattern = bool(
    re.search(r'\bradix_sort\s*\(', code)
    and re.search(r'\bcounting_sort_by_digit\s*\(', code)
    and re.search(r'\bexp\s*\*=\s*10', code)
    and re.search(r'\bmax_value\s*//\s*exp', code)
)
    # Detect bucket sort
    bucket_sort_pattern = bool(
    re.search(r'\bbucket_sort\s*\(', code)
    and re.search(r'\bbuckets\s*=\s*\[', code)
    and re.search(r'\bbuckets\s*\[[^\]]+\]\.append', code)
    and re.search(r'\bbucket\.sort\s*\(', code)
)
    # Detect shell sort
    shell_sort_pattern = bool(
    re.search(r'\bshell_sort\s*\(', code)
    and re.search(r'\bgap\s*=\s*\w+\s*//\s*2', code)
    and re.search(r'\bgap\s*//=\s*2', code)
    and re.search(r'\bwhile\s+gap\s*>\s*0', code)
)
    # Detect Tim Sort
    tim_sort_pattern = bool(
    re.search(r'\bsorted\s*\(', code)
    or re.search(r'\.sort\s*\(', code)
)
    # Detect nested-loop pair generation
    nested_pair_generation = bool(
    re.search(r'\bpairs\s*=\s*\[\s*\]', code)
    and re.search(r'\bfor\s+\w+\s+in\s+range\s*\(', code)
    and re.search(r'\.append\s*\(\s*\(', code)
    and re.search(r'\bpairs\.append\s*\(', code)
    and loop_count >= 2
)
   
    # Detect matrix multiplication
    matrix_multiplication_pattern = bool(
    re.search(r'\bmatrix_multiply\s*\(', code)
    and re.search(r'\brows_A\s*=', code)
    and re.search(r'\bcols_B\s*=', code)
    and re.search(r'\bresult\s*=\s*\[\[', code)
    and loop_count >= 3
)
    # Detect matrix transpose
    matrix_transpose_pattern = bool(
    re.search(r'\btranspose_matrix\s*\(', code)
    and re.search(r'\brows\s*=\s*len\s*\(\s*matrix\s*\)', code)
    and re.search(r'\bcols\s*=\s*len\s*\(\s*matrix\s*\[\s*0\s*\]\s*\)', code)
    and re.search(r'\bresult\s*=\s*\[\[', code)
    and re.search(r'\bresult\s*\[\s*j\s*\]\s*\[\s*i\s*\]\s*=', code)
)
    # Detect matrix addition
    matrix_addition_pattern = bool(
      re.search(r'\bmatrix_addition\s*\(', code)
      and re.search(r'\brows\s*=\s*len\s*\(\s*A\s*\)', code)
      and re.search(r'\bcols\s*=\s*len\s*\(\s*A\s*\[\s*0\s*\]\s*\)', code)
      and re.search(r'\bresult\s*=\s*\[\[', code)
      and re.search(
        r'result\s*\[\s*i\s*\]\s*\[\s*j\s*\]\s*=\s*A\s*\[\s*i\s*\]\s*\[\s*j\s*\]\s*\+\s*B\s*\[\s*i\s*\]\s*\[\s*j\s*\]',
        code
    )
)
    # Detect spiral matrix traversal
    spiral_matrix_pattern = bool(
       re.search(r'\bspiral_order\s*\(', code)
       and re.search(r'\bresult\s*=\s*\[\s*\]', code)
       and re.search(r'\bmatrix\.pop\s*\(\s*0\s*\)', code)
       and re.search(r'\brow\.pop\s*\(\s*\)', code)
       and re.search(r'\bresult\s*\+=', code)
)
    # Detect Inorder Tree Traversal
    inorder_traversal_pattern = bool(
      re.search(r'\bdef\s+inorder\s*\(', code)
      and re.search(r'\binorder\s*\(\s*root\.left\s*\)', code)
      and re.search(r'\binorder\s*\(\s*root\.right\s*\)', code)
      and re.search(r'\broot\.value\b', code)
)
    # Detect Preorder Tree Traversal
    preorder_traversal_pattern = bool(
    re.search(r'\bdef\s+preorder\s*\(', code)
    and re.search(r'\bpreorder\s*\(\s*root\.left\s*\)', code)
    and re.search(r'\bpreorder\s*\(\s*root\.right\s*\)', code)
    and re.search(r'\broot\.value\b', code)
)
    for i, match in enumerate(function_matches):

        function_name = match.group(1)

        start = match.end()

        end = (
            function_matches[i + 1].start()
            if i + 1 < len(function_matches)
            else len(code)
        )

        function_body = code[start:end]

        calls = list(re.finditer(
            rf'\b{re.escape(function_name)}\s*\(',
            function_body
        ))

        if calls:
            recursive_functions.append({
                "name": function_name,
                "calls": len(calls),
                "body": function_body
            })

    recursive = bool(recursive_functions)

# Detect recursive binary search
    recursive_binary_search = any(
    item["calls"] >= 1
    and re.search(r'\bmid\b', item["body"])
    and re.search(r'\barr\s*\[\s*mid\s*\]', item["body"])
    and re.search(r'\b(?:low|start)\b', item["body"])
    and re.search(r'\b(?:high|end)\b', item["body"])
    for item in recursive_functions
) 

    # Detect Fibonacci-like exponential recursion
    exponential_recursion = any(
        item["calls"] >= 2
        and re.search(
            rf'return\s+.*\b{re.escape(item["name"])}\s*\(.*\)'
            rf'.*\b{re.escape(item["name"])}\s*\(',
            item["body"]
        )
        for item in recursive_functions
    )

    # Detect divide-and-conquer recursion
    divide_conquer_recursion = any(
        item["calls"] >= 2
        and re.search(r'\[\s*:\s*\w+\s*\]', item["body"])
        and re.search(r'\[\s*\w+\s*:', item["body"])
        for item in recursive_functions
    )
    # Detect string slicing
    string_slicing = bool(
    re.search(r'\[\s*:\s*:\s*-?1\s*\]', code)
    )
    # Detect string concatenation inside a loop
    string_concatenation = bool(
    loop_count > 0
    and re.search(
        r"""(?s)\b(?P<var>\w+)\s*=\s*(['"])\2.*?\b(?P=var)\s*\+=""",
        code
    )
)
# Detect list comprehension
    list_comprehension = bool(
    re.search(
        r'\[[^\]]*\bfor\s+\w+\s+in\b[^\]]*\]',
        code
    )
)    
# Detect dictionary comprehension
    dictionary_comprehension = bool(
    re.search(
        r'\{[^{}]*:\s*[^{}]*\bfor\s+\w+\s+in\b[^{}]*\}',
        code
    )
)
    # Detect set comprehension
    set_comprehension = bool(
    re.search(
        r'\{(?![^{}]*:)[^{}]*\bfor\s+\w+\s+in\b[^{}]*\}',
        code
    )
)
    # Detect nested list comprehension
    nested_list_comprehension = bool(
    re.search(
        r'\[[^\]]*\bfor\s+\w+\s+in\b[^\]]*\bfor\s+\w+\s+in\b[^\]]*\]',
        code
    )
)
    # Detect list comprehension with membership check
    list_membership_comprehension = bool(
    re.search(
        r'\[[^\]]*\bfor\s+\w+\s+in\b[^\]]*\bif\s+\w+\s+in\s+\w+',
        code
    )
)
    # Detect nested dictionary comprehension
    nested_dictionary_comprehension = bool(
    re.search(
        r'\{[^{}]*:\s*\{[^{}]*\bfor\s+\w+\s+in\b[^{}]*\}[^{}]*\bfor\s+\w+\s+in\b[^{}]*\}',
        code
    )
)
   # Detect nested set comprehension
    nested_set_comprehension = bool(
    re.search(
        r'\{[^{}]*\bfor\s+\w+\s+in\b[^{}]*\bfor\s+\w+\s+in\b[^{}]*\}',
        code
    )
)
    # Detect generator expression
    generator_expression = bool(
    re.search(
        r'\([^()]*\bfor\s+\w+\s+in\b[^()]*\)',
        code
    )
)
    # Detect nested generator expression
    nested_generator_expression = bool(
    re.search(
        r'\b(?:sum|max|min)\s*\(\s*(?:sum|max|min)\s*\([^)]*\)\s+for\s+\w+\s+in\b',
        code
    )
)   
    if matrix_addition_pattern:
     time_complexity = "O(n × m)"

    elif matrix_transpose_pattern:
     time_complexity = "O(n × m)"
    elif list_membership_comprehension:
     time_complexity = "O(n × m)"

    elif merge_sort_pattern:
     time_complexity = "O(n log n)"

    elif tim_sort_pattern:
     time_complexity = "O(n log n)"
    elif shell_sort_pattern:
     time_complexity = "O(n log n) - estimated"

    elif bucket_sort_pattern:
     time_complexity = "O(n) - average"
    elif radix_sort_pattern:
     time_complexity = "O(d × n)"

    elif counting_sort_pattern:
      time_complexity = "O(n + k)"

    elif heap_sort_pattern:
     time_complexity = "O(n log n)"
    elif quick_sort_pattern:
     time_complexity = "O(n log n) - average"
    elif max_nested_depth >= 3:
     time_complexity = "O(n³)"

    elif max_nested_depth == 2:
        time_complexity = "O(n²)"

    elif divide_conquer_recursion or sorting:
        time_complexity = "O(n log n)"
    elif inorder_traversal_pattern:
      time_complexity = "O(n)"
    elif preorder_traversal_pattern:
      time_complexity = "O(n)"  
    elif exponential_recursion:
        time_complexity = "O(2^n) - estimated"

    elif recursive_binary_search or binary_search or logarithmic_loop:
        time_complexity = "O(log n) - estimated"

    elif recursive:
        time_complexity = "O(n) - estimated"
    elif string_slicing:
     time_complexity = "O(n)"

    elif string_concatenation:
     time_complexity = "O(n²) - estimated"
    elif nested_list_comprehension or nested_dictionary_comprehension or nested_set_comprehension:
     time_complexity = "O(n²)"
    elif nested_generator_expression:
     time_complexity = "O(n²)" 
    elif generator_expression:
      time_complexity = "O(n)" 
    elif list_comprehension or dictionary_comprehension or set_comprehension:
     time_complexity = "O(n)"
    elif loop_count > 0:
     time_complexity = "O(n)"
    else:
        time_complexity = "O(1)"
    # Best-case and worst-case time complexity
    # Detect linear search
    # Detect linear search
    linear_search_pattern = bool(
    re.search(r'\bfor\s+\w+\s+in\s+range\s*\(', code)
    and re.search(r'\bif\b[^\n]*==', code)
    and re.search(r'\breturn\b', code)
)
    best_case_time_complexity = time_complexity
    worst_case_time_complexity = time_complexity

    short_circuit_iteration = bool(
    re.search(r'\b(?:any|all)\s*\(', code)
)
   #Detect iterative binary search
    binary_search_best_case = bool(
    re.search(r'\bwhile\b', code)
    and re.search(r'\bmid\b', code)
    and re.search(r'\b(?:low|left)\s*=', code)
    and re.search(r'\b(?:high|right)\s*=', code)
)
    best_case_time_complexity = time_complexity
    worst_case_time_complexity = time_complexity

    short_circuit_iteration = bool(
    re.search(r'\b(?:any|all)\s*\(', code)
)  
    if inorder_traversal_pattern or preorder_traversal_pattern:
     best_case_time_complexity = "O(n)"
     worst_case_time_complexity = "O(n)"
    elif matrix_addition_pattern:
     best_case_time_complexity = "O(n × m)"
     worst_case_time_complexity = "O(n × m)"
    elif matrix_transpose_pattern:
     best_case_time_complexity = "O(n × m)"
     worst_case_time_complexity = "O(n × m)"

    elif list_membership_comprehension:
     best_case_time_complexity = "O(n × m)"
     worst_case_time_complexity = "O(n × m)"
    elif nested_pair_generation:
     best_case_time_complexity = "O(n²)"
     worst_case_time_complexity = "O(n²)"
 
    elif tim_sort_pattern:
     best_case_time_complexity = "O(n)"
     worst_case_time_complexity = "O(n log n)" 
    elif shell_sort_pattern:
      best_case_time_complexity = "O(n log n)"
      worst_case_time_complexity = "O(n²)"
    elif bucket_sort_pattern:
     best_case_time_complexity = "O(n)"
     worst_case_time_complexity = "O(n²)"
    elif radix_sort_pattern:
     best_case_time_complexity = "O(d × n)"
     worst_case_time_complexity = "O(d × n)"
    elif counting_sort_pattern:
     best_case_time_complexity = "O(n + k)"
     worst_case_time_complexity = "O(n + k)"

    elif heap_sort_pattern:
     best_case_time_complexity = "O(n log n)"
     worst_case_time_complexity = "O(n log n)"

    elif merge_sort_pattern:
     best_case_time_complexity = "O(n log n)"
     worst_case_time_complexity = "O(n log n)"

    elif quick_sort_pattern:
     best_case_time_complexity = "O(n log n)"
     worst_case_time_complexity = "O(n²)"
   

    elif linear_search_pattern:
     best_case_time_complexity = "O(1)"
     worst_case_time_complexity = "O(n)"

    elif binary_search_best_case:
     best_case_time_complexity = "O(1)"
     worst_case_time_complexity = "O(log n)"

    elif optimized_bubble_sort:
     best_case_time_complexity = "O(n)"
     worst_case_time_complexity = "O(n²)"

    elif insertion_sort_pattern:
     best_case_time_complexity = "O(n)"
     worst_case_time_complexity = "O(n²)"

    elif selection_sort_pattern:
     best_case_time_complexity = "O(n²)"
     worst_case_time_complexity = "O(n²)"

    elif short_circuit_iteration:
     best_case_time_complexity = "O(1)"
     worst_case_time_complexity = "O(n)"

   # Space complexity detection
     
    set_creation = bool(re.search(
        r'\b\w+\s*=\s*set\s*\(',
        code
    ))

    list_creation = bool(re.search(
        r'\b\w+\s*=\s*\[\s*\]|'
        r'\.append\s*\(',
        code
    ))

    dictionary_creation = bool(re.search(
        r'\b\w+\s*=\s*\{\s*\}',
        code
    ))

    matrix_creation = bool(re.search(
        r'\bmatrix\s*=\s*\[\s*\]|'
        r'\bresult\s*=\s*\[\s*\][\s\S]*?'
        r'\brow\s*=\s*\[\s*\][\s\S]*?'
        r'\.append\s*\(',
        code
    ))
    sorted_creation = bool(
    re.search(r'\bsorted\s*\(', code)
    or re.search(r'\.\s*sort\s*\(', code)
)   
    if spiral_matrix_pattern:
     space_complexity = "O(n²)"
    elif matrix_addition_pattern:
     space_complexity = "O(n × m)"
 
    elif matrix_transpose_pattern:
     space_complexity = "O(n × m)"

    elif matrix_multiplication_pattern:
     space_complexity = "O(n²)"
    elif nested_pair_generation:
     space_complexity = "O(n²)"
    elif heap_sort_pattern:
     space_complexity = "O(log n)"
    elif quick_sort_pattern:
     space_complexity = "O(log n) - average"
    elif radix_sort_pattern:
     space_complexity = "O(n)"

    elif counting_sort_pattern and re.search(
     r'\bcount\s*=\s*\[0\]\s*\*\s*\(.*max.*\+?\s*1.*\)',
     code
) and re.search(r'\barr\s*\[\s*index\s*\]\s*=', code):
     space_complexity = "O(k)"

    elif counting_sort_pattern:
     space_complexity = "O(n + k)"
    elif matrix_creation or nested_list_comprehension or nested_dictionary_comprehension or nested_set_comprehension:
     space_complexity = "O(n²) - estimated"
    elif recursive_binary_search:
     space_complexity = "O(log n) - estimated"

    elif recursive or set_creation or list_creation or dictionary_creation or sorted_creation or string_slicing or string_concatenation or list_comprehension or dictionary_comprehension or set_comprehension:
     space_complexity = "O(n) - estimated"
    else:
     space_complexity = "O(1) - estimated"

    # Efficiency score

    if time_complexity == "O(1)":
        efficiency = 95

    elif time_complexity in (
        "O(n)",
        "O(log n) - estimated"
    ):
        efficiency = 80

    else:
        efficiency = 65

    # Suggestions

    suggestions = []

    if max_nested_depth >= 2:
        suggestions.append(
            "Review nested loops for possible optimization."
        )

    if sorting:
        suggestions.append(
            "Sorting operations generally take O(n log n) time."
        )
# Time complexity detection
    if recursive:
        suggestions.append(
            "Check recursion depth and repeated calculations."
        )

    if logarithmic_loop or binary_search or recursive_binary_search:
        suggestions.append(
            "The code contains a logarithmic search or loop pattern."
        )

    if not suggestions:
        suggestions.append(
            "Review the code for opportunities to improve readability."
        )

    return {
        "success": True,
        "language": language,
        "time_complexity": time_complexity,
        "best_case_time_complexity": best_case_time_complexity,
        "worst_case_time_complexity": worst_case_time_complexity,
        "space_complexity": space_complexity,
        "efficiency": efficiency,
        "lines_of_code": len(clean_lines),
        "code_quality": "Basic static analysis",
        "bottlenecks": suggestions,
        "suggestions": suggestions
    }