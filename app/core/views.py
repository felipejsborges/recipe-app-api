from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(*args, **kwargs):  # pylint: disable=unused-argument
    # TODO: check if database is available
    return Response({"healthy": True})
