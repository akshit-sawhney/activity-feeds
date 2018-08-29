from rest_framework.exceptions import APIException
from rest_framework import status



class BadRequestException(APIException):
    status_code = 400



class NotFoundException(APIException):
    status_code = 404


class AddCandidateException(APIException):
    status_code = 400