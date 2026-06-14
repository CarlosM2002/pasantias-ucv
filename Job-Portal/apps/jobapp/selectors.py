from django.db.models import QuerySet
from jobapp.models import Job


def get_listed_jobs() -> QuerySet[Job]:
    return Job.objects.select_related('category', 'user').filter(
        is_deleted=False,
        is_closed=False,
    ).order_by('-updated_at')


def search_jobs(title_or_company: str | None = None, company_type: str | None = None, category_id: str | None = None) -> QuerySet[Job]:
    job_list = Job.objects.select_related('category', 'user').filter(is_deleted=False).order_by('-updated_at')

    if title_or_company:
        job_list = job_list.filter(title__icontains=title_or_company) | job_list.filter(company_name__icontains=title_or_company)

    if company_type:
        job_list = job_list.filter(user__tipo_empresa=company_type)

    if category_id:
        job_list = job_list.filter(category_id=category_id)

    return job_list
