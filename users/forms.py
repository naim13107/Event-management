from django import forms
import re
from django.contrib.auth.forms  import AuthenticationForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import Permission,Group
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Enter a strong password'
        }),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Confirm your password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'confirm_password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Choose a unique username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'email@example.com'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password1):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):  
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white',
            'placeholder': 'Enter your username'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white',
            'placeholder': 'Enter your password'
        })   
        
class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']   
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition',
                'placeholder': 'Enter role name (e.g., Moderator)'
            }),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Fixed the double 'fields' typo here
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'bio', 'profile_image']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'email@example.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': '+8801XXXXXXXXX'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
            }),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
       
        common_classes = (
            'w-full px-4 py-3 border border-orange-200 rounded-xl '
            'focus:outline-none focus:ring-2 focus:ring-orange-500 '
            'transition-all duration-200 placeholder-gray-400'
        )

        
        self.fields['old_password'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter current password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter new password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Confirm new password'
        })

class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-orange-200 rounded-xl '
                     'focus:outline-none focus:ring-2 focus:ring-orange-500 '
                     'transition-all duration-200 placeholder-gray-400',
            'placeholder': 'Enter your registered email'
        })
        
      
class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        common_classes = (
            'w-full px-4 py-3 border border-orange-200 rounded-xl '
            'focus:outline-none focus:ring-2 focus:ring-orange-500 '
            'transition-all duration-200 placeholder-gray-400'
        )

        self.fields['new_password1'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Enter new password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Confirm new password'
        })
