from django.contrib import admin
from django.utils.html import format_html
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['rank', 'name', 'openness_score', 'category_badge', 'trend_icon', 'risk_score']
    list_filter = ['category', 'org_type', 'trend']
    search_fields = ['name', 'short_name']
    list_editable = ['openness_score']
    ordering = ['rank']
    
    def category_badge(self, obj):
        colors = {'green': '#22c55e', 'yellow': '#eab308', 'red': '#ef4444'}
        return format_html(
            '<span style="background:{}; color:white; padding:3px 8px; border-radius:4px;">{}</span>',
            colors.get(obj.category, '#6b7280'),
            obj.get_category_display()
        )
    category_badge.short_description = 'Kategoriya'
    
    def trend_icon(self, obj):
        icons = {'up': '📈', 'down': '📉', 'stable': '➡️'}
        return icons.get(obj.trend, '')
    trend_icon.short_description = 'Trend'
