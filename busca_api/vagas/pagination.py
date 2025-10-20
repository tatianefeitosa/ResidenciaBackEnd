from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50  # valor padrão
    page_size_query_param = 'page_size'  # permite ao usuário definir a quantidade
    max_page_size = 100  # limita o máximo para evitar sobrecarga

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,               # total geral
            'returned': len(data),                            # quantos itens vieram nesta página
            'page': self.page.number,                         # número da página atual
            'total_pages': self.page.paginator.num_pages,      # total de páginas
            'next': self.get_next_link(),                      # link para a próxima página (ou null)
            'previous': self.get_previous_link(),              # link para a anterior (ou null)
            'results': data                                   # os objetos em si
        })