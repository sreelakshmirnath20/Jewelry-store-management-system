from django.shortcuts import render,redirect,get_object_or_404
from account.models import *
from django.views import View
from django.views.generic import TemplateView,ListView,CreateView,DetailView
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Avg


# Create your views here.
def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please login First!!")
            return redirect('log')
    return inner
decorators=[never_cache,signin_required]


@method_decorator(decorator=decorators,name='dispatch')
class CustomerHomeView(ListView):
    template_name="home.html"
    queryset=Products.objects.all()
    context_object_name='products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Products.objects.all().order_by('-datetime')[:8]
        context['latest_products'] = latest_products        
        return context

@method_decorator(decorator=decorators,name='dispatch')
class ProductListView(ListView):
    template_name = "productlist.html"
    queryset = Products.objects.all()  # Default queryset
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = self.kwargs.get('cat', None)
        context['cat'] = cat  # Ensure 'cat' is passed to the template
        return context

    def get_queryset(self):
        cat = self.kwargs.get('cat', None)

        # Store the category in session (optional)
        if cat:
            self.request.session['category'] = cat
        else:
            self.request.session['category'] = None

        # Filter the queryset based on the category if provided
        queryset = self.queryset
        if cat:
            queryset = queryset.filter(category=cat)

        # Get the sorting filter from the query parameters
        sort_option = self.request.GET.get('sort', None)
        if sort_option == "price_low_to_high":
            queryset = queryset.order_by('price')  # Sort by price ascending
        elif sort_option == "price_high_to_low":
            queryset = queryset.order_by('-price')  # Sort by price descending

        return queryset


        
@method_decorator(decorator=decorators,name='dispatch')
class ProductDetailView(DetailView):
    template_name="productDetails.html"
    queryset=Products.objects.all()
    context_object_name="product"
    pk_url_kwarg="id"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        reviews = product.reviews.all()

        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

        context['reviews'] = reviews
        context['avg_rating'] = avg_rating if avg_rating else 0 

        related_products = Products.objects.filter(category=product.category).exclude(id=product.id)[:4]
        
        for related_product in related_products:
            related_reviews = related_product.reviews.all()
            related_avg_rating = related_reviews.aggregate(Avg('rating'))['rating__avg']
            related_product.avg_rating = related_avg_rating if related_avg_rating else 0 

        context['related_products'] = related_products

        return context


def product_detail(request, id):
    product = get_object_or_404(Products, pk=id)
    
    avg_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
    
    form = ProductReviewForm() 
    
    return render(request, 'productdetail.html', {
        'product': product,
        'avg_rating': avg_rating,
        'form': form,
        'category': product.category, 
    })




def addToCart(request,*args,**kwargs):
    try:
        pid=kwargs.get('id')
        product=Products.objects.get(id=pid)
        user=request.user
        cartcheck=Cart.objects.filter(product=product,user=user).exists()
        if cartcheck:
            cartitem=Cart.objects.get(product=product,user=user)
            cartitem.quantity+=1
            cartitem.save()
            messages.success(request,"Cart item quantity increased!!")
            return redirect('home')
        else:
            Cart.objects.create(product=product,user=user)
            messages.success(request,f"{product.title}Added To cart!!")
            return redirect('home')
    except Exception as e:
        print(e)
        messages.warning(request,"Something went WRONG!!")
        return redirect('home')















@method_decorator(decorator=decorators,name='dispatch')   
class CartListView(ListView):
    template_name="cartlist.html"
    queryset=Cart.objects.all()
    context_object_name="carts"
    def get_queryset(self):
        qs=self.queryset.filter(user=self.request.user)
        return qs
    
decorators 
def IncreaseQuantity(request,*args,**kwrgs):
    try:
        cid=kwrgs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.quantity+=1
        cart.save()
        return redirect('cartlist')
    except:
        messages.warning(request,"Something went wrong!!")
        return redirect('cartlist')
    
decorators 
def DecreaseQuantity(request, *args, **kwargs):
    try:
        cid = kwargs.get('id')
        cart = Cart.objects.get(id=cid)
        if cart.quantity==1:
            cart.delete()
            return redirect('cartlist')
        else:
            cart.quantity-=1 
            cart.save()
            return redirect('cartlist')
            
    except:
        messages.warning(request, "Something went wrong!!")
        return redirect('cartlist')
    
