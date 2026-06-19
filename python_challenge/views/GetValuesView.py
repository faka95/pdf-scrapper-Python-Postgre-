from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from python_challenge.models import Index
from python_challenge.scrapper import index_scrapper
from python_challenge.serializers import IndexSerializer


def scrap_indexes():
    indexes = index_scrapper.get_indexes()
    for index in indexes:
        Index.objects.get_or_create(type=index["type"], value=index["value"], year=index["year"],
                                    month=index["month"])
    return


class GetValuesView(APIView):

    def get(self, request, *args, **kwargs):
        if not request.GET:
            last_index = Index.objects.order_by("-year", "-month").first()
            if last_index is None:
                scrap_indexes()
                last_index = Index.objects.order_by("-year", "-month").first()
            indexes = Index.objects.filter(year=last_index.year, month=last_index.month).order_by("-year", "-month")[:3]
            serializer = IndexSerializer(indexes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            start_date = request.GET.get("startDate").split("-")
            end_date = request.GET.get("endDate").split("-")
            start_year, start_month = start_date[0], start_date[1]
            end_year, end_month = end_date[0], end_date[1]

            indexes = Index.objects.filter(
                Q(year__gt=start_year) | Q(year=start_year, month__gte=start_month),
                Q(year__lt=end_year) | Q(year=end_year, month__lte=end_month)
            ).order_by("year", "month")
            if indexes.first() is None:
                scrap_indexes()
                indexes = Index.objects.filter(
                    Q(year__gt=start_year) | Q(year=start_year, month__gte=start_month),
                    Q(year__lt=end_year) | Q(year=end_year, month__lte=end_month)
                ).order_by("year", "month")
            serializer = IndexSerializer(indexes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
