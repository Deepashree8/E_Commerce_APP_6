from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Vendor,Category,Product,Cart,Review,Order


# def category_list(request):
#     categories=Category.objects.all()
#     return render(request,'App/layouts/category_list.html',{'categries':categories})


# def dashboard(request):
#     vendor = None
#     products = []
#     orders = []

#     # Handle POST request
#     if request.method == 'POST':
#         vendor_name = request.POST.get('vendor_name')

#         try:
#             # Find the vendor by store_name (case-insensitive)
#             vendor = Vendor.objects.get(store_name__iexact=vendor_name)

#             # Fetch products and orders related to the vendor
#             products = Product.objects.filter(postman=vendor.user)  # Products posted by the vendor
#             orders = Order.objects.filter(vendor=vendor)  # Fetch orders associated with the vendor

#         except Vendor.DoesNotExist:
#             messages.error(request, "Vendor not found.")  # Display an error message if vendor not found

#     return render(request, 'App/layouts/dashboard.html', {
#         'vendor': vendor,
#         'products': products,
#         'orders': orders
#     })

# def enter_name(request):
#     return render(request,'App/layouts/enter_vendor_name.html')

def place_order(request):
    cart_items=Cart.objects.filter(customer=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('view_cart')
    for cart_item in cart_items:
        # Create an order for each cart item
        Order.objects.create(
            customer=request.user,
            product=cart_item.product,
            quantity=cart_item.quantity,
            status='Pending'  # Initial status
        )
        
        
    # Clear the cart after placing the order
    cart_items.delete()
    
    return redirect('home')  #"replace with order succes page later"


















def post_reviews(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=='POST':
        content=request.POST['content']
        customer=request.user
        rating=request.POST['rating']
        
        reviews=Review.objects.create(
            product=product,
            content=content,
            customer=customer,
            rating=rating
        )
        reviews.save()
        return redirect('product_reviews',pk=product.pk)
    
    else:
        return render(request,'App/layouts/postreview.html',{'product':product})
        
    
def product_reviews(request,pk):
    product=get_object_or_404(Product,pk=pk)
    reviews=Review.objects.filter(product=product)
    return render(request,'App/layouts/review.html',{'product':product,'reviews':reviews})


def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.delete()
    return redirect('view_cart')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(customer=request.user, product=product)

    if not created:
        # If the item already exists in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart') 

# Redirect to view cart page after adding to cart
@login_required
def view_cart(request):
    username = request.user.username
    cart_items = Cart.objects.filter(customer=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'App/layouts/view_cart.html', {'cart_items': cart_items, 'total_price': total_price,'username':username})


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Fetch the vendor details related to the product's postman
    vendor = get_object_or_404(Vendor, user=product.postman)
    return render(request, 'App/layouts/product_details.html', {'product': product, 'vendor': vendor,'category':product.category})

def about(request):
    return render(request,'App/layouts/about.html')

def category_product(request,category_id):
    category=Category.objects.get(id=category_id)
    products=Product.objects.filter(category=category)
    return render(request,'App/layouts/category_product.html',{'products':products,'category':category}) 

def post_product(request):
    if request.method=='POST':
        name=request.POST['productname']
        category_id = request.POST['category']  
        category = Category.objects.get(id=category_id)  # Fetch the category object
        description=request.POST['description']
        price=request.POST['price']
        stock=request.POST['stock']
        image=request.FILES['image'] 
        is_trending = request.POST.get('is_trending') == 'true'
        
        vendor_name = request.POST.get('vendorname')  # Get the vendor's name from the form
        try:
            vendor_user = User.objects.get(username=vendor_name)  # Fetch the User instance for that vendor
        except User.DoesNotExist:
            messages.error(request, "Vendor not found.")
            return redirect('post_product')
        
        
        product=Product.objects.create(
            postman=vendor_user,
            name=name,
            category=category,
            description=description,
            price=price,
            stock=stock,
            image=image,
            is_trending=is_trending
        )
        product.save()
        messages.success(request, "Product posted successfully.")
        return redirect('post_product')
    
    categories = Category.objects.all()
    return render(request,'App/layouts/postman.html',{'categories':categories})

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if the user with the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('user_register')

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Log in the user after registration
        login(request, user)

        # Add a success message
        messages.success(request, f"Welcome, {username}! You have successfully registered.")

        # Redirect to home page after successful registration
        return redirect('home')  

    return render(request,'App/layouts/user_register.html')

def index(request):
    trending_products = Product.objects.filter(is_trending=True)
    categories=Category.objects.all()
    return render(request,'App/layouts/index.html',{'categories':categories,'trending_products':trending_products})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to your home page or desired page

def vendor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        whatsapp_number = request.POST['phone_number']
        store_name=request.POST['store_name']
        

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('vendor_register')

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Create a Vendor profile associated with the user
        vendor = Vendor(user=user, whatsapp_number=whatsapp_number,store_name=store_name)
        vendor.save()

        # Log in the vendor after registration
        login(request, user)

        # Add a success message
        messages.success(request, f"Welcome, {username}! You have successfully registered as a vendor.")

        # Redirect to home page or vendor dashboard
        return redirect('post_product')  # Or redirect to the vendor dashboard if needed
    return render(request,'App/layouts/vendor_register.html')