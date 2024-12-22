from django.urls import path
from .views import *

urlpatterns =[
    path('chome',CustomerHomeView.as_view(),name='home'),
    path('plist/<str:cat>',ProductListView.as_view(),name='plist'),
    path('pdetail/<int:id>',ProductDetailView.as_view(),name='pdetail'),
    path('addcart/<int:id>',addToCart,name='acart'),




    path('cartlist',CartListView.as_view(),name='cartlist'),
    path('incqty/<int:id>',IncreaseQuantity,name='incQuantity'),
    path('decqty/<int:id>',DecreaseQuantity,name='decQuantity'),
    path('removeitem/<int:id>',deleteCartItem,name='delcart'),
    path('order/<int:id>',placeOrder,name='order'),
    path('orderlist',OrderListView.as_view(),name='lorder'),
    path('corder/<int:id>',cancellOrder,name='cancelorder'),
    path('searchproduct',searchproduct,name='search'),

    path('deleteorder/<int:id>/',deleteOrder, name='deleteorder'),



    path('product/<int:id>/review/', add_review, name='add_review'),
    path('review/<int:review_id>/update/', update_review, name='update_review'),
    path('product/<int:pk>/reviews/', view_reviews, name='view_reviews'),
    path('review/<int:id>/delete/', delete_review, name='delete_review'),
    path('reviews/<int:pk>/',view_reviews, name='view_reviews'),
    


]