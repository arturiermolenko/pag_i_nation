import io
import sys
import unittest


def pagination(
        current_page: int, total_pages: int, boundaries: int = 0, around: int = 0
) -> None:
    if not validation(current_page, total_pages, boundaries, around):
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
    for page in range(
            max(total_pages - boundaries, end_around) + 1, total_pages + 1
    ):
        result += str(page) + " "

    print(result)


def validation(current_page: int, total_pages: int, boundaries: int, around: int):
    """Checking, if arguments are valid before creating result"""
    if current_page < 1:
        print("Current page should be greater than 1")
        return
    elif current_page > total_pages:
        print("Current page cannot be greater than total_pages")
        return
    elif any([boundaries < 0, around < 0]):
        print("Parameters could not be less then 0")
        return
    elif boundaries > total_pages:
        print("Boundaries should not be greater than total_pages.")
        return
    elif around > total_pages:
        print("Around should not be greater than total_pages.")
        return

    return True


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, io.StringIO()

    def test_simple_pagination_1(self):
        pagination(current_page=5, total_pages=10, boundaries=2, around=1)
        test_result = "1 2 ... 4 5 6 ... 9 10"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_simple_pagination_2(self):
        pagination(current_page=4, total_pages=10, boundaries=2, around=1)
        test_result = "1 2 3 4 5 ... 9 10"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_simple_pagination_3(self):
        pagination(current_page=9, total_pages=10, boundaries=2, around=1)
        test_result = "1 2 ... 8 9 10"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_huge_total(self):
        pagination(current_page=2, total_pages=999999, boundaries=2, around=1)
        test_result = "1 2 3 ... 999998 999999"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_huge_boundaries(self):
        pagination(current_page=2, total_pages=10, boundaries=999999)
        test_result = "Boundaries should not be greater than total_pages."
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_huge_amount(self):
        pagination(current_page=2, total_pages=10,around=999999)
        test_result = "Around should not be greater than total_pages."
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_current_page_equals_null(self):
        pagination(current_page=0, total_pages=10)
        test_result = "Current page should be greater than 1"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_total_pages_equals_null(self):
        pagination(current_page=5, total_pages=0)
        test_result = "Current page cannot be greater than total_pages"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_current_page_greater_than_total_pages(self):
        pagination(current_page=5, total_pages=4)
        test_result = "Current page cannot be greater than total_pages"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_boundaries_less_than_null(self):
        pagination(current_page=5, total_pages=10, boundaries=-1)
        test_result = "Parameters could not be less then 0"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_around_less_than_null(self):
        pagination(current_page=5, total_pages=10, around=-1)
        test_result = "Parameters could not be less then 0"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_no_boundary_no_around_should_work(self):
        pagination(current_page=5, total_pages=10)
        test_result = "... 5 ..."
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_small_values_1(self):
        test_result = "1 2 3"
        pagination(current_page=2, total_pages=3, around=1)
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_small_values_2(self):
        test_result = "1 2 3"
        pagination(current_page=2, total_pages=3, boundaries=1)
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_small_values_3(self):
        test_result = "1 2 3"
        pagination(current_page=1, total_pages=3, boundaries=1, around=1)
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_no_current_page_gives_error(self):
        with self.assertRaises(TypeError):
            pagination(total_pages=10, boundaries=2, around=1)

    def test_no_total_pages_gives_error(self):
        with self.assertRaises(TypeError):
            pagination(current_page=10, boundaries=2, around=1)

    def tearDown(self):
        sys.stdout = self.held


if __name__ == "__main__":
    unittest.main()