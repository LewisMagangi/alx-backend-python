from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages
    """
    page_size = 20  # Number of messages per page
    page_size_query_param = 'page_size'  # Allow client to override page size
    max_page_size = 100  # Maximum limit per client request
    page_query_param = 'page'  # Query parameter for page number