from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from activity_feed.services import ActivityFeedImpl, UserActivityFeedImpl
from activity_feed.serializers import ActivityFeedListSerializer, UserActivityFeedListSerializer


class BaseClass(object):
    permission_classes = ()
    authentication_classes = ()

class FeedView(BaseClass, APIView):
    def post(self, request, user_id):
        ActivityFeedImpl().save_new_feed(request, user_id)
        return Response({
            "status": 200,
            "type": "POST",
        })

    def get(self, request, user_id):
        output = ActivityFeedImpl().get_home_feed(request, user_id)
        return Response(
            ActivityFeedListSerializer({
                'results': output,
            }).data
        )

class UserFeedView(BaseClass, APIView):
    def get(self, request, user_id):
        output = UserActivityFeedImpl().get_user_feed(request, user_id)
        return Response(
            UserActivityFeedListSerializer({
                "results": output,
            }).data
        )
