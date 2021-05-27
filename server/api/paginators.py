from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 1

    def get_paginated_response(self, quiz_id, data):
        return Response(OrderedDict([
            ('id', quiz_id),
            ('offset', self.offset),
            ('count', self.count),
            ('next', f"'{self.get_next_link()}'"),
            ('previous', self.get_previous_link()),
            ('results', data)

        ]))
