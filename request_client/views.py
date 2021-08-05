from django.conf import settings
from django.http import HttpResponse
from django.http.response import JsonResponse
from nltk.featstruct import _is_mapping
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
import json
# from .models import SearchKeyword,PostComment
from selenium.common.exceptions import InvalidSessionIdException
# from request_client.facebook_request_client import RequestClient
from request_client.models import SearchKeyword,PostComments
from request_client.sentiment_analyzer import main as Sentiment_analyzer
from .serializer import SearchKeywordSerializer

class ClassView(APIView):
    def get(self,request):
        response_data = {'suggestions':[]}
        
        keyword_suggestions = SearchKeyword.objects.all()
        if keyword_suggestions:
            keyword_data = SearchKeywordSerializer(instance=keyword_suggestions,many=True)

            response_data['suggestions'] = keyword_data.data
            
        return HttpResponse(json.dumps(response_data),content_type='application/json',status=200)    
        


    def post(self,request,query=''):
        response_data = {}
        status = 200
        comment_lst = PostComments.objects.filter(fk_keyword__keyword=query).values_list('comment',flat=True)
        comments,review = Sentiment_analyzer(comment_lst)
        response_data = {
                        'comments':comments,
                        'review': review
                    }
        return HttpResponse(json.dumps(response_data),content_type='application/json',status=200)

        try:
            if query is not '':
                # comments_for_query = RequestClient().main(search_keyword=query)
                if comments_for_query.get('saved') is True:
                    comment_lst = PostComments.objects.filter(fk_keyword__keyword=query).values_list('comment',flat=True)
                    comments,review = Sentiment_analyzer(comment_lst)
                    response_data = {
                        'comments':comments,
                        'review': review
                    }
                    # return HttpResponse(json.dumps(response_data),content_type='application/json',status=200)
            else:
                status = 404
                response_data['error'] = 'Please enter a valid search keyword'
                # return HttpResponse(json.dumps(response_data),content_type='application/json',status=status)

        except :
            instance = {'error':'An error has occured'}
            status = 500
            # return HttpResponse(json.dumps(response_data),content_type='application/json',status=status)

        return HttpResponse(json.dumps(response_data),content_type='application/json',status=status)
            
        
        

        
