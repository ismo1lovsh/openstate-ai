from django.contrib import admin
from django.utils.html import format_html
from .models import Official, Asset, Relative, Tender


class AssetInline(admin.TabularInline):
    model = Asset
    extra = 0
    fields = ['asset_type', 'name', 'value', 'is_declared', 'is_luxury', 'owner_name']


class RelativeInline(admin.TabularInline):
    model = Relative
    extra = 0
    fields = ['full_name', 'relation_type', 'has_business', 'has_government_tenders', 'total_tender_value']


@admin.register(Official)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'organization', 'risk_badge', 'risk_score']
    list_filter = ['risk_level', 'organization', 'position_level']
    search_fields = ['full_name', 'position']
    inlines = [AssetInline, RelativeInline]
    
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('full_name', 'photo', 'birth_date')
        }),
        ('Lavozim', {
            'fields': ('organization', 'position', 'position_level', 'appointed_date')
        }),
        ('Daromad', {
            'fields': ('monthly_salary', 'declared_income', 'declared_assets')
        }),
        ('AI Risk Analysis', {
            'fields': ('risk_score', 'risk_level', 'income_mismatch_score', 
                      'lifestyle_score', 'network_score', 'wealth_growth_score',
                      'risk_explanation', 'red_flags')
        }),
    )
    
    actions = ['calculate_risk_action']
    
    def risk_badge(self, obj):
        colors = {
            'low': '#22c55e',
            'medium': '#eab308',
            'high': '#f97316',
            'critical': '#ef4444'
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:4px; font-weight:bold;">{}</span>',
            colors.get(obj.risk_level, '#6b7280'),
            obj.get_risk_level_display()
        )
    risk_badge.short_description = 'Risk'
    
    def calculate_risk_action(self, request, queryset):
        for official in queryset:
            official.calculate_risk()
        self.message_user(request, f"{queryset.count()} ta amaldor uchun risk hisoblandi.")
    calculate_risk_action.short_description = "AI Risk qayta hisoblash"


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_type', 'value', 'official', 'is_declared', 'is_luxury']
    list_filter = ['asset_type', 'is_declared', 'is_luxury']
    search_fields = ['name', 'official__full_name']


@admin.register(Relative)
class RelativeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'relation_type', 'official', 'has_business', 'has_government_tenders', 'total_tender_value']
    list_filter = ['relation_type', 'has_business', 'has_government_tenders']
    search_fields = ['full_name']


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'value', 'organization', 'is_suspicious', 'awarded_date']
    list_filter = ['is_suspicious', 'organization']
    search_fields = ['title', 'company_name']
    date_hierarchy = 'awarded_date'
