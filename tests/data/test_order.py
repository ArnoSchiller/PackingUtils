from packutils.data.order import Article, Order
import unittest


class TestImports(unittest.TestCase):

    def test_load_from_json_file(self):
        order = Order.from_json_file("tests/test_order.json")

        self.assertEqual(order.order_id, "xyz", "Failed to load order_id")
        self.assertEqual(len(order.articles), 1, "Failed to load articles")
        self.assertEqual(len(order.supplies), 1, "Failed to load supplies")

    def test_convert_to_item(self):
        article = Article(
            article_id="test_article", length=20,
            width=20, height=20, weight=0.0, amount=20)
        order = Order(order_id="test", articles=[article])
        items = order.to_item_list()

        self.assertEqual(len(items), 1, "Failed to convert")
        self.assertEqual(items[0].width, article.width,
                         "Failed to convert order to items list (wrong width)")
        self.assertEqual(items[0].length, article.length,
                         "Failed to convert order to items list (wrong length)")
        self.assertEqual(items[0].height, article.height,
                         "Failed to convert order to items list (wrong height)")
        self.assertEqual(items[0].weight, article.weight,
                         "Failed to convert order to items list (wrong weight)")
        self.assertEqual(items[0].position, None,
                         "Failed to convert order to items list (wrong position)")


if __name__ == '__main__':
    unittest.main()
