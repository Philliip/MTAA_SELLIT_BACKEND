from django.urls import path

from apps.api.views import user, api_key, auth, city, category, image, offer

urlpatterns = [

    path('api_keys', api_key.ApiKeyManagement.as_view()),
    path('api_keys/<uuid:api_key_id>', api_key.ApiKeyDetail.as_view()),

    path('auth', auth.UserAuth.as_view(), name='auth-token-login'),
    path('logout', auth.LogoutManager.as_view(), name='auth-token-logout'),

    path('users', user.UserManagement.as_view()),
    path('users/<uuid:user_id>', user.UserDetail.as_view()),
    path('users/me', user.UserMe.as_view()),
    path('users/<uuid:user_id>/image', user.UserProfileImage.as_view(), name='profile_image'),

    path('cities', city.CityManagement.as_view()),
    path('cities/<uuid:city_id>', city.CityDetail.as_view()),

    path('categories', category.CategoryManagement.as_view()),
    path('categories/<uuid:category_id>', category.CategoryDetail.as_view()),

    path('images/<uuid:image_id>', image.ImageDetail.as_view()),

    path('offers', offer.OfferManagement.as_view()),
    path('offers/<uuid:offer_id>', offer.OfferDetail.as_view()),


]
