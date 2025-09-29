import argparse
import sys
from prism import ShamirSecret


def split_secret_cli(args):
    """
    Splits a secret into n shares with a threshold of k using Shamir's Secret Sharing.

    Args:
        args: Parsed command-line arguments containing k, n, and secret.

    Prints:
        The generated shares or an error message.
    """
    shares, msg = ShamirSecret.split(args.k, args.n, args.secret)
    if not shares:
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)
    print("Shares:")
    for s in shares:
        print(s)


def combine_secret_cli(args):
    """
    Combines shares to reconstruct the original secret using Shamir's Secret Sharing.

    Args:
        args: Parsed command-line arguments containing shares or a shares file.

    Prints:
        The reconstructed secret or an error message.
    """
    shares = []
    if args.shares_file:
        with open(args.shares_file, "r") as f:
            shares = [line.strip() for line in f if line.strip()]
    else:
        shares = args.shares
    secret, msg = ShamirSecret.combine(shares)
    if not secret:
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)
    print("Reconstructed secret:")
    print(secret)


def main():
    """
    Main entry point for the Prism CLI.

    Provides two commands:
    - split: Split a secret into shares.
    - combine: Reconstruct a secret from shares.

    Usage examples:
        python cli.py split -k 3 -n 5 "my_secret"
        python cli.py combine -s 1-... 2-... 3-...
        python cli.py combine -f shares.txt
    """
    parser = argparse.ArgumentParser(description="Prism CLI - Shamir's Secret Sharing")
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Split a secret into shares")
    split_parser.add_argument("-k", type=int, required=True, help="Minimum shares needed to reconstruct")
    split_parser.add_argument("-n", type=int, required=True, help="Total number of shares")
    split_parser.add_argument("secret", type=str, help="Secret to split")
    split_parser.set_defaults(func=split_secret_cli)

    combine_parser = subparsers.add_parser("combine", help="Reconstruct a secret from shares")
    combine_group = combine_parser.add_mutually_exclusive_group(required=True)
    combine_group.add_argument("-f", "--shares-file", type=str, help="File containing shares (one per line)")
    combine_group.add_argument("-s", "--shares", nargs="+", help="Shares provided directly on the command line")
    combine_parser.set_defaults(func=combine_secret_cli)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
