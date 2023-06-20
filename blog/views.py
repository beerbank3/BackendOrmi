from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Index page GET')
#     # 나머지 요청
#     # 에러, 예외처리
#     return HttpResponse('No!!!')

class Index(View):
    def get(self, request):
        #return HttpResponse('Index page GET Class')
        return render(request, 'blog/board.html')