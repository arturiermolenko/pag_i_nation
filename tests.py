import io
import sys
import unittest
from main import pagination


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, io.StringIO()

    def test_current_page_not_integer(self):
        pagination(current_page=2.8, total_pages=10)
        test_result = "Current page should be integer"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_total_pages_not_integer(self):
        pagination(current_page=2, total_pages=10.6)
        test_result = "Total pages should be integer"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_boundaries_not_integer(self):
        pagination(current_page=2, total_pages=10, boundaries=2.4)
        test_result = "Boundaries should be integer"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_around_not_integer(self):
        pagination(current_page=2, total_pages=10, around=1.1)
        test_result = "Around should be integer"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_huge_boundaries(self):
        pagination(current_page=2, total_pages=10, boundaries=999999)
        test_result = "Boundaries should not be greater than total_pages."
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_huge_amount(self):
        pagination(current_page=2, total_pages=10, around=999999)
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
        test_result = "Boundaries could not be less then 0"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_around_less_than_null(self):
        pagination(current_page=5, total_pages=10, around=-1)
        test_result = "Around could not be less then 0"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

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
