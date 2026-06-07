import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from account.models import EmployerProfile, User
from jobapp.models import Applicant, BookmarkJob, Job


@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    Handle Dashboard View
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    admin_stats = {}
    recent_users = []

    if request.user.role == 'employer':
        jobs = Job.objects.filter(user=request.user.id, is_deleted=False)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id, is_deleted=False).count()
            total_applicants[job.id] = count

    elif request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id, is_deleted=False, job__is_deleted=False)
        appliedjobs = Applicant.objects.filter(user=request.user.id, is_deleted=False, job__is_deleted=False)

    elif request.user.role == 'admin':
        admin_stats = {
            'total_companies': User.objects.filter(role='employer').exclude(tipo_empresa='dependencia').count(),
            'total_dependencies': User.objects.filter(role='employer', tipo_empresa='dependencia').count(),
            'total_employees': User.objects.filter(role='employee').count(),
            'total_admins': User.objects.filter(role='admin').count(),
            'total_jobs': Job.objects.filter(is_deleted=False).count(),
            'total_applicants': Applicant.objects.filter(is_deleted=False, job__is_deleted=False).count(),
        }
        recent_users = User.objects.exclude(id=request.user.id).select_related('employer_profile').order_by('-date_joined')[:5]

    context = {
        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs': appliedjobs,
        'total_applicants': total_applicants,
        'admin_stats': admin_stats,
        'recent_users': recent_users,
    }
    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
def toggle_employer_privileges(request, user_id, action):
    if request.user.role != 'admin':
        raise PermissionDenied

    if action not in ('grant', 'revoke'):
        raise PermissionDenied

    employer = get_object_or_404(User, id=user_id, role='employer')
    profile, _ = EmployerProfile.objects.get_or_create(user=employer)

    if action == 'grant':
        profile.privilegios = True
        profile.save()
        Job.objects.filter(user=employer, is_deleted=False).update(priority=True)
        messages.success(request, f'Privilegios otorgados a {employer.email}.')
    else:
        profile.privilegios = False
        profile.save()
        Job.objects.filter(user=employer, is_deleted=False).update(priority=False)
        messages.success(request, f'Privilegios eliminados de {employer.email}.')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
def delete_user_view(request, user_id):
    if request.user.role != 'admin':
        raise PermissionDenied

    if request.user.id == user_id:
        messages.error(request, 'No puedes eliminar tu propia cuenta desde aquí.')
        return redirect('jobapp:dashboard')

    user_to_delete = get_object_or_404(User, id=user_id)
    email = user_to_delete.email
    user_to_delete.delete()
    messages.success(request, f'La cuenta de {email} ha sido eliminada.')
    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
