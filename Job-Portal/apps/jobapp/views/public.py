from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import os
from django.views.generic import DetailView, ListView
from django.db.models import F
from jobapp.models import Category, Job
from jobapp.selectors import get_listed_jobs, search_jobs

User = get_user_model()


def home_view(request):
    published_jobs = Job.objects.filter(is_published=True, is_deleted=False).order_by('-updated_at')
    jobs = published_jobs.filter(is_closed=False)
    promoted_jobs = jobs.filter(priority=True)
    regular_jobs = jobs.filter(priority=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(regular_jobs, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_lists = []
        for job_list in page_obj.object_list.values():
            job_lists.append(job_list)
        data = {
            'job_lists': job_lists,
            'current_page_no': page_obj.number,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'no_of_page': paginator.num_pages,
            'prev_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        }
        return JsonResponse(data)

    stats = cache.get('home_stats')
    if not stats:
        stats = {
            'total_candidates': User.objects.filter(role='employee').count(),
            'total_companies': User.objects.filter(role='employer').count(),
            'total_jobs': get_listed_jobs().count(),
            'total_completed_jobs': published_jobs.filter(is_closed=True).count(),
        }
        cache.set('home_stats', stats, 60 * 15)

    context = {
        'total_candidates': stats['total_candidates'],
        'total_companies': stats['total_companies'],
        'total_jobs': stats['total_jobs'],
        'total_completed_jobs': stats['total_completed_jobs'],
        'page_obj': page_obj,
        'promoted_jobs': promoted_jobs,
        'categories': Category.objects.all(),
    }
    return render(request, 'jobapp/index.html', context)


def about_view(request):
    docs_dir = os.path.join(settings.BASE_DIR, 'static', 'docs')
    doc_files = []
    try:
        for fname in sorted(os.listdir(docs_dir)):
            fpath = os.path.join(docs_dir, fname)
            if os.path.isfile(fpath):
                doc_files.append(os.path.join('docs', fname).replace('\\', '/'))
    except Exception:
        doc_files = []

    context = {
        'doc_files': doc_files,
    }
    return render(request, 'about.html', context)


class JobListView(ListView):
    template_name = 'jobapp/job-list.html'
    context_object_name = 'page_obj'
    paginate_by = 1000

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        queryset = get_listed_jobs()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.filter(priority=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get('user_id')
        queryset = get_listed_jobs()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        context['promoted_jobs'] = queryset.filter(priority=True)
        return context


class SingleJobView(DetailView):
    template_name = 'jobapp/job-single.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        job_id = self.kwargs['id']
        Job.objects.filter(id=job_id).update(views_count=F('views_count') + 1)
        job = cache.get(job_id)
        if not job:
            job = get_object_or_404(Job, id=job_id)
            cache.set(job_id, job, 60 * 15)
        else:
            job.views_count += 1
            cache.set(job_id, job, 60 * 15)
        return job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_objects = self.object.tags.similar_objects()
        related_job_ids = [obj.id for obj in related_objects]
        related_job_list = Job.objects.filter(id__in=related_job_ids, is_deleted=False)
        paginator = Paginator(related_job_list, 5)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['total'] = len(related_job_list)
        return context


class SearchResultView(ListView):
    template_name = 'jobapp/result.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        return search_jobs(
            title_or_company=self.request.GET.get('job_title_or_company_name'),
            company_type=self.request.GET.get('tipo_empresa'),
            category_id=self.request.GET.get('category'),
        )



