from django.urls import path 
from . import views 

urlpatterns=[
    path('',views.index,name='home'),
    path('register/user/',views.user_register,name='user_register'),
    path('register/vendor/',views.vendor_register,name='vendor_register'),
    path('post/product/',views.post_product,name='post_product'),
    # path('category/list/',views.category_list,name='category_list'),
    path('category/<int:category_id>/',views.category_product,name='category_product'),
    path('about/',views.about,name='about'),
    path('product_details/<int:pk>/',views.product_details,name='product_details'),
    path('cart/add/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/view/',views.view_cart,name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/review/<int:pk>/',views.product_reviews,name='product_reviews'),
    path('post/reviews/<int:pk>/',views.post_reviews,name='post_reviews'),
    path('place/order/',views.place_order,name='place_order'),
    # path('enter_name/',views.enter_name,name='name'),
    # path('dashboard/',views.dashboard,name='dashboard'),

]