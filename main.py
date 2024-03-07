def pagination(
        current_page: int, total_pages: int, boundaries: int = 0, around: int = 0
) -> None:
    if not validate_data(current_page, total_pages, boundaries, around):
        return

    if total_pages < (boundaries + around) * 2:
        result = " ".join(str(page) for page in range(1, total_pages + 1))
        print(result)
        return

    start_around = max(1, current_page - around)
    end_around = min(total_pages, current_page + around)
    result = ""

    # adding boundary at the beginning
    result += add_pages_in_range(start=1, end=boundaries + 1)

    # adding ... before start_around if needed
    if start_around > boundaries + 1:
        result += "... "

    # adding current page with around
    if boundaries >= start_around:
        result += add_pages_in_range(start=boundaries + 1, end=end_around + 1)
    else:
        result += add_pages_in_range(
            start=min(start_around, total_pages - boundaries + 1),
            end=end_around + 1)

    # adding ... after end_around if needed
    if end_around < total_pages - boundaries:
        result += "... "

    # adding boundary at the end
    result += add_pages_in_range(
        start=max(total_pages - boundaries, end_around) + 1,
        end=total_pages + 1
    )

    print(result.strip())


def validate_data(current_page: int, total_pages: int, boundaries: int, around: int) -> bool:
    for arg_name, value in locals().items():
        if not isinstance(value, int):
            print(f"{arg_name} is not an integer")
            return False

    conditions = {
        "Current page should be greater than 1": current_page < 1,
        "Current page cannot be greater than total_pages": current_page > total_pages,
        "Boundaries could not be less then 0": boundaries < 0,
        "Around could not be less then 0": around < 0
    }

    for message, condition in conditions.items():
        if condition:
            print(message)
            return False
    return True


def add_pages_in_range(start: int, end: int) -> str:
    result = ""
    for page in range(start, end):
        result += str(page) + " "
    return result


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
