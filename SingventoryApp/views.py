from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import SVUserForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from .forms import SVUserForm, BorrowForm, UserUpdateForm, CategoryForm, EquipmentForm, SVUserFormAdmin
from django.contrib.auth.decorators import login_required
from .models import Category, Equipment, SVUser, Borrow, Notification
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.conf import settings
from django.core.mail import EmailMessage, message
from django.urls import reverse




def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Account Activation'
    email_body = render_to_string('SingventoryApp/activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })


    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,to=[user.email])
    email.send()



# Create your views here.

   
#forgot password
def PasswordResetView(request):
    return render(request, 'SingventoryApp/reset_password.html')

@csrf_protect
def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.activated == "Inactive":
                messages.error(request, "Please activate your account through your email.")

            elif user.activated == "Active":
                login(request,user)
                if user.is_superuser:
                    return redirect('/svadmin')

                elif user.category == 'Admin':
                    return redirect('/svadmin')
            
                elif user.category == 'User':
                    return redirect(userhome)

        else:
            messages.error(request, "Email or Password is incorrect.")
            # return render(request, 'SingventoryApp/login.html', {'user':user, 'email':email, 'password':password})
            
    
    return render(request, 'SingventoryApp/login.html')


@csrf_protect
def reg(request):
    form = SVUserForm()
    if request.method == 'POST':
        form = SVUserForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.save()
            password = request.POST.get('password2')
            password1 = request.POST.get('password1')
            if password == password1:
                user.set_password(password)
                user.save()
                # login(request,user) 
                send_activation_email(user, request)
                messages.success(request, "Please verify your account through your email.")


                # return redirect(userhome)
            else:
                messages.error(request, "Password does not match!")
                return redirect(reg)

            # login(request,user)    
            # return redirect(userhome)
        else:
            messages.error(request, 'Email is taken!!!')
            
    return render(request, 'SingventoryApp/reg.html', {'form': form})

#search 
@login_required(login_url=home)
def searchBar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            equipments = Equipment.objects.filter(name__icontains=query) 
            return render(request, 'SingventoryApp/user/searchbar.html', {'equipments':equipments})
        else:
            print("No information to show")
            return render(request, 'SingventoryApp/user/searchbar.html', {})


@login_required(login_url=home)
@csrf_protect
def userhome(request):
    equipmentsl = Equipment.objects.all().exclude(visibility='Inactive').order_by('name')
    cate = Category.objects.all()
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    page = request.GET.get('page', 1)
  
    paginator = Paginator(equipmentsl, 9)
    try:
        equipments = paginator.page(page)
    except PageNotAnInteger:
        equipments = paginator.page(1)
    except EmptyPage:
        equipments = paginator.page(paginator.num_pages)

    return render(request, 'SingventoryApp/user/index.html',{'equipments':equipments,'cate':cate,'notifications':notifications, 'unreadcount':unreadcount})

@login_required(login_url=home)
@csrf_protect
def userequip(request):
    equipmentsl = Equipment.objects.all().exclude(visibility='Inactive').order_by('name')
    cate = Category.objects.all()
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    page = request.GET.get('page', 1)
  
    paginator = Paginator(equipmentsl, 9)
    try:
        equipments = paginator.page(page)
    except PageNotAnInteger:
        equipments = paginator.page(1)
    except EmptyPage:
        equipments = paginator.page(paginator.num_pages)

    return render(request, 'SingventoryApp/user/equipment.html',{'equipments':equipments,'cate':cate,'notifications':notifications, 'unreadcount':unreadcount})


@login_required(login_url=home)
def categoryview(request, pk):
    equipments = Equipment.objects.filter(category=pk)
    cate = Category.objects.all()
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()

    # item.visibility = 'Inactive'
    return render(request, 'SingventoryApp/user/index.html', {'equipments':equipments,'cate':cate,'notifications':notifications, 'unreadcount':unreadcount})

@login_required(login_url=home)
def userabout(request):
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    return render(request, 'SingventoryApp/user/about.html',{'notifications':notifications, 'unreadcount':unreadcount})

