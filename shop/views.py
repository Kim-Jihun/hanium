from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import RatingForm
from django.contrib.auth.decorators import login_required
from .models import Rating
from .utils.collab_filtering import *

# Create your views here.

def post_list(request):
    qs = Post.objects.all()
    return render(request, 'shop/post_list.html', {
        'shop_list':qs,
        'recomendation': user_recommendations(str(request.user))
    })

def post_detail(request, id):
    tag = request.GET.get('tag','')
    post = get_object_or_404(Post, id=id)
    next_post_list = Post.objects.filter(id__gt=post.id).order_by('id')
    prev_post_list = Post.objects.filter(id__lt=post.id).order_by('-id')

    if tag:
        next_post_list = next_post_list.filter(tag_set__name__iexact=tag)
        prev_post_list = prev_post_list.fitler(tag_set__name__iexact=tag)

    return render(request, 'shop/post_detail.html', {
        'post': post,
        'next_post': next_post_list.first(),
        'prev_post': prev_post_list.first(),
        'tag': tag,
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
                    record_check.score = form.score
                    return redirect('shop:detail', record_check.shop.pk)# 저장한 후 식당 상세페이지로 이동

                else:
                    rating = form.save(commit=False)# 유저가 그 식당을 평가한 레코드가 없다면...
                    rating.shop = shop
                    rating.user = request.user
                    rating.save()
                    rating.shop.calc_score()
                    return redirect('shop:detail', rating.shop.pk)# 저장한 후 식당 상세페이지로 이동
            else:
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

