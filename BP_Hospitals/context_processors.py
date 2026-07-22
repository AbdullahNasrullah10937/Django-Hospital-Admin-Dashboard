from itertools import chain
from hospitals.models import Hospital
from directors.models import HospitalDirector
from wards.models import Ward


def notifications_processor(request):
    """
    Context processor that supplies recent system activities to all templates
    for rendering in the Notifications dropdown menu.
    """
    if not request.user.is_authenticated:
        return {'notifications': [], 'unread_notifications_count': 0}

    # Fetch recent records from each entity
    hospitals = Hospital.objects.all().order_by('-updated_at')[:5]
    directors = HospitalDirector.objects.select_related('hospital').all().order_by('-updated_at')[:5]
    wards = Ward.objects.select_related('hospital').all().order_by('-updated_at')[:5]

    activity_list = []

    for h in hospitals:
        activity_list.append({
            'title': f"Hospital: {h.hospital_name}",
            'subtitle': f"Located in {h.location} • Founded {h.founded_year}",
            'timestamp': h.updated_at,
            'url': f"/hospitals/{h.pk}/",
            'icon': 'bi-hospital',
            'badge_class': 'bg-primary'
        })

    for d in directors:
        activity_list.append({
            'title': f"Director: {d.director_name}",
            'subtitle': f"{d.qualification} at {d.hospital.hospital_name}",
            'timestamp': d.updated_at,
            'url': f"/directors/{d.pk}/",
            'icon': 'bi-person-badge',
            'badge_class': 'bg-info text-dark'
        })

    for w in wards:
        activity_list.append({
            'title': f"Ward: {w.ward_name}",
            'subtitle': f"{w.capacity} Beds at {w.hospital.hospital_name}",
            'timestamp': w.updated_at,
            'url': f"/wards/{w.pk}/",
            'icon': 'bi-door-open',
            'badge_class': 'bg-success'
        })

    # Sort combined activity by timestamp descending and slice top 5
    notifications = sorted(activity_list, key=lambda x: x['timestamp'], reverse=True)[:5]

    return {
        'notifications': notifications,
        'unread_notifications_count': len(notifications)
    }
