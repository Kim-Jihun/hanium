from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import RatingForm, IndexForm
from django.contrib.auth.decorators import login_required
from .models import Rating
from .utils.collab_filtering import *
from django.urls import reverse
from shop.utils.crawling_restaurant.crawling import *
from django.db.models import Q

# Create your views here.

def data(request, keyword):
    post_rest(keyword)
    return redirect('shop:list')



def post_list(request):
    print(reverse('shop:list'))
    qs = Post.objects.all()

    return render(request, 'shop/post_list.html', {
        'shop_list':qs,
        'recommendation': user_recommendations(str(request.user))
    })

def post_detail(request, id):
    tag = request.GET.get('tag','')
    post = get_object_or_404(Post, id=id)

    next_post_list = Post.objects.filter(id__gt=post.id).order_by('id')
    prev_post_list = Post.objects.filter(id__lt=post.id).order_by('-id')

    if tag:
        next_post_list = next_post_list.filter(tag_set__name__iexact=tag)
        prev_post_list = prev_post_list.filter(tag_set__name__iexact=tag)

    return render(request, 'shop/post_detail.html', {
        'post': post,
        'next_post': next_post_list.first(),
        'prev_post': prev_post_list.first(),
        'tag': tag,
    })

def post_home(request):
    recommendation = user_recommendations(str(request.user))
    recommend_restaurant_list = []

    if len(recommendation) != 0:
        for tuple in recommendation:
            object = Post.objects.get(title = tuple[1])
            recommend_restaurant_list.append(object)
    else:
        pass

    star8 = Post.objects.all().order_by('-score')[0:8]

    if request.method =='POST':
        form = IndexForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(form.cleaned_data)
            '''사전 key: title, location, menu, price'''
            query = Post.objects.filter(Q(tag_set__location__icontains=cleaned_data['location'])&Q(tag_set__menu__icontains=cleaned_data['menu'])&
                                        Q(tag_set__avg_price__gte=int(cleaned_data['price']))&Q(tag_set__avg_price__lte=int(cleaned_data['price'])+2000))

            return render(request, 'shop/post_home.html',
                {
                'shop_list':query,
                'star8' : star8,
                'form':form,
                'recommendation': recommend_restaurant_list,
                })



        else:
            form.errors
    else:
        form = IndexForm()


    return render(request, 'shop/post_home.html',
        {
        'star8' : star8,
        'form' : form,
        'recommendation': recommend_restaurant_list
        })


@login_required
def rating_new(request, shop_pk):
    # shop = Shop.objects.get(pk=shop_pk)
    shop = get_object_or_404(Post, pk=shop_pk)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_query_set = Rating.objects.all()
            if(rating_query_set): #사용자 평가가 있으면....
                record_check = rating_query_set.filter(user = request.user, shop = shop)## 같은 유저가 같은 식당을 평가한 레코드가 있으면...

                if record_check:
                    #print(record_check[0].score)
                    record_check.update(score = int(form.cleaned_data['score']))
                    #return redirect('shop:detail', record_check[0].shop.pk)# 저장한 후 식당 상세페이지로 이동
                    #return redirect('shop:detail', 1)
                    return redirect(record_check[0])

                else:
                    rating = form.save(commit=False)# 유저가 그 식당을 평가한 레코드가 없다면...
                    rating.shop = shop
                    rating.user = request.user
                    rating.save()
                    rating.shop.calc_score()
                    return redirect('shop:detail', rating.shop.pk)# 저장한 후 식당 상세페이지로 이동
            else: # 사용자 평가가 한건도 없음
                rating = form.save(commit=False)
                rating.shop = shop
                rating.user = request.user
                rating.save()
                rating.shop.calc_score()
                return redirect('shop:detail', rating.shop.pk)

    else:
        form = RatingForm()
    return render(request, 'shop/rating_form.html', {
        'form': form,
    })


def recommendation(request):

    #produce_dataset()
    recommendation = user_recommendations(str(request.user))
    recommend_restaurant_list = []
    if len(recommendation) != 0:
        print("here")
        print(recommendation)
        for tuple in recommendation:
            object = Post.objects.get(title = tuple[1])
            recommend_restaurant_list.append(object)
    else:
        pass
    return render(request, 'shop/recommendation_list.html',
                  {'recommendation': recommend_restaurant_list,})


def select_shop(request):
    #print(request.user)
    #rated_qs=Rating.objects.select_related("shop").filter(user__username__icontains=request.user)
    #not_rated_qs=Rating.objects.select_related("shop").exclude(user__username__icontains=request.user)
    rated_qs = Post.objects.filter(rating__user__username__icontains=request.user)
    not_rated_qs = Post.objects.exclude(rating__user__username__icontains=request.user)

    #print(rated_qs)
    #print(not_rated_qs)

    return render(request, 'shop/rated_not_rated_respectively.html', {
        'rated': rated_qs,
        'not_rated': not_rated_qs,
        'recommendation': user_recommendations(request.user.username)
    })


def post_tag(request, tag):
    qs_tag = Post.objects.filter(tag_set__location__icontains=tag)


    return render(request, 'shop/post_tag.html',{
        'tag': tag,
        'shop_list_tag': qs_tag
    })




