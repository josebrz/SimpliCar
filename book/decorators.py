from rest_framework.response import Response
from rest_framework.views import status


def validate_library_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        if not name:
            return Response(
                data={
                    "message": "The name is required to add a library"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated


def validate_book_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        title = args[0].request.data.get("title", "")
        if not title:
            return Response(
                data={
                    "message": "The title is required to add/update a Book"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated
