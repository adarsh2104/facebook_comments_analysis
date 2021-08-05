from request_client.models import SearchKeyword
from request_client.serializer import PostCommentsSerializer
from typing import Dict
import logging
log = logging.getLogger(__name__)


class SerializerFunctions:
    def save_extracted_comments(self, comments: list, search_keyword:str) -> Dict:
        '''
        Serialize the collected post comments PostComment models
        '''
        print('save_extracted_comments', comments)
        keyword_instance, _ = SearchKeyword.objects.get_or_create(
            keyword=search_keyword)
        data_set = {'fk_keyword': keyword_instance.keyword_id}

        comments_data = [{
            'comment': comment,
            **data_set
        } for comment in comments]
        instance = PostCommentsSerializer(data=comments_data, many=True)

        if instance.is_valid():
            instance.save()
            print('is_valid', comments_data)
            return {'data': instance.data, 'saved': True}
        else:
            return {'error': instance.errors, 'saved': False}