decorators 
def deleteCartItem(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.delete()
        messages.success(request,"Item removed from cart!!")
        return redirect('cartlist')
    except:
        messages.warning(request,"Something went wrong!!")
        return redirect('cartlist')
    
decorators 
def placeOrder(request,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        Order.objects.create(product=cart.product,user=request.user,quantity=cart.quantity)
        cart.delete()

        # send_mail
        subject="Jewlery Order Notification"
        msg=f"Order for {cart.product.title} is Placed!!"
        f_rom='sreelakshmirnathclt@gmail.com'
        to_id=request.user.email
        send_mail(subject,msg,f_rom,[to_id],fail_silently=True)

        


        messages.success(request,f'{cart.product.title}\'s Order placed!!')
        return redirect('cartlist')
    except:
        messages.warning(request,"Something went wrong!!")
        return redirect('cartlist')
    
@method_decorator(decorator=decorators,name='dispatch')  
class OrderListView(ListView):
    template_name="orderlist.html"
    queryset=Order.objects.all()
    context_object_name="orders"
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

decorators
def cancellOrder(request,**kwargs):
    try:
        oid=kwargs.get('id')
        order=Order.objects.get(id=oid)
        order.status="Cancelled"
        order.save()
        messages.success(request,"Order Cancelled!!")
        return redirect('lorder')
    except:
        messages.warning(request,"Something went wrong!!")
        return redirect('lorder')
    



def searchproduct(request, *args, **kwargs):
    keyword = request.POST.get('searchkey', '').strip()  # Get the search keyword
    cat = request.session.get('category', None)  # Get category from session

    if keyword:
        # Filter by category if it exists; otherwise, filter only by the keyword
        if cat:
            products = Products.objects.filter(title__icontains=keyword, category=cat)
        else:
            products = Products.objects.filter(title__icontains=keyword)

        return render(request, "productlist.html", {"products": products, "cat": cat})
    else:
        # Redirect to 'plist' if category is available; otherwise, to 'home'
        if cat:
            return redirect('plist', cat=cat)
        else:
            return redirect('home')  # Redirect to a safe fallback when no category is set

    

    
decorators
def deleteOrder(request, **kwargs):
    try:
        oid = kwargs.get('id')
        order = Order.objects.get(id=oid)

        # Ensure only canceled orders can be deleted
        if order.status == "Cancelled":
            order.delete()
            messages.success(request, "Order deleted successfully!")
        else:
            messages.error(request, "Only canceled orders can be deleted.")
        return redirect('lorder')
    except Order.DoesNotExist:
        messages.error(request, "Order not found!")
        return redirect('lorder')
    except Exception as e:
        messages.error(request, "Something went wrong!")
        print(e)
        return redirect('lorder')








@signin_required
def view_reviews(request, pk):
    product = get_object_or_404(Products, pk=pk)
    reviews = ProductReview.objects.filter(product=product)
    # reply_form = ReviewReplyForm()

    if request.method == 'POST':
        # Handle review deletion
        if 'delete_review' in request.POST:
            review_id = request.POST.get('delete_review')
            review = get_object_or_404(ProductReview, id=review_id)
            if request.user.is_superuser:
                review.delete()
                return redirect('view_reviews', pk=pk)

        # Handle replying to a review
        # if 'reply_to_review' in request.POST:
        #     review_id = request.POST.get('reply_to_review')
        #     review = get_object_or_404(ProductReview, id=review_id)
            
        #     # Check if a reply already exists for this review
        #     existing_reply = ReviewReply.objects.filter(review=review).first()
        #     if existing_reply:
        #         messages.error(request, "A reply already exists for this review.")
        #         return redirect('view_reviews', pk=pk)

            # reply_form = ReviewReplyForm(request.POST)
            # if reply_form.is_valid() and request.user.is_superuser:
            #     reply = reply_form.save(commit=False)
            #     reply.review = review
            #     reply.admin = request.user
            #     reply.save()
            #     return redirect('view_reviews', pk=pk)

    return render(request, 'view_reviews.html', {
        'product': product,
        'reviews': reviews,
        # 'reply_form': reply_form,
    })



@signin_required
def add_review(request, id):
    product = get_object_or_404(Products, id=id)
    has_delivered_order = Order.objects.filter(
        user=request.user,
        product=product,
        status='Delivered'
    ).exists()
    
    if not has_delivered_order:
        messages.error(request, "You can only review products you have bought and received.")
        return redirect('pdetail', id=product.id)
    
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Your review has been added successfully!")
            return redirect('pdetail', id=product.id)
    else:
        form = ProductReviewForm()
    
    return render(request, 'add_review.html', {'form': form, 'product': product})


@signin_required
def update_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)

    # Ensure the product's category exists before rendering the template
    if not review.product.category:
        # Redirect to a fallback page if the category is missing
        return redirect('shop')

    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('pdetail', kwargs={'id': review.product.id}))
    else:
        form = ProductReviewForm(instance=review)

    return render(request, 'add_review.html', {'form': form, 'review': review})


@signin_required
def delete_review(request, id):
    review = get_object_or_404(ProductReview, id=id, user=request.user)
    product_id = review.product.id
    if request.method == 'POST':
        review.delete()
        return redirect('pdetail', id=product_id)
    return render(request, 'add_review.html', {'review': review})