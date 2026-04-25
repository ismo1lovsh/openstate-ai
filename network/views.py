from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from officials.models import Official, Relative, Tender
import json


def network_view(request, official_id=None):
    """Network graph - hidden connections"""
    
    if official_id:
        official = get_object_or_404(Official, pk=official_id)
    else:
        # Eng xavfli amaldorni default qilib ko'rsatamiz
        official = Official.objects.filter(risk_level='critical').first()
        if not official:
            official = Official.objects.order_by('-risk_score').first()
    
    officials = Official.objects.all().order_by('-risk_score')
    
    context = {
        'official': official,
        'officials': officials,
    }
    return render(request, 'network/graph.html', context)


def network_data(request, official_id):
    """JSON API for network graph"""
    official = get_object_or_404(Official, pk=official_id)
    
    nodes = []
    edges = []
    
    # Central node - the official
    nodes.append({
        'id': f'off_{official.id}',
        'label': official.full_name,
        'title': f"{official.position}\nRisk: {official.risk_score}",
        'group': 'official',
        'color': '#ef4444' if official.risk_level == 'critical' else '#f97316',
        'size': 40,
    })
    
    # Organization node
    nodes.append({
        'id': f'org_{official.organization.id}',
        'label': official.organization.name,
        'title': f'Ochiqlik: {official.organization.openness_score}',
        'group': 'organization',
        'color': '#3b82f6',
        'size': 30,
    })
    edges.append({
        'from': f'off_{official.id}',
        'to': f'org_{official.organization.id}',
        'label': 'ishlaydi',
        'color': '#6b7280',
    })
    
    # Relatives
    for relative in official.relatives.all():
        nodes.append({
            'id': f'rel_{relative.id}',
            'label': relative.full_name,
            'title': f"{relative.get_relation_type_display()}",
            'group': 'relative',
            'color': '#8b5cf6',
            'size': 25,
        })
        edges.append({
            'from': f'off_{official.id}',
            'to': f'rel_{relative.id}',
            'label': relative.get_relation_type_display(),
            'color': '#8b5cf6',
        })
        
        # Business connection
        if relative.has_business and relative.business_name:
            nodes.append({
                'id': f'biz_{relative.id}',
                'label': relative.business_name,
                'title': f'Biznes qiymati: {relative.business_value:,.0f}',
                'group': 'business',
                'color': '#eab308',
                'size': 20,
            })
            edges.append({
                'from': f'rel_{relative.id}',
                'to': f'biz_{relative.id}',
                'label': 'egasi',
                'color': '#eab308',
            })
        
        # Tenders
        for tender in relative.tenders.all()[:5]:
            nodes.append({
                'id': f'tnd_{tender.id}',
                'label': tender.title[:40],
                'title': f'{tender.value:,.0f} so\'m',
                'group': 'tender',
                'color': '#ef4444' if tender.is_suspicious else '#22c55e',
                'size': 18,
            })
            # Tender -> Organization
            edges.append({
                'from': f'org_{tender.organization.id}' if tender.organization else f'off_{official.id}',
                'to': f'tnd_{tender.id}',
                'label': 'tender',
                'color': '#ef4444' if tender.is_suspicious else '#6b7280',
                'dashes': True,
            })
            # Tender -> Relative's business
            if relative.business_name:
                edges.append({
                    'from': f'biz_{relative.id}',
                    'to': f'tnd_{tender.id}',
                    'label': 'yutgan',
                    'color': '#ef4444' if tender.is_suspicious else '#22c55e',
                })
    
    return JsonResponse({'nodes': nodes, 'edges': edges})
