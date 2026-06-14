from django.shortcuts import get_object_or_404
from jobapp.models import Job, Applicant, BookmarkJob
from account.models import User


def toggle_job_status(user_id: int, job_id: int) -> bool:
    job = get_object_or_404(Job, id=job_id, user=user_id)
    job.is_closed = True
    job.save()
    return True
