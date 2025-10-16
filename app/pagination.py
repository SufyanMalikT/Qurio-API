from rest_framework.pagination import PageNumberPagination

class StandardResultPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'size'
    max_page_size = 20