import argparse
from data_generator.ecommerce_generator import generate_dataset, run_benchmark

def main():
    parser = argparse.ArgumentParser(
        description="Synthetic E-commerce Data Generator"
    )

    parser.add_argument("-n", type=int, default=1000,
                        help="Number of records to generate")

    parser.add_argument("-o", type=str, default="ecommerce_data.csv",
                        help="Output file path")

    parser.add_argument("-b", action="store_true",
                        help="Run benchmark")

    parser.add_argument("-s", type=int, default=1000,
                        help="Benchmark step size")

    args = parser.parse_args()

    if args.b:
        run_benchmark(max_size=args.n, step=args.s)
    else:
        generate_dataset(n=args.n, output_path=args.o)
        print(f"Dataset generated: {args.o}")


if __name__ == "__main__":
    main()
