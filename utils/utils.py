"""
Utility functions for URL Shortener app.
"""

import string

# Short URL will only consists of these ASCII characters: [0-9a-zA-Z]
# Initialise characters hash map for quick access to corresponding
#   digit's character
char_set = string.digits + string.ascii_letters
char_map = {digit: char for digit, char in enumerate(char_set)}


def encode_base62(id: int) -> str:
    """
    Takes an unique integer row id provided by the database and convert it to an
    unique base-62 encoded string to generate the short url.

    Args:
        id: Unique integer row id provided by the database

    Returns:
        str: Short URL
    """
    # Initialise a list to store the digits created from changing from base-10
    #   to base-62
    base62_encoded_result = []

    # For an integer N, it can be represented as
    # N = d_k * b^k + d_(k-1) * b^(k-1) + ... + d_1 * b^1 + d_0 * b^0
    # where b is the base.
    #
    # Dividing by b yields
    # N = b ( d_k * b^(k-1) + d_(k-1) * b^(k-2) + ... + d_1 ) + d_0
    # which is equivalent to
    # N = b * q + r
    # where q and r is the quotient and remainder respectively.
    #
    # By extracting the remainder r at every division by base b, we get the
    #   digit starting from the Least Significant Position.
    while id > 0:
        quotient = id // 62
        remainder = id % 62

        id = quotient

        # Store the generated base62 char
        base62_encoded_result.append(char_map[remainder])

    # Because we append to the list, the character in the Least Significant Position
    #   will be at the start of the list. We reverse because we read numbers from
    #   left to right, and it is easier to understand numbers going from Most
    #   Significant Position to Least Significant Position (i.e. Character in Least
    #   Significant Position is at the end).
    base62_encoded_result.reverse()

    # Return result as a single base-62 encoded string
    return "".join(base62_encoded_result)
