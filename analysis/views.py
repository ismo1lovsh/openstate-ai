from django.shortcuts import render
from django.db.models import F, Sum, Count
from officials.models import Official, Asset, Tender


def analyzer(request):
    """Lifestyle vs Income Analyzer"""
    
    # Eng yuqori mismatch
    officials = Official.objects.all().order_by('-risk_score')[:20]
    
    # Chart data - scatter plot uchun
    scatter_data = []
    for o in Official.objects.all():
        assets_total = o.assets.aggregate(total=Sum('value'))['total'] or 0
        scatter_data.append({
            'name': o.full_name,
            'income': float(o.declared_income),
            'assets': float(assets_total),
            'risk': float(o.risk_score),
            'id': o.id,
        })
    
    context = {
        'officials': officials,
        'scatter_data': scatter_data,
    }
    return render(request, 'analysis/analyzer.html', context)


def wealth_growth(request):
    """Boylik o'sishi tahlili"""
    context = {}
    return render(request, 'analysis/wealth_growth.html', context)


def tender_anomaly(request):
    """Tender anomaliyalari"""
    suspicious_tenders = Tender.objects.filter(is_suspicious=True).order_by('-value')
    
    context = {
        'suspicious_tenders': suspicious_tenders,
        'total_suspicious_value': suspicious_tenders.aggregate(total=Sum('value'))['total'] or 0,
    }
    return render(request, 'analysis/tender_anomaly.html', context)
