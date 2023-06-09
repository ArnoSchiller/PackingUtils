import unittest
from packutils.data.item import Item
from packutils.data.position import Position


class ItemTestCase(unittest.TestCase):
    def test_item_creation(self):
        item = Item(id="test", width=10, length=20, height=30)
        self.assertEqual(item.id, "test")
        self.assertEqual(item.width, 10)
        self.assertEqual(item.length, 20)
        self.assertEqual(item.height, 30)
        self.assertIsNone(item.position)

    def test_item_pack(self):
        item = Item(id="test", width=10, length=20, height=30)
        position = Position(x=5, y=5, z=5, rotation=0)
        item.pack(position)
        self.assertEqual(item.is_packed(), True)
        self.assertEqual(item.position, position)

    def test_to_position_and_dimension_2d(self):
        item = Item(
            id="test", width=40, length=50, height=60, position=Position(x=10, y=20, z=30)
        )

        # Test for valid dimensions
        pos, dim = item.to_position_and_dimension_2d(["width", "height"])
        self.assertEqual(pos, (10, 30))
        self.assertEqual(dim, (40, 60))

        pos, dim = item.to_position_and_dimension_2d(["length", "height"])
        self.assertEqual(pos, (20, 30))
        self.assertEqual(dim, (50, 60))

        pos, dim = item.to_position_and_dimension_2d(["width", "length"])
        self.assertEqual(pos, (10, 20))
        self.assertEqual(dim, (40, 50))

        # Test for invalid dimensions
        with self.assertRaises(ValueError):
            item.to_position_and_dimension_2d(
                ["width", "length", "height"])  # More than 2 dimensions

        with self.assertRaises(ValueError):
            item.to_position_and_dimension_2d(
                ["width", "depth"])  # Invalid dimension


if __name__ == '__main__':
    unittest.main()
