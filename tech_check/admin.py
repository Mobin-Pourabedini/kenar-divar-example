from django.contrib import admin

from tech_check.models import Report, Technician, Post, User
from tech_check.utils import apply_report_in_divar


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    actions = ['apply_in_divar']
    list_display = ('post', 'technician_name', 'battery_health', 'screen_health', 'camera_health', 'body_health', 'performance_health')

    @admin.display(description='technician name')
    def technician_name(self, obj):
        return obj.technician.name

    def apply_in_divar(self, request, queryset):
        for report in queryset:
            r: Report = report
            response = apply_report_in_divar(r)
            if response.status_code != 200:
                self.message_user(request, f"Error in applying report in divar for report {r.id}")
                return
        self.message_user(request, "Reports applied in divar successfully")


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name')
    list_filter = ('phone', 'name')
    search_fields = ('phone', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('token', 'access_token', 'user_phone')

    @admin.display(description='User Phone')
    def user_phone(self, obj):
        if obj.user is None:
            return 'None'
        return obj.user.phone


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('phone', 'access_token')
