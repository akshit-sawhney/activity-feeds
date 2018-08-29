from rest_framework import serializers


class ActivityFeedSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    meta_data = serializers.SerializerMethodField()

    def get_type(self, obj):
        if obj and 'type' in obj and obj['type']:
            return (obj['type'])

    def get_created_at(self, obj):
        if obj and 'created_at' in obj and obj['created_at']:
            return (obj['created_at'])

    def get_meta_data(self, obj):
        return (obj['meta_data'])

class UserActivityFeedSerializer(serializers.Serializer):
    relevance = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    activity_feed = serializers.SerializerMethodField()

    def get_relevance(self, obj):
        if obj and 'relevance' in obj and obj['relevance']:
            return (obj['relevance'])

    def get_created_at(self, obj):
        if obj and 'created_at' in obj and obj['created_at']:
            return (obj['created_at'])

    def get_activity_feed(self, obj):
        return (obj['activity_feed'])


class ActivityFeedListSerializer(serializers.Serializer):
    results = ActivityFeedSerializer(many=True)

class UserActivityFeedListSerializer(serializers.Serializer):
    results = UserActivityFeedSerializer(many=True)