def admin_report_view(request):
    if request.user.role != 'admin':
        raise PermissionDenied

    applicants = Applicant.objects.filter(
        is_deleted=False,
        job__is_deleted=False,
        user__role='employee',
    ).select_related('user', 'job').order_by('user__email', 'job__title')

    admin_stats = {
        'total_companies': User.objects.filter(role='employer').exclude(tipo_empresa='dependencia').count(),
        'total_dependencies': User.objects.filter(role='employer', tipo_empresa='dependencia').count(),
        'total_employees': User.objects.filter(role='employee').count(),
        'total_admins': User.objects.filter(role='admin').count(),
        'total_jobs': Job.objects.filter(is_deleted=False).count(),
        'total_applicants': Applicant.objects.filter(is_deleted=False, job__is_deleted=False).count(),
    }

    accepted_employee_ids = Applicant.objects.filter(
        is_deleted=False,
        job__is_deleted=False,
        user__role='employee',
        status='accepted',
    ).values_list('user_id', flat=True).distinct()

    employees_with_accepted = User.objects.filter(role='employee', id__in=accepted_employee_ids).count()
    employees_without_accepted = User.objects.filter(role='employee').exclude(id__in=accepted_employee_ids).count()

    buffer = io.BytesIO()
    pdf = Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = inch * 0.75
    y = height - margin

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(margin, y, 'Reporte de Administrador')
    y -= 24

    pdf.setFont('Helvetica', 10)
    pdf.drawString(margin, y, f'Generado por: {request.user.email}')
    y -= 14
    pdf.drawString(margin, y, 'Incluye estadísticas del dashboard y el detalle de aplicaciones de estudiantes.')
    y -= 20

    stats = [
        ('Total empresas', admin_stats['total_companies']),
        ('Total dependencias', admin_stats['total_dependencies']),
        ('Total candidatos', admin_stats['total_employees']),
        ('Total administradores', admin_stats['total_admins']),
        ('Total ofertas de trabajo', admin_stats['total_jobs']),
        ('Total postulaciones', admin_stats['total_applicants']),
        ('Estudiantes con al menos una pasantía aceptada', employees_with_accepted),
        ('Estudiantes sin ninguna pasantía aceptada', employees_without_accepted),
    ]

    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(margin, y, 'Estadísticas')
    y -= 18
    pdf.setFont('Helvetica', 10)
    for label, value in stats:
        if y < margin + 72:
            pdf.showPage()
            pdf.setFont('Helvetica', 10)
            y = height - margin
        pdf.drawString(margin, y, f'{label}: {value}')
        y -= 14

    if applicants.exists():
        # Group data by semester (1 or 2) for the current year
        current_year = timezone.now().year
        companies_by_sem = {1: {'Empresa': [], 'Dependencia': []}, 2: {'Empresa': [], 'Dependencia': []}}
        students_by_sem = {1: [], 2: []}

        employers = User.objects.filter(role='employer').order_by('date_joined')
        for e in employers:
            if not e.date_joined or e.date_joined.year != current_year:
                continue
            sem = 1 if e.date_joined.month <= 6 else 2
            name = e.get_full_name() or e.email
            kind = 'Dependencia' if getattr(e, 'tipo_empresa', None) == 'dependencia' else 'Empresa'
            companies_by_sem[sem][kind].append(name)

        students = User.objects.filter(role='employee').order_by('date_joined')
        for s in students:
            if not s.date_joined or s.date_joined.year != current_year:
                continue
            sem = 1 if s.date_joined.month <= 6 else 2
            students_by_sem[sem].append(s.get_full_name() or s.email)

        # Print semester lists
        if y < margin + 220:
            pdf.showPage()
            y = height - margin

        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(margin, y, 'Listados por Semestre (año {})'.format(current_year))
        y -= 16

        for sem in (1, 2):
            pdf.setFont('Helvetica-Bold', 10)
            pdf.drawString(margin, y, f'Semestre S{sem}')
            y -= 12

            pdf.setFont('Helvetica-Bold', 9)
            pdf.drawString(margin + 6, y, 'Empresas:')
            y -= 10
            if companies_by_sem[sem]['Empresa']:
                for name in companies_by_sem[sem]['Empresa']:
                    if y < margin + 36:
                        pdf.showPage(); pdf.setFont('Helvetica', 10); y = height - margin
                    pdf.drawString(margin + 12, y, name)
                    y -= 10
            else:
                pdf.drawString(margin + 12, y, '-')
                y -= 10

            pdf.setFont('Helvetica-Bold', 9)
            pdf.drawString(margin + 6, y, 'Dependencias:')
            y -= 10
            if companies_by_sem[sem]['Dependencia']:
                for name in companies_by_sem[sem]['Dependencia']:
                    if y < margin + 36:
                        pdf.showPage(); pdf.setFont('Helvetica', 10); y = height - margin
                    pdf.drawString(margin + 12, y, name)
                    y -= 10
            else:
                pdf.drawString(margin + 12, y, '-')
                y -= 10

            pdf.setFont('Helvetica-Bold', 9)
            pdf.drawString(margin + 6, y, 'Estudiantes:')
            y -= 10
            if students_by_sem[sem]:
                for name in students_by_sem[sem]:
                    if y < margin + 36:
                        pdf.showPage(); pdf.setFont('Helvetica', 10); y = height - margin
                    pdf.drawString(margin + 12, y, name)
                    y -= 10
            else:
                pdf.drawString(margin + 12, y, '-')
                y -= 10

            y -= 6

        # Simplified application detail lines including the company/dependency of the offer
        if y < margin + 90:
            pdf.showPage()
            y = height - margin

        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(margin, y, 'Detalle de aplicaciones')
        y -= 18
        pdf.setFont('Helvetica', 10)

        for applicant in applicants:
            status = 'Aceptado' if applicant.status == 'accepted' else 'Rechazado'
            student_name = applicant.user.get_full_name() or applicant.user.email
            job_title = applicant.job.title
            employer_user = applicant.job.user
            company_name = employer_user.get_full_name() or employer_user.email
            company_type = 'Dependencia' if getattr(employer_user, 'tipo_empresa', None) == 'dependencia' else 'Empresa'

            line = f'Estudiante {student_name} aplicó a oferta {job_title} de {company_name} ({company_type}) y fue {status}'
            wrapped = []
            while len(line) > 90:
                split_at = line.rfind(' ', 0, 90)
                if split_at == -1:
                    split_at = 90
                wrapped.append(line[:split_at])
                line = line[split_at+1:]
            wrapped.append(line)

            for part in wrapped:
                if y < margin + 36:
                    pdf.showPage()
                    pdf.setFont('Helvetica', 10)
                    y = height - margin
                pdf.drawString(margin, y, part)
                y -= 12
            y -= 4

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admin_dashboard_report.pdf"'
    return response
