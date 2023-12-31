from django.shortcuts import redirect, render, get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from accounts.views import check_role_vendor
from menu.models import Category,Medicine_lobby
from menu.forms import CategoryForm,Medicine_lobbyForm
from django.template.defaultfilters import slugify


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

# Create your views here.

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)

def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
 
    context = {
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/vprofile.html',context)


@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render(request, 'vendor/menu_builder.html',context)

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def Medicine_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    Medicine_types = Medicine_lobby.objects.filter(vendor=vendor,category=category)
    context = {
        'Medicine_types':Medicine_types,
        'category':category,
    }
    return render(request, 'vendor/Medicine_by_category.html',context)

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            form.save() #here cat_id will be generated
            category.slug = slugify(category_name) + '-' +str(category.id)
            category.save()
            messages.success(request,'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, 'vendor/add_category.html',context)

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html', context)

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully!')
    return redirect('menu_builder')

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def add_med(request):
    if request.method == 'POST':
        form = Medicine_lobbyForm(request.POST, request.FILES)
        if form.is_valid():
            Medicine_title = form.cleaned_data['Medicine_title']
            med = form.save(commit=False)
            med.vendor = get_vendor(request)
            med.slug = slugify(Medicine_title)
            form.save()
            messages.success(request,'Medicine added successfully!')
            return redirect('Medicine_by_category',med.category.id)
        else:
            print(form.errors)
    else:
        form = Medicine_lobbyForm()
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
        context = {
            'form': form,
        }

    return render(request, 'vendor/add_med.html', context)




@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def edit_med(request,pk=None):
    med = get_object_or_404(Medicine_lobby, pk=pk)
    if request.method == 'POST':
        form = Medicine_lobbyForm(request.POST,request.FILES, instance=med)
        if form.is_valid():
            Medicine_title = form.cleaned_data['Medicine_title']
            med = form.save(commit=False)
            med.vendor = get_vendor(request)
            med.slug = slugify(Medicine_title)
            form.save()
            messages.success(request,'Medicines list updated successfully!')
            return redirect('Medicine_by_category',med.category.id)
        else:
            print(form.errors)
    else:
        form = Medicine_lobbyForm(instance=med)
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form':form,
        'med':med,
    }
    return render(request,'vendor/edit_med.html', context)


@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def delete_med(request, pk=None):
    med = get_object_or_404(Medicine_lobby,pk=pk)
    med.delete()
    messages.success(request,'Med has been deleted successfully!')
    return redirect('Medicine_by_category',med.category.id)