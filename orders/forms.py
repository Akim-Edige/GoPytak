from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from orders.models import Order, Service, EquipmentSubCategory
from users.models import User
from users.tasks import send_email_verification
from django.utils.timezone import now


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control py-4',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-4',
            'placeholder': 'Password'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'repeat password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class OrderForm(forms.ModelForm):
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'цена'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'описание'}))

    class Meta:
        model = Order
        fields = ('price', 'description')


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['customer', 'service', 'subcategory', 'price', 'description']
#
#     # Customize fields if needed
#     customer = forms.ModelChoiceField(
#         queryset=User.objects.all(),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     service = forms.ModelChoiceField(
#         queryset=Service.objects.all(),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     subcategory = forms.ModelChoiceField(
#         queryset=EquipmentSubCategory.objects.all(),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     price = forms.DecimalField(
#         max_digits=10, decimal_places=2,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'})
#     )
#
#     description = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your order'})
#     )


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'email', 'username')
