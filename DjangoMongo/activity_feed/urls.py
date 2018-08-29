from django.urls import path, include, re_path
from activity_feed.views import FeedView, UserFeedView

urlpatterns = [
    path('v1/<str:user_id>/', include([
        path('feeds/', FeedView.as_view()),
        path('user-feeds/', UserFeedView.as_view()),
    ])),
]
