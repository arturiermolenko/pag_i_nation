import io
import sys
import unittest
from main import pagination


class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, io.StringIO()

    def test_current_page_not_integer(self):
        pagination(current_page=2.8, total_pages=10)
        test_result = "current_page is not an integer\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_total_pages_not_integer(self):
        pagination(current_page=2, total_pages="str")
        test_result = "total_pages is not an integer\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_boundaries_not_integer(self):
        pagination(current_page=2, total_pages=10, boundaries=2.4)
        test_result = "boundaries is not an integer\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_around_not_integer(self):
        pagination(current_page=2, total_pages=10, around=1.1)
        test_result = "around is not an integer\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_huge_boundaries(self):
        pagination(current_page=2, total_pages=10, boundaries=999999)
        test_result = "1 2 3 4 5 6 7 8 9 10\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_huge_amount(self):
        pagination(current_page=2, total_pages=10, around=999999)
        test_result = "1 2 3 4 5 6 7 8 9 10\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_current_page_equals_null(self):
        pagination(current_page=0, total_pages=10)
        test_result = "Current page should be greater than 1\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_total_pages_equals_null(self):
        pagination(current_page=5, total_pages=0)
        test_result = "Current page cannot be greater than total_pages\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_current_page_greater_than_total_pages(self):
        pagination(current_page=5, total_pages=4)
        test_result = "Current page cannot be greater than total_pages\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_boundaries_less_than_null(self):
        pagination(current_page=5, total_pages=10, boundaries=-1)
        test_result = "Boundaries could not be less then 0\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_around_less_than_null(self):
        pagination(current_page=5, total_pages=10, around=-1)
        test_result = "Around could not be less then 0\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_simple_pagination_1(self):
        pagination(current_page=5, total_pages=10, boundaries=2, around=1)
        test_result = "1 2 ... 4 5 6 ... 9 10\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_simple_pagination_2(self):
        pagination(current_page=4, total_pages=10, boundaries=2, around=1)
        test_result = "1 2 3 4 5 ... 9 10\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_simple_pagination_3(self):
        pagination(current_page=9, total_pages=10, boundaries=2, around=1)
        test_result = "1 2 ... 8 9 10\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_huge_total(self):
        pagination(current_page=2, total_pages=999999, boundaries=2, around=1)
        test_result = "1 2 3 ... 999998 999999\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_huge_total_2(self):
        pagination(current_page=999998, total_pages=999999, boundaries=3, around=1)
        test_result = "1 2 3 ... 999997 999998 999999\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_large_inputs(self):
        pagination(current_page=500000, total_pages=1000000, boundaries=2, around=2)
        test_result = "1 2 ... 499998 499999 500000 500001 500002 ... 999999 1000000"
        self.assertEqual(sys.stdout.getvalue().strip(), test_result)

    def test_no_boundary_no_around_should_work(self):
        pagination(current_page=5, total_pages=10)
        test_result = "... 5 ...\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_no_boundary_should_work(self):
        pagination(current_page=5, total_pages=10, around=1)
        test_result = "... 4 5 6 ...\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_no_boundary_should_work_2(self):
        pagination(current_page=5, total_pages=10, around=3)
        test_result = "... 2 3 4 5 6 7 8 ...\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_minimum_thresholds(self):
        pagination(current_page=1, total_pages=1, boundaries=0, around=0)
        test_result = "1\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_small_values_1(self):
        test_result = "1 2 3\n"
        pagination(current_page=2, total_pages=3, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_small_values_2(self):
        test_result = "1 2 3\n"
        pagination(current_page=2, total_pages=3, boundaries=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_small_values_3(self):
        test_result = "1 2 3\n"
        pagination(current_page=1, total_pages=3, boundaries=1, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_no_current_page_gives_error(self):
        with self.assertRaises(TypeError):
            pagination(total_pages=10, boundaries=2, around=1)

    def test_no_total_pages_gives_error(self):
        with self.assertRaises(TypeError):
            pagination(current_page=10, boundaries=2, around=1)

    def test_1_10_3_1(self):
        test_result = "1 2 3 ... 8 9 10\n"
        pagination(current_page=1, total_pages=10, boundaries=3, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_9_10_4_1(self):
        test_result = "1 2 3 4 ... 7 8 9 10\n"
        pagination(current_page=9, total_pages=10, boundaries=4, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_4_5_1_0(self):
        test_result = "1 ... 4 5\n"
        pagination(current_page=4, total_pages=5, boundaries=1, around=0)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_4_10_2_2(self):
        test_result = "1 2 3 4 5 6 ... 9 10\n"
        pagination(current_page=4, total_pages=10, boundaries=2, around=2)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_5_10_3_2(self):
        pagination(current_page=5, total_pages=10, boundaries=3, around=2)
        test_result = "1 2 3 4 5 6 7 8 9 10\n"
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_5_10_1_0(self):
        test_result = "1 ... 5 ... 10\n"
        pagination(current_page=5, total_pages=10, boundaries=1, around=0)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_1_10(self):
        test_result = "1 ...\n"
        pagination(current_page=1, total_pages=10)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_1_10_0_1(self):
        test_result = "1 2 ...\n"
        pagination(current_page=1, total_pages=10, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_1_10_1_1(self):
        test_result = "1 2 ... 10\n"
        pagination(current_page=1, total_pages=10, boundaries=1, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_10_10(self):
        test_result = "... 10\n"
        pagination(current_page=10, total_pages=10)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_10_10_0_1(self):
        test_result = "... 9 10\n"
        pagination(current_page=10, total_pages=10, around=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_10_10_1_0(self):
        test_result = "1 ... 10\n"
        pagination(current_page=10, total_pages=10, boundaries=1)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_4_9_0_4(self):
        test_result = "1 2 3 4 5 6 7 8 ...\n"
        pagination(current_page=4, total_pages=9, around=4)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def test_2_10_0_4(self):
        test_result = "1 2 3 4 5 6 ...\n"
        pagination(current_page=2, total_pages=10, around=4)
        self.assertEqual(sys.stdout.getvalue(), test_result)

    def tearDown(self):
        sys.stdout = self.held
