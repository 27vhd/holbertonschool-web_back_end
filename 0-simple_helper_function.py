#!/usr/bin/env python3
"""
Simple helper function for pagination.
"""


def index_range(page, page_size):
    """
    Returns start and end index for pagination.

    Args:
        page (int): page number (1-indexed)
        page_size (int): number of items per page

    Returns:
        tuple: (start_index, end_index)
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
