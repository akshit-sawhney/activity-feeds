from abc import ABC, abstractmethod
from datetime import datetime
from activity_feed.exceptions import BadRequestException
from activity_feed.models import Activity_feed, User_activity_feed

class UserService(ABC):
    @abstractmethod
    def save_new_user(self, request):
        pass

    @abstractmethod
    def get_users(self, request):
        pass

class ActivityFeedService(ABC):
    @abstractmethod
    def save_new_feed(self, request):
        pass
    def get_home_feed(self, request):
        pass

class UserActivityFeedService(ABC):
    @abstractmethod
    def get_user_feed(self, request):
        pass

class ActivityFeedImpl(ActivityFeedService):
    def save_new_feed(self, request, user_id):
        _user_id_param = int(user_id) or 0
        _type_param = request.data.get('type')
        if (_user_id_param and _type_param):
            new_feed = Activity_feed(user_id=_user_id_param, type=_type_param)
            new_feed.meta_data = request.data.get('meta')
            output = new_feed.save()
            friends_list = [1,2,3,4]
            for friend_id in friends_list:
                new_user_field = User_activity_feed(user_id=friend_id, reference_id=output.id, relevance=1)
                new_user_field.save()
            return True
        else:
            message = {
                "success": False,
                "message": 'paramMissing',
            }
            raise BadRequestException(message)

    def get_home_feed(self, request, user_id):
        _user_id_param = int(user_id) or 0
        _type_param = str(request.query_params.get('type', ''))
        _last_param = int(request.query_params.get('last_time', 0))
        if _last_param:
            try:
                _last_param = convertMillisecondsToDateTime(_last_param)
            except:
               _last_param = 0
        if _user_id_param:
            records = []
            if _type_param:
                if (_last_param):
                    _queryObject = Activity_feed.objects(user_id=_user_id_param, type=_type_param, created_at__lt=_last_param).order_by('-created_at')[:2]
                else:
                    _queryObject = Activity_feed.objects(user_id=_user_id_param, type=_type_param).order_by('-created_at')[:2]
            elif _last_param:
                _queryObject = Activity_feed.objects(user_id=_user_id_param, created_at__lt=_last_param).order_by('-created_at')[:2]
            else:
                _queryObject = Activity_feed.objects(user_id=_user_id_param).order_by('-created_at')[:2]
            for record in _queryObject:
                records.append({
                    "meta_data": record.meta_data,
                    "type": record.type,
                    "created_at": convertDateTimeToMillisconds(record.created_at),
                })
            return records
        else:
            message = {
                "success": False,
                "message": 'paramMissing',
            }
            raise BadRequestException(message)

class UserActivityFeedImpl(UserActivityFeedService):
    def get_user_feed(self, request, user_id):
        _user_id_param = int(user_id) or 0
        _last_param = int(request.query_params.get('last_time', 0))
        if _last_param:
            try:
                _last_param = convertMillisecondsToDateTime(_last_param)
            except:
                _last_param = 0
        if _user_id_param:
            records = []
            if (_last_param):
                _user_activity_feed_query = User_activity_feed.objects(user_id=_user_id_param , created_at__lt=_last_param).order_by('-created_at')[:2]
            else:
                _user_activity_feed_query = User_activity_feed.objects(user_id=_user_id_param).order_by('-created_at')[:2]
            for record in _user_activity_feed_query:
                records.append({
                    "relevance": record.relevance,
                    "created_at": convertDateTimeToMillisconds(record.created_at),
                    "activity_feed": {
                        "type": record.reference_id.type,
                        "user_id": record.reference_id.user_id,
                        "meta_data": record.reference_id.meta_data,
                        "created_at": convertDateTimeToMillisconds(record.reference_id.created_at),
                    }
                })
            return records
        else:
            message = {
                "success": False,
                "message": 'paramMissing',
            }
            raise BadRequestException(message)

epoch = datetime.utcfromtimestamp(0)
def convertDateTimeToMillisconds(dt):
    return (dt - epoch).total_seconds() * 1000.0

def convertMillisecondsToDateTime(ms):
    return datetime.fromtimestamp(ms / 1000.0)

