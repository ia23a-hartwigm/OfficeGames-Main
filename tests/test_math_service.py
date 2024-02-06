import unittest

import services.math_service as math_service

class TestMathService(unittest.TestCase):

    def test_add(self):
        # ASSIGN
        # nothing to do

        # ACT
        result = math_service.add(1.0, 2.0)

        # ASSERT
        self.assertEqual(result, 3.0)
