from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, View

from jobapp.forms import JobApplyForm, JobBookmarkForm
from jobapp.models import Applicant, BookmarkJob, Job
from jobapp.permission import EmployeeRequiredMixin



class ApplyJobView(EmployeeRequiredMixin, View):

    def post(self, request, id):
        user = request.user
        job = get_object_or_404(Job, id=id)
        form = JobApplyForm(request.POST)

        existing = Applicant.objects.filter(user=user, job=job).first()
        if existing:
            if not existing.is_deleted:
                messages.error(request, '¡Ya has solicitado este puesto!')
            else:
                existing.is_deleted = False
                existing.status = 'pending'
                existing.save()
                messages.success(request, '¡Has solicitado este puesto con éxito!')
        elif form.is_valid():
            Applicant.objects.create(user=user, job=job)
            messages.success(request, '¡Has solicitado este puesto con éxito!')

        return redirect(reverse('jobapp:single-job', kwargs={'id': id}))

    def get(self, request, id):
        return redirect(reverse('jobapp:single-job', kwargs={'id': id}))


class DeleteBookmarkView(EmployeeRequiredMixin, DeleteView):

    model = BookmarkJob
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('jobapp:dashboard')

    def get_queryset(self):
        return BookmarkJob.objects.filter(user=self.request.user, is_deleted=False)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, '¡El puesto guardado fue eliminado con éxito!')
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


class DeleteApplicantView(EmployeeRequiredMixin, DeleteView):

    model = Applicant
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('jobapp:dashboard')

    def get_queryset(self):
        return Applicant.objects.filter(user=self.request.user, is_deleted=False)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, '¡La solicitud se eliminó correctamente!')
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


class JobBookmarkView(EmployeeRequiredMixin, View):

    def post(self, request, id):
        user = request.user
        job = get_object_or_404(Job, id=id)
        form = JobBookmarkForm(request.POST)

        existing = BookmarkJob.objects.filter(user=user, job=job).first()
        if existing:
            if not existing.is_deleted:
                messages.error(request, '¡Ya has guardado este puesto!')
            else:
                existing.is_deleted = False
                existing.save()
                messages.success(request, '¡Has guardado este puesto con éxito!')
        elif form.is_valid():
            BookmarkJob.objects.create(user=user, job=job)
            messages.success(request, '¡Has guardado este puesto con éxito!')

        return redirect(reverse('jobapp:single-job', kwargs={'id': id}))

    def get(self, request, id):
        return redirect(reverse('jobapp:single-job', kwargs={'id': id}))