@login_required(login_url=home)
@csrf_protect
def useritem(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    form = BorrowForm()
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        user = request.user
        equipmentname = equipment
        if form.is_valid():
            quantity = int(request.POST.get('quantity'))
            totalq = equipment.quantity
            if quantity>totalq or quantity<=0:
                message = 'Please enter a valid number of equipment.'
                return render(request, 'SingventoryApp/user/item.html', {'equipment':equipment, 'form':form, 'message':message,'notifications':notifications, 'unreadcount':unreadcount})

            else:
                totalq = totalq - quantity
                Equipment.objects.filter(pk=pk).update(quantity=totalq)    
                obj = form.save(commit=False)
                obj.user = user
                obj.equipment = equipmentname
                obj.save()
                equipment = Equipment.objects.get(pk=pk)
                message='Request sent successfully.'
                return render(request, 'SingventoryApp/user/item.html', {'equipment':equipment, 'form':form, 'message':message,'notifications':notifications, 'unreadcount':unreadcount})
        else:   
            return render(request, 'SingventoryApp/user/item.html', {'equipment':equipment, 'form':form,'notifications':notifications, 'unreadcount':unreadcount})

            
    return render(request, 'SingventoryApp/user/item.html', {'equipment':equipment, 'form':form,'notifications':notifications, 'unreadcount':unreadcount})

@login_required(login_url=home)
def userprofile(request):
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    user = request.user
    borrowed = Borrow.objects.filter(user=user.email).filter(status='Approved') | Borrow.objects.filter(user=user.email).filter(status='Return') | Borrow.objects.filter(user=user.email).filter(status='Pending') | Borrow.objects.filter(user=user.email).filter(status='Possession')
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    borrowed = borrowed.order_by('-date')
    return render(request, 'SingventoryApp/user/profile.html', {'borrowed':borrowed,'notifications':notifications, 'unreadcount':unreadcount})

@login_required(login_url=home)
@csrf_protect
def userprofileupdate(request):
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    user = request.user
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()

    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'SingventoryApp/user/updateprofile.html', {'form':form,'notifications':notifications, 'unreadcount':unreadcount})

@login_required(login_url=home)
def userReturnPage(request,pk):
    unreadcount = Notification.objects.filter(user=request.user).filter(readStatus='unread').count()
    user = request.user
    notifications = Notification.objects.all().filter(user=request.user).order_by('-date')
    returnEquip = Borrow.objects.get(pk=pk)
    equip = returnEquip.equipment

    if request.method == 'POST':        
        rQty = int(request.POST.get('qty'))
        if rQty>returnEquip.quantity or rQty==0:
            message = 'Please enter a valid number of equipment to return.'
            return render(request, 'SingventoryApp/user/return.html', {'notifications':notifications, 'unreadcount':unreadcount, 'message':message})

        else:
            updatedQty = returnEquip.quantity - rQty
            Borrow.objects.create_borrow(user, equip, rQty, "Return")
            returnEquip.quantity = updatedQty
            returnEquip.save()

        # status = 'Return'
        # Borrow.objects.filter(pk=pk).update(status=status)

            return render(request, 'SingventoryApp/user/return.html', {'notifications':notifications, 'unreadcount':unreadcount, 'rqty':rQty})
        

    return render(request, 'SingventoryApp/user/return.html', {'notifications':notifications, 'unreadcount':unreadcount, 'returnEquip':returnEquip})

@login_required(login_url=home)
@csrf_protect
def userReturn(request, pk):
    status = 'Return'
    # Borrow.objects.filter(pk=pk).update(status=status)
    borrow = Borrow.objects.get(pk=pk)
    borrow.status = status
    borrow.save()

    return redirect(userprofile)



@login_required(login_url=home)
@csrf_protect
def userCancel(request, pk):
    borrowed = Borrow.objects.get(pk=pk)
    epk = borrowed.equipment.pk
    equip = Equipment.objects.get(pk=epk)
    totalq = borrowed.equipment.quantity
    bquantity = borrowed.quantity

    totalq = totalq + bquantity
    Equipment.objects.filter(pk=epk).update(quantity=totalq)
    status = 'Cancelled'
    Borrow.objects.filter(pk=pk).update(status=status)
    Notification.objects.create_notification(request.user,equip,"cancelled")


    return redirect(userprofile)

@login_required(login_url=home)
@csrf_protect
def notifRead(request, pk):
    status = 'read'
    Notification.objects.all().filter(user=request.user).filter(pk=pk).update(readStatus=status)

    return redirect(userprofile)

# Admin
@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
def adminHome(request):
    # users = SVUser.objects.all().exclude(visibility='Inactive').order_by('name')
    usercount = SVUser.objects.count()
    catcount = Category.objects.count()
    equipcount = Equipment.objects.count()
    borrowcount = Borrow.objects.filter(status='Possession').count()
    borrowedl = Borrow.objects.order_by('-date').exclude(status='Cancelled')
    page = request.GET.get('page', 1)
  
    paginator = Paginator(borrowedl, 10)
    try:
        borrowed = paginator.page(page)
    except PageNotAnInteger:
        borrowed = paginator.page(1)
    except EmptyPage:
        borrowed = paginator.page(paginator.num_pages)

    return render(request, 'SingventoryApp/admin/adminindex.html',{'borrowed':borrowed,'ucount':usercount,'ccount':catcount,'ecount':equipcount,'bcount':borrowcount})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
def adminViewUser(request):
    svusersl = SVUser.objects.all().order_by('name')
    page = request.GET.get('page', 1)
  
    paginator = Paginator(svusersl, 5)
    try:
        svusers = paginator.page(page)
    except PageNotAnInteger:
        svusers = paginator.page(1)
    except EmptyPage:
        svusers = paginator.page(paginator.num_pages)

    return render(request, 'SingventoryApp/admin/viewUser.html',{'svusers':svusers})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
