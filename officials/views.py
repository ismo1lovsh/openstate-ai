from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Sum
from .models import Official, Asset, Relative, Tender
from organizations.models import Organization


def official_list(request):
    """Barcha amaldorlar ro'yxati"""
    officials = Official.objects.all().select_related('organization')
    
    # Filter
    risk_level = request.GET.get('risk')
    if risk_level in ['low', 'medium', 'high', 'critical']:
        officials = officials.filter(risk_level=risk_level)
    
    org_id = request.GET.get('organization')
    if org_id:
        officials = officials.filter(organization_id=org_id)
    
    search = request.GET.get('search')
    if search:
        officials = officials.filter(
            Q(full_name__icontains=search) | 
            Q(position__icontains=search)
        )
    
    officials = officials.order_by('-risk_score')
    
    # Organizations uchun filter
    organizations = Organization.objects.all().order_by('rank')
    
    context = {
        'officials': officials,
        'organizations': organizations,
        'selected_risk': risk_level,
        'selected_org': int(org_id) if org_id else None,
        'search_query': search or '',
        'total_count': officials.count(),
    }
    return render(request, 'officials/list.html', context)


def official_detail(request, pk):
    """Amaldor batafsil — AI Risk Analysis"""
    official = get_object_or_404(Official, pk=pk)
    
    # Aktivlar
    assets = official.assets.all().order_by('-value')
    total_assets_value = assets.aggregate(total=Sum('value'))['total'] or 0
    luxury_assets = assets.filter(is_luxury=True)
    hidden_assets = assets.filter(is_declared=False)
    
    # Qarindoshlar
    relatives = official.relatives.all()
    relatives_with_tenders = relatives.filter(has_government_tenders=True)
    
    # Tenderlar (qarindoshlar orqali)
    related_tenders = Tender.objects.filter(
        linked_relative__official=official
    ).order_by('-awarded_date')
    
    total_tender_value = related_tenders.aggregate(total=Sum('value'))['total'] or 0
    
    # Income vs Assets ratio
    ratio = float(total_assets_value) / float(official.declared_income) if official.declared_income > 0 else 0
    
    # Risk breakdown uchun chart data
    risk_breakdown = {
        'labels': ['Daromad nomuvofiqligi', 'Hayot tarzi', 'Tarmoq riski', 'Boylik o\'sishi'],
        'data': [
            float(official.income_mismatch_score),
            float(official.lifestyle_score),
            float(official.network_score),
            float(official.wealth_growth_score),
        ]
    }
    
    context = {
        'official': official,
        'assets': assets,
        'total_assets_value': total_assets_value,
        'luxury_assets': luxury_assets,
        'hidden_assets': hidden_assets,
        'relatives': relatives,
        'relatives_with_tenders': relatives_with_tenders,
        'related_tenders': related_tenders,
        'total_tender_value': total_tender_value,
        'ratio': ratio,
        'risk_breakdown': risk_breakdown,
    }
    return render(request, 'officials/detail.html', context)


def recalculate_risk(request, pk):
    """AI Risk qayta hisoblash"""
    official = get_object_or_404(Official, pk=pk)
    official.calculate_risk()
    return render(request, 'officials/detail.html', {'official': official})
