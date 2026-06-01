#!/usr/bin/env python3
"""
Hypermedia pagination module.
"""

import math
from typing import List, Dict

SimpleServer = __import__('1-simple_pagination').Server


class Server(SimpleServer):
    """Server class with hypermedia pagination support."""

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Returns a dictionary with hypermedia pagination metadata and data.

        Args:
            page (int): page number (1-indexed)
            page_size (int): number of items per page

        Returns:
            Dict: pagination metadata including data, page info, and neighbors
        """
        data = self.get_page(page, page_size)
        dataset_len = len(self.dataset())

        total_pages = math.ceil(dataset_len / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": page_size if data else 0,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
