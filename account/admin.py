from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models import Team, UserProfile, OTP, MobileOTP

admin.site.unregister(Group)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "manager_name")
    search_fields = ("name", "manager__username", "manager__email")
    ordering = ("name",)
    filter_horizontal = ("permissions", "members")

    @admin.display(description="Team Manager", ordering="manager")
    def manager_name(self, obj):
        return obj.manager.get_full_name()


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = (
    "username", "email", "first_name", "last_name", "phone_number", "team", "is_team_manager", "is_admin")
    search_fields = ("username", "email", "first_name", "last_name", "phone_number")
    list_filter = ( "team", "is_team_manager", "is_admin")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('team', 'is_team_manager', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_staff',
            'is_active', 'team', 'is_team_manager', 'is_admin')}
         ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("email", "code", "created")

@admin.register(MobileOTP)
class MobileOTPAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")