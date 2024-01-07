from rest_framework.response import Response

from .models import Freelancer, Validator
from .serializers import FreelancerSerializer
from django.db.models import Q

from rest_framework.views import APIView


sort_by_lst = [
    "id",
    "name",
    "email",
    "phone_number",
    "availability",
    "salary",
    "position"
]

sort_type_lst = [
    "asc",
    "desc",
]


class FreelancerAPIGet(APIView):
    def get(self, request, **kwargs):
        query_set = Freelancer.objects.all()
        query_set_size = len(query_set)
        errors = {}
        set_limit = request.GET.get('limit', None)
        # validate limit
        if not set_limit:
            self.limit = 5
        elif Validator.validate_natural_number(set_limit):
            self.limit = int(set_limit)
        else:
            errors['limit'] = f'should be natural number'

        set_offset = request.GET.get('offset', None)
        # validate offset
        if not set_offset:
            self.offset = 0
        elif Validator.validate_natural_number(set_offset) and not len(errors):
            self.offset = int(set_offset)
            self.offset *= self.limit
        else:
            errors['offset'] = f'should be natural number'

        set_sort_type = request.GET.get('sort_type', None)
        # validate field
        if not set_sort_type:
            self.sort_type = 'asc'
        elif set_sort_type in sort_type_lst:
            self.sort_type = set_sort_type
        else:
            errors['sort_type'] = 'should be asc | desc'

        set_sort_by = request.GET.get('sort_by', None)
        # validate sort_by
        if not set_sort_by:
            self.sort_by = 'id'
        elif set_sort_by in sort_by_lst:
            self.sort_by = set_sort_by
        else:
            errors['sort_by'] = 'should be fieldname'

        set_search = request.GET.get('s', None)
        if set_search:
            self.search = set_search

        query_set = Freelancer.objects.all()
        query_set2 = Freelancer.objects.all()
        search_query_set = None
        # searched
        if set_search and not len(errors):
            search_query = Q()
            for field in Freelancer._meta.get_fields():
                search_query |= Q(**{f'{field.name}__contains': set_search})

            search_query_set = query_set2.filter(search_query)

        # sorted
        if self.sort_by and not len(errors):
            if set_sort_type == 'asc':
                query_set = query_set.order_by(f'{self.sort_by}')
            elif set_sort_type == 'desc':
                query_set = query_set.order_by(f'-{self.sort_by}')

        # paginated
        if (set_limit or set_offset) and not len(errors):
            query_set = query_set[self.offset: self.offset + self.limit]

        if len(errors):
            return Response({
                'status': '400',
                'errors': errors
            }, '400',)

        if search_query_set:
            return Response({
                'results': {'results of search': FreelancerSerializer(search_query_set, many=True).data,
                            'results of slice': FreelancerSerializer(query_set, many=True).data}
            }, '200')
        return Response({
            'results': [FreelancerSerializer(query_set, many=True).data]
        }, '200')

    def post(self, request):
        serializer = FreelancerSerializer(data=request.data)
        # check whether all fields that don't have default
        if not serializer.is_valid():
            return Response({"Result": {"status": "400",
                                        "errors": serializer.errors}}, "400")
        serializer.save()

        return Response({"Result": {"status": "200",
                                    "message": f"freelancer has been successfully created"}}, "200")


# get by id correct
class FreelancerAPIViewGet(APIView):
    # responsible for get calls with index

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method GET not allowed"})

        try:
            instance = Freelancer.objects.get(id=pk)
        except:
            return Response({"status": "404", "error": "Freelancer is not found"}, "404")

        return Response({'freelancer': FreelancerSerializer(instance).data}, '200')

    # responsible for put calls with index
    def put(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Freelancer.objects.get(id=pk)
        except:
            return Response({"status": "404", "error": "Freelancer is not found"}
                            , '404')

        serializer = FreelancerSerializer(data=request.data, instance=instance)
        if not serializer.is_valid():
            return Response({"Result": {"status": "400",
                                        "message": serializer.errors}}, "400")
        # if without return Response data, then method save
        # in this case method update
        serializer.save()
        # may work incorrectly request.data
        return Response({"Result": {"status": "200", "message": f"freelancer has been successfully updated",
                                    "freelancer": request.data}}, '200')

    # responsible for delete calls with index
    def delete(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        # here code to delete
        try:
            object_to_delete = Freelancer.objects.get(id=pk)
        except:
            return Response({"status": "404", "error": "Freelancer is not found"},
                            '404')

        object_to_delete.delete()

        # return Response({"Result": {"status": "200",
        #                             "message": f"freelancer has been successfully deleted"}})
        return Response({"Result": {"status": "200",
                                    "message": f"freelancer has been successfully deleted"}}, '200')
