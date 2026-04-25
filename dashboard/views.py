from django.shortcuts import render
from django.db.models import Count, Avg, Q
from organizations.models import Organization
from officials.models import Official, Asset, Relative, Tender


def home(request):
    """Asosiy Dashboard"""
    
    total_orgs = Organization.objects.count()
    green_count = Organization.objects.filter(category='green').count()
    yellow_count = Organization.objects.filter(category='yellow').count()
    red_count = Organization.objects.filter(category='red').count()
    
    total_officials = Official.objects.count()
    critical_risk = Official.objects.filter(risk_level='critical').count()
    high_risk = Official.objects.filter(risk_level='high').count()
    medium_risk = Official.objects.filter(risk_level='medium').count()
    low_risk = Official.objects.filter(risk_level='low').count()
    
    top_risky_officials = Official.objects.filter(
        risk_level__in=['critical', 'high']
    ).order_by('-risk_score')[:10]
    
    worst_orgs = Organization.objects.filter(category='red').order_by('openness_score')[:10]
    best_orgs = Organization.objects.filter(category='green').order_by('-openness_score')[:5]
    
    # Suspicious tenders
    suspicious_tenders_count = Tender.objects.filter(is_suspicious=True).count()
    
    # Red flag assets
    luxury_assets_count = Asset.objects.filter(is_luxury=True).count()
    
    context = {
        'total_orgs': total_orgs,
        'green_count': green_count,
        'yellow_count': yellow_count,
        'red_count': red_count,
        'green_percent': round(green_count / total_orgs * 100, 1) if total_orgs else 0,
        'yellow_percent': round(yellow_count / total_orgs * 100, 1) if total_orgs else 0,
        'red_percent': round(red_count / total_orgs * 100, 1) if total_orgs else 0,
        
        'total_officials': total_officials,
        'critical_risk': critical_risk,
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk,
        
        'top_risky_officials': top_risky_officials,
        'worst_orgs': worst_orgs,
        'best_orgs': best_orgs,
        
        'suspicious_tenders_count': suspicious_tenders_count,
        'luxury_assets_count': luxury_assets_count,
    }
    
    return render(request, 'dashboard/home.html', context)


def about(request):
    """Loyiha haqida"""
    return render(request, 'dashboard/about.html')
