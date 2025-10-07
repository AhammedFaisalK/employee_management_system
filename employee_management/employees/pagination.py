from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Calculate start and end indices based on current page and page size
        start_index = (self.page.number - 1) * self.page.paginator.per_page + 1
        end_index = start_index + len(data) - 1

        # Adjust end_index to reflect the actual end of the current page's data
        if end_index > self.page.paginator.count:
            end_index = self.page.paginator.count

        response = {
            "count": self.page.paginator.count,
            "next": self.page.has_next(),
            "previous": self.page.has_previous(),
            "results": data,
            "page_number": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "start_index": start_index,
            "end_index": end_index,
        }

        return response