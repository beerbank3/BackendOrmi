from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse

# Create your views here.
# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Index page GET')
#     # 나머지 요청
#     # 에러, 예외처리
#     return HttpResponse('No!!!')

### Post
class Index(View):
    def get(self, request):
        # return HttpResponse('Index page GET class')
        
        # 데이터베이스에 접근해서 값을 가져와야 합니다.
        # 게시판에 글들을 보여줘야하기 때문에 데이터베이스에서 "값 조회"
        # MyModel.objects.all()
        post_objs = Post.objects.all()
        # context = 데이터베이스에서 가져온 값
        context = {
            "posts": post_objs
        }
        # print(post_objs)
        return render(request, 'blog/board.html', context)


# write
# post - form
# 글 작성 화면
def write(request):
    if request.method == 'POST':
        # form 확인
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('blog:list')

    form = PostForm()
    return render(request, 'blog/write.html', { 'form': form })


# Django 자체의 클래스 뷰 기능도 강력, 편리
# model, template_name, context_object_name,
# paginate_by
# Django.views.generic -> ListView
class List(ListView):
    model = Post # model
    template_name = 'blog/post_list.html' # 템플릿
    context_object_name = 'posts' # 변수 값의 이름


class Write(CreateView):
    model = Post # model
    form_class = PostForm # 폼
    success_url = reverse_lazy('blog:list') # 성공시 보내줄 url


class Detail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class Update(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']
    #success_url = reverse_lazy('blog:list')
    # intial 기능
    def get_initial(self):
        initial = super().get_initial()
        post = self.get_object() # pk 기반으로 객체를 가져옴
        initial['title'] = post.title
        initial['content'] = post.content
        return initial
    
    def get_success_url(self):
        post = self.get_object()
        return reverse('blog:detail' , kwargs={'pk' : post.pk})
    
    #def get_absolute_url(self):


class Delete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:list')


class DetailView(View):
    def get(self, request, post_id): # post_id : 데이터베이스 post_id 테이블 이름
        # list -> object 삼세 페이지 -> 상세 페이지 하나의 내용
        # pk 값을 왔다갔다, 하나의 인자

        # DB 방문
        # 해당 글
        post = Post.objects.get(pk=post_id)
        # 댓글
        #comments
        pass
    def post():
        pass

### Comment
class CommentWrite(View):
    def get(self, request):
        pass
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            # 사용자에게 댓글 내용을 받아옴
            content = form.cleaned_data['content']
            # 해당 아이디에 해당하는 글 불러옴
            post = Post.objects.get(pk=post_id)

            comment = Comment.objects.create(post=post, contetn=content)
            return redirect('blog:list', pk=post_id)