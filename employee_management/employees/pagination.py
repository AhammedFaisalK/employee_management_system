from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        start_index = (self.page.number - 1) * self.page.paginator.per_page + 1
        end_index = start_index + len(data) - 1
        if end_index > self.page.paginator.count:
            end_index = self.page.paginator.count

        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
                "page_number": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "start_index": start_index,
                "end_index": end_index,
            }
        )
