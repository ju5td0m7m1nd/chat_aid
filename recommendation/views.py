from rest_framework.views import APIView
from rest_framework.response import Response
import sys
from chat_ass import ChatAid
CA = ChatAid()

class Recommend(APIView):
    def get(self, request, user_input):
        result = CA.query_sent(user_input)
        return Response({'result': result})
    def post(self):
        pass
