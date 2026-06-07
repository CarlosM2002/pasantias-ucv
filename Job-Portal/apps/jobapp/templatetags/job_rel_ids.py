from django import template

from jobapp.models import BookmarkJob, Applicant

register = template.Library()


@register.simple_tag(name='get_bookmark_id')
def get_bookmark_id(job, user):
    try:
        bk = BookmarkJob.objects.filter(job=job, user=user, is_deleted=False).first()
        return bk.id if bk else ''
    except Exception:
        return ''


@register.simple_tag(name='get_application_id')
def get_application_id(job, user):
    try:
        app = Applicant.objects.filter(job=job, user=user, is_deleted=False).first()
        return app.id if app else ''
    except Exception:
        return ''
