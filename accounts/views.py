from django.shortcuts import redirect, render
from . forms import SignupForm, LoginForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from shop.utils.collab_filtering import  *
from shop.models import Post
from shop.utils.produce_dataset import produce_dataset
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

# Create your views here.
def signup(request):
    if request.method == 'POST':
        print("before SignupForm")
        form = SignupForm(request.POST)
        print("before valid")
        print(form.is_valid())
        if form.is_valid():
            form.save()
            print("after valid, save")
            return redirect(settings.LOGIN_URL) # 회원가입에 성공하면, LOGIN 페이지로 이동
    else:
        print("method = get")
        form = SignupForm()
    return render(request, 'accounts/signup_form.html',
                  {'form': form,})


@login_required
def profile(request):
    #produce_dataset()
    rated_qs = Post.objects.filter(rating__user=request.user)
    not_rated_qs = Post.objects.exclude(rating__user=request.user)
    point = Post.objects.order_by('-score')[0:8]
    recommendation = user_recommendations(str(request.user))
    recommend_restaurant_list = []
    for tuple in recommendation:
        object = Post.objects.get(title = tuple[1])
        recommend_restaurant_list.append(object)

    return render(request, 'accounts/profile.html',
                  {'recommendation': recommend_restaurant_list,
                  'rated': rated_qs,
                  'not_rated': not_rated_qs,
                  'point' : point,
                  })


def login(request):
    providers = []
    for provider in get_providers():
    # social_app속성은 provider에는 없는 속성입니다.
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)
    return auth_login(request,
        authentication_form=LoginForm,
        template_name='accounts/login_form.html',
        extra_context={'providers': providers,
                       },

        )

