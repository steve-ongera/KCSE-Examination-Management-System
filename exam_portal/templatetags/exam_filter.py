from django import template
import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='timedelta_time')
def timedelta_time(value):
    """Convert timedelta to time string"""
    if hasattr(value, 'total_seconds'):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    return value

@register.filter
def duration_slots(duration_minutes):
    """Calculate how many time slots an exam should span based on duration"""
    # Assuming each time slot is 30 minutes
    slot_minutes = 30
    slots = max(1, int(duration_minutes / slot_minutes))
    return slots

# We're not using this anymore, relying on duration_slots instead

@register.filter
def time_slot_has_active_exam(day_sessions, time_slot):
    """
    Check if a time slot has an active exam (either starting or ongoing)
    but the exam did not start at this exact time slot
    """
    for slot, session in day_sessions.items():
        if not session:
            continue
            
        # Check if this time_slot is after the start but before the end
        # And it's not the starting slot itself
        if (hasattr(session, 'start_time') and 
            hasattr(session, 'end_time') and 
            session.start_time < time_slot and
            time_slot < session.end_time):
            return True
    return False

@register.filter
def time_slot_has_active_exam(day_sessions, time_slot):
    """Check if a time slot has an active exam (either starting or ongoing)"""
    for session in day_sessions:
        if (hasattr(session, 'start_time') and 
            hasattr(session, 'end_time') and 
            session.start_time <= time_slot < session.end_time):
            return True
    return False