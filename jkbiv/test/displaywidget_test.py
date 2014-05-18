from jkbiv.displaywidget import *
import unittest

class RectangleTest(unittest.TestCase):

    def testScaling(self):
        # scale with respect to (0, 0)
        r0 = Rectangle(5, 6, 10, 20)
        r1 = r0.computeScaledRect(2.0, 0, 0)
        self.assertEqual(r1, Rectangle(10, 12, 20, 40))
        # scale with respect to center
        r0 = Rectangle(5, 10, 20, 30)
        r1 = r0.computeScaledRect(2.0, 15, 25)
        self.assertEqual(r1, Rectangle(-5, -5, 40, 60))
        # scale with respect to arbitrary point inside the rect
        r0 = Rectangle(0, 0, 3, 4)
        r1 = r0.computeScaledRect(2.0, 2, 1)
        self.assertEqual(r1, Rectangle(-2, -1, 6, 8))
