import unittest
from src.validpanda.helpers import Helper


class TestHelpers(unittest.TestCase):
    """
    Tests Helper class
    """

    def test_chunks(self):
        test_list = []
        for i in Helper.chunks((1, 2, 3, 4), 2):
            test_list.append(i)
        self.assertEqual(test_list, [(1, 2), (3, 4)]), "chunks function is wrong"

    def test_find_pattern1(self):
        """
        test find_pattern functionality

        :return:
        """
        self.assertEqual(Helper.find_pattern((1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 5), (1, 2)), 8)

    def test_find_pattern2(self):
        """
        test find_pattern raises error

        :return:
        """
        self.assertRaises(ValueError,
                          Helper.find_pattern,
                          (1, 2, 1, 2),
                          (1, 2, 3, 4, 5))


if __name__ == '__main__':
    unittest.main()
