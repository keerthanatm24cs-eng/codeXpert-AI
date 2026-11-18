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

    # Detect recursive functions
    recursive_functions = []

    function_matches = list(re.finditer(
        r'def\s+(\w+)\s*\([^)]*\)\s*:',
        code
    ))

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
        and re.search(
            r'\b(?:low|left|start)\b',
            item["body"]
        )
        and re.search(
            r'\b(?:high|right|end)\b',
            item["body"]
        )
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

    # Time complexity detection

    if max_nested_depth >= 3:
        time_complexity = "O(n³)"

    elif max_nested_depth == 2:
        time_complexity = "O(n²)"

    elif divide_conquer_recursion or sorting:
        time_complexity = "O(n log n)"

    elif exponential_recursion:
        time_complexity = "O(2^n) - estimated"

    elif recursive_binary_search or binary_search or logarithmic_loop:
        time_complexity = "O(log n) - estimated"

    elif recursive:
        time_complexity = "O(n) - estimated"

    elif loop_count > 0:
        time_complexity = "O(n)"

    else:
        time_complexity = "O(1)"

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

    if matrix_creation:
        space_complexity = "O(n²) - estimated"

    elif recursive_binary_search:
        space_complexity = "O(log n) - estimated"

    elif recursive or set_creation or list_creation or dictionary_creation:
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
        "space_complexity": space_complexity,
        "efficiency": efficiency,
        "lines_of_code": len(clean_lines),
        "code_quality": "Basic static analysis",
        "bottlenecks": suggestions,
        "suggestions": suggestions
    }