def adminViewEquipment(request):
    equipmentsl = Equipment.objects.all().order_by('name')
    page = request.GET.get('page', 1)
  
    paginator = Paginator(equipmentsl, 5)
    try:
        equipments = paginator.page(page)
    except PageNotAnInteger:
        equipments = paginator.page(1)
    except EmptyPage:
        equipments = paginator.page(paginator.num_pages)

    return render(request, 'SingventoryApp/admin/viewEquipment.html',{'equipments':equipments})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
def adminViewCategory(request):
    categoriesl = Category.objects.all().order_by('name')
    page = request.GET.get('page', 1)
  
    paginator = Paginator(categoriesl, 9)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    return render(request, 'SingventoryApp/admin/viewCategory.html',{'categories':categories})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminAddCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Category added successfully."

        else:
            message = "Category already exists."

        return render(request, 'SingventoryApp/admin/addCategory.html', {'form':form, 'message':message})

    return render(request, 'SingventoryApp/admin/addCategory.html', {'form':form})


@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminAddEquipment(request):
    form = EquipmentForm()
    if request.method == 'POST':
        form = EquipmentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            message = "Equipment added successfully."
            return render(request, 'SingventoryApp/admin/addEquipment.html', {'form':form, 'message':message})

    return render(request, 'SingventoryApp/admin/addEquipment.html', {'form':form})


@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminAddUser(request):
    form = SVUserFormAdmin()
    if request.method == 'POST':
        form = SVUserFormAdmin(request.POST)
        if form.is_valid():
            user = form.save()
            password = "Singventory123"
            user.set_password(password)
            user.save()
            message = "User added successfully."
            return render(request, 'SingventoryApp/admin/addUser.html', {'form':form, 'message':message})

    return render(request, 'SingventoryApp/admin/addUser.html', {'form':form})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
def adminProfile(request):
    return render(request, 'SingventoryApp/admin/profile.html')


@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminProfileUpdate(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()

    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'SingventoryApp/admin/profileUpdate.html', {'form':form})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminEditCategory(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            
    else:
        form = CategoryForm(instance=category)

    return render(request, 'SingventoryApp/admin/editCategory.html', {'form':form})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminEditUser(request, pk):
    user = SVUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = SVUserFormAdmin(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
    else:
        form = SVUserFormAdmin(instance=user)

    return render(request, 'SingventoryApp/admin/editUser.html', {'form':form})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminDelUser(request, pk):
    user = SVUser.objects.get(pk=pk)
    user.delete()

    return redirect(adminViewUser)


@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminDelCategory(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()

    return redirect(adminViewCategory)

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminEditEquipment(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'SingventoryApp/admin/editEquipment.html', {'form':form})

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminDelEquipment(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    equipment.delete()

    return redirect(adminViewEquipment)

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminApprove(request, pk):
    borrowed = Borrow.objects.get(pk=pk)
    userr = SVUser.objects.get(pk=borrowed.user.pk)
    equip = Equipment.objects.get(pk=borrowed.equipment.pk)
    status = 'Approved'
    Borrow.objects.filter(pk=pk).update(status=status)
    Notification.objects.create_notification(userr,equip,"approved")

    return redirect(adminHome)

@csrf_protect
@user_passes_test(lambda u: True if u.category=="Admin" else False )
def approveConfirm(request, pk):
    status = 'Possession'
    Borrow.objects.filter(pk=pk).update(status=status)

    return redirect(adminHome)

@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminReject(request, pk):
    borrowed = Borrow.objects.get(pk=pk)
    epk = borrowed.equipment.pk
    totalq = borrowed.equipment.quantity
    bquantity = borrowed.quantity
    userr = SVUser.objects.get(pk=borrowed.user.pk)
    equip = Equipment.objects.get(pk=borrowed.equipment.pk)

    totalq = totalq + bquantity
    Equipment.objects.filter(pk=epk).update(quantity=totalq)
    status = 'Rejected'
    Borrow.objects.filter(pk=pk).update(status=status)
    Notification.objects.create_notification(userr,equip,"rejected")

    return redirect(adminHome)


# to be done
@login_required(login_url=home)
@user_passes_test(lambda u: True if u.category=="Admin" else False )
@csrf_protect
def adminReturnConfirm(request, pk):
    borrowed = Borrow.objects.get(pk=pk)
    epk = borrowed.equipment.pk
    totalq = borrowed.equipment.quantity
    bquantity = borrowed.quantity
    totalq = totalq + bquantity

    Equipment.objects.filter(pk=epk).update(quantity=totalq)
    status = 'Returned'
    Borrow.objects.filter(pk=pk).update(status=status)

    return redirect(adminHome)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = SVUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, SVUser.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.activated = "Active"
        # user.is_staff = True
        user.save()
        
        # login(request, user)
        # return redirect('home')
        return redirect(reverse('login'))
    else:
        return HttpResponse('Activation link is invalid!')

# Logout
def logout_view(request):
    logout(request)
    return redirect('/')