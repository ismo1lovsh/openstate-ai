from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Organization


def organization_list(request):
    """Barcha tashkilotlar ro'yxati (Ochiqlik Indeksi)"""
    organizations = Organization.objects.all().order_by('rank')
    
    # Filter
    category = request.GET.get('category')
    if category in ['green', 'yellow', 'red']:
        organizations = organizations.filter(category=category)
    
    search = request.GET.get('search')
    if search:
        organizations = organizations.filter(name__icontains=search)
    
    # Kategoriyalar bo'yicha guruhlash
    green_orgs = Organization.objects.filter(category='green').order_by('rank')
    yellow_orgs = Organization.objects.filter(category='yellow').order_by('rank')
    red_orgs = Organization.objects.filter(category='red').order_by('rank')
    
    context = {
        'organizations': organizations,
        'green_orgs': green_orgs,
        'yellow_orgs': yellow_orgs,
        'red_orgs': red_orgs,
        'selected_category': category,
        'search_query': search or '',
    }
    return render(request, 'organizations/list.html', context)


def organization_detail(request, pk):
    """Tashkilot batafsil"""
    organization = get_object_or_404(Organization, pk=pk)
    officials = organization.officials.all().order_by('-risk_score')
    tenders = organization.tenders.all()[:20]
    
    context = {
        'organization': organization,
        'officials': officials,
        'tenders': tenders,
        'critical_count': officials.filter(risk_level='critical').count(),
        'high_count': officials.filter(risk_level='high').count(),
    }
    return render(request, 'organizations/detail.html', context)
