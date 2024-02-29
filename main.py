def pagination(
        current_page: int, total_pages: int, boundaries: int = 0, around: int = 0
) -> None:
    if not validate_data(current_page, total_pages, boundaries, around):
        return

    result = ""
    start_around = max(1, current_page - around)
    end_around = min(total_pages, current_page + around)

    # adding boundary at start
    for page in range(1, min(total_pages, boundaries) + 1):
        if page < start_around or page > end_around:
            result += str(page) + " "

    # adding ... before start_around if needed
    if start_around > boundaries + 1:
        result += "... "

    # adding current page with around
    for page in range(start_around, end_around + 1):
        result += str(page) + " "

    # adding ... after end_around if needed
    if end_around < total_pages - boundaries:
        result += "... "

    # adding boundary at the end
    for page in range(max(total_pages - boundaries, end_around) + 1, total_pages + 1):
        result += str(page) + " "

    print(result)


def validate_data(current_page: int, total_pages: int, boundaries: int, around: int):
    """Checking, if arguments are valid before creating result"""
    conditions = {
        "Current page should be integer": not isinstance(current_page, int),
        "Total pages should be integer": not isinstance(total_pages, int),
        "Boundaries should be integer": not isinstance(boundaries, int),
        "Around should be integer": not isinstance(around, int),
        "Current page should be greater than 1": current_page < 1,
        "Current page cannot be greater than total_pages": current_page > total_pages,
        "Boundaries could not be less then 0": boundaries < 0,
        "Around could not be less then 0": around < 0,
        "Boundaries should not be greater than total_pages.": boundaries > total_pages,
        "Around should not be greater than total_pages.": around > total_pages
    }

    for message, condition in conditions.items():
        if condition:
            print(message)
            return
    return True


if __name__ == "__main__":
    try:
        pagination(
            current_page=int(input("Current page: ")),
            total_pages=int(input("Total pages: ")),
            boundaries=int(input("Boundaries: ")),
            around=int(input("Around: "))
        )
    except ValueError:
        print("Invalid value type. Use numbers only, please.")
