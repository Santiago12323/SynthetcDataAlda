import random
import uuid
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from faker import Faker

fake = Faker()


CATEGORIES = {
    "Electronics": (200, 3000),
    "Clothing": (20, 200),
    "Home": (50, 1000),
    "Sports": (30, 800),
    "Beauty": (10, 300),
}

CATEGORY_WEIGHTS = [0.25, 0.30, 0.20, 0.15, 0.10]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
PAYMENT_WEIGHTS = [0.45, 0.30, 0.15, 0.10]

DELIVERY_TYPES = {
    "Standard": 5,
    "Express": 15,
    "Next-Day": 25
}

LOYALTY_LEVELS = ["Bronze", "Silver", "Gold", "Platinum"]
LOYALTY_WEIGHTS = [0.5, 0.25, 0.15, 0.10]



def generate_customer():
    return {
        "customer_id": str(uuid.uuid4()),
        "age": random.randint(18, 70),
        "gender": random.choice(["Male", "Female"]),
        "country": fake.country(),
        "registration_date": fake.date_between(start_date='-5y', end_date='today'),
        "loyalty_level": random.choices(
            LOYALTY_LEVELS, weights=LOYALTY_WEIGHTS
        )[0]
    }


def generate_product():
    category = random.choices(
        list(CATEGORIES.keys()),
        weights=CATEGORY_WEIGHTS
    )[0]

    price_range = CATEGORIES[category]

    return {
        "product_id": str(uuid.uuid4()),
        "category": category,
        "brand": fake.company(),
        "price": round(random.uniform(*price_range), 2),
        "rating": round(random.uniform(3.0, 5.0), 1)
    }


def generate_order(customer, product):
    quantity = random.randint(1, 5)

    delivery_type = random.choice(list(DELIVERY_TYPES.keys()))
    shipping_cost = DELIVERY_TYPES[delivery_type]

    discount = 0
    if customer["loyalty_level"] in ["Gold", "Platinum"]:
        discount = random.uniform(5, 15)

    subtotal = product["price"] * quantity
    total = subtotal - (subtotal * discount / 100) + shipping_cost

    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "quantity": quantity,
        "order_date": fake.date_between(start_date='-2y', end_date='today'),
        "payment_method": random.choices(
            PAYMENT_METHODS,
            weights=PAYMENT_WEIGHTS
        )[0],
        "delivery_type": delivery_type,
        "shipping_cost": shipping_cost,
        "discount_percent": round(discount, 2),
        "total_price": round(total, 2),
        "order_status": random.choices(
            ["Delivered", "Shipped", "Cancelled"],
            weights=[0.80, 0.15, 0.05]
        )[0]
    }



def generate_dataset(n=1000, output_path="ecommerce_data.csv"):
    records = []

    for _ in range(n):
        customer = generate_customer()
        product = generate_product()
        order = generate_order(customer, product)

        record = {**customer, **product, **order}
        records.append(record)

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)

    return df



def run_benchmark(max_size=10000, step=1000):
    sizes = list(range(step, max_size + 1, step))
    times = []

    for size in sizes:
        start = time.time()
        generate_dataset(n=size, output_path="temp.csv")
        end = time.time()
        times.append(end - start)

    Path("analysis_results").mkdir(exist_ok=True)

    plt.figure()
    plt.plot(sizes, times)
    plt.xlabel("Dataset Size")
    plt.ylabel("Generation Time (seconds)")
    plt.title("E-commerce Data Generation Benchmark")
    plt.savefig("analysis_results/benchmark.png")
    plt.close()

    print("Benchmark saved to analysis_results/benchmark.png")
