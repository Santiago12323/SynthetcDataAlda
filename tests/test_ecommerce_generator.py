import unittest
from data_generator.ecommerce_generator import generate_dataset


class TestEcommerceGenerator(unittest.TestCase):

    def test_dataset_size(self):
        df = generate_dataset(n=100)
        self.assertEqual(len(df), 100)

    def test_required_columns(self):
        df = generate_dataset(n=10)
        required_columns = [
            "customer_id",
            "product_id",
            "order_id",
            "total_price",
            "category",
            "loyalty_level"
        ]
        for col in required_columns:
            self.assertIn(col, df.columns)


if __name__ == "__main__":
    unittest.main()
