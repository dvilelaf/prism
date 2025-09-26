import binascii
from typing import List

from Crypto.Protocol.SecretSharing import Shamir

from prism.constants import EXPECTED_SECRET_LENGTH_BYTES


class ShamirSecret:
    """Class to handle Shamir's Secret Sharing operations"""

    @classmethod
    def split(cls, k: int, n: int, secret: str):
        """Split the secret into n shares with a threshold of k"""

        if k <= 1 or n < k:
            return None, "Invalid parameters: ensure that n >= k > 1."
        secret_bytes = secret.encode("utf-8")

        if len(secret_bytes) > EXPECTED_SECRET_LENGTH_BYTES:
            return (
                None,
                f"Secret too long: must be at most {EXPECTED_SECRET_LENGTH_BYTES} bytes",
            )

        if len(secret_bytes) < EXPECTED_SECRET_LENGTH_BYTES:
            secret_bytes = secret_bytes.ljust(
                EXPECTED_SECRET_LENGTH_BYTES, b"\x00"
            )  # Pad with null bytes

        if len(secret_bytes) != EXPECTED_SECRET_LENGTH_BYTES:
            return (
                None,
                f"Secret must be exactly {EXPECTED_SECRET_LENGTH_BYTES} bytes after padding",
            )

        shares = Shamir.split(k, n, secret_bytes)

        formatted_shares = []
        for index, share_data in shares:
            formatted_shares.append(
                f"{index}: {binascii.hexlify(share_data).decode("ascii")}"
            )
        return formatted_shares, "OK"

    @classmethod
    def combine(cls, shares: List[str]):
        """Combine shares to reconstruct the secret"""

        shares = [s.strip() for s in shares if s.strip()]

        prepared_shares = []
        for share in shares:
            parts = share.split(":")
            if len(parts) != 2:
                return None, "Incorrect share format. Must be 'index: secret_part'."
            idx = int(parts[0].strip())
            share_bytes = binascii.unhexlify(parts[1].strip())
            prepared_shares.append((idx, share_bytes))

        # Ensure there's no duplicate indices
        indices = [idx for idx, _ in prepared_shares]
        if len(indices) != len(set(indices)):
            return (
                None,
                "Duplicate share indices detected. Each share must have a unique index.",
            )

        secret_bytes = Shamir.combine(prepared_shares)
        try:
            secret = secret_bytes.rstrip(b"\x00").decode(
                "utf-8"
            )  # Remove padding and decode
        except UnicodeDecodeError:
            return (
                None,
                "You probably don't have enough valid parts to reconstruct this secret.",
            )
        return secret, "OK"
