from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .managers import generate_password
from .models import CustomUser, Technecian, Tech_doc
from django.contrib.auth.forms import UserChangeForm, UserCreationForm



from django.contrib import admin, messages

def generate_new_password(modeladmin, request, queryset):
    for user in queryset:
        # Generate a new password
        new_password = generate_password()
        user.set_password(new_password)
        user.raw_password = new_password  
        user.save() 
    
    # Display success message
    message = f"Successfully generated. new password  is {new_password}.\n"
    modeladmin.message_user(request, message, level=messages.SUCCESS)

generate_new_password.short_description = "Generate new password"



class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'
        USERNAME_FIELD = 'phone'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone')
       
        USERNAME_FIELD = 'phone'

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    ordering = ('phone',)
    USERNAME_FIELD = 'phone' 
    list_display = ('id','phone', 'first_name', 'last_name', 'is_staff','is_superuser','raw_password')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.add_action(generate_new_password)
admin.site.register(Technecian)
admin.site.register(Tech_doc)