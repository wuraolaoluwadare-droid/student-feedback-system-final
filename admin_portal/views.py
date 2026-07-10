from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from student_app.models import Student
from lecturer_app.models import Lecturer
from course_app.models import Course
from feedback_app.models import Feedback, AnonymousComplaint

from django.shortcuts import redirect

def admin_home(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    return redirect("admin_login")

def admin_login(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(request, user)

            return redirect("admin_dashboard")

        messages.error(
            request,
            "Invalid administrator username or password."
        )

    return render(
        request,
        "admin_portal/login.html"
    )

from django.db.models import Count, Avg

def get_report_data():

    # Feedback by course
    course_feedback = (
        Feedback.objects
        .values("course__course_code")
        .annotate(total=Count("id"))
        .order_by("course__course_code")
    )

    feedback_labels = [
        item["course__course_code"]
        for item in course_feedback
    ]

    feedback_data = [
        item["total"]
        for item in course_feedback
    ]

    # Complaints
    complaint_summary = (
        AnonymousComplaint.objects
        .values("category")
        .annotate(total=Count("id"))
    )

    complaint_labels = [
        item["category"]
        for item in complaint_summary
    ]

    complaint_data = [
        item["total"]
        for item in complaint_summary
    ]

    averages = Feedback.objects.aggregate(
        avg_teaching=Avg("teaching_rating"),
        avg_communication=Avg("communication_rating"),
        avg_punctuality=Avg("punctuality_rating"),
        avg_material=Avg("course_material_rating"),
    )

    return {
        "feedback_labels": feedback_labels,
        "feedback_data": feedback_data,
        "complaint_labels": complaint_labels,
        "complaint_data": complaint_data,
        "avg_teaching": round(averages["avg_teaching"] or 0, 1),
        "avg_communication": round(averages["avg_communication"] or 0, 1),
        "avg_punctuality": round(averages["avg_punctuality"] or 0, 1),
        "avg_material": round(averages["avg_material"] or 0, 1),
    }
@login_required(login_url="admin_login")
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("login")

    # Dashboard counts
    student_count = Student.objects.count()
    lecturer_count = Lecturer.objects.count()
    course_count = Course.objects.count()
    feedback_count = Feedback.objects.count()
    complaint_count = AnonymousComplaint.objects.count()

    # Feedback count by course
    course_feedback = (
        Feedback.objects
        .values("course__course_code")
        .annotate(total=Count("id"))
        .order_by("course__course_code")
    )

    feedback_labels = [
        item["course__course_code"]
        for item in course_feedback
    ]

    feedback_data = [
        item["total"]
        for item in course_feedback
    ]

    # Complaint count by category
    complaint_summary = (
        AnonymousComplaint.objects
        .values("category")
        .annotate(total=Count("id"))
    )

    complaint_labels = [
        item["category"]
        for item in complaint_summary
    ]

    complaint_data = [
        item["total"]
        for item in complaint_summary
    ]

        # Average Ratings
    averages = Feedback.objects.aggregate(
        avg_teaching=Avg("teaching_rating"),
        avg_communication=Avg("communication_rating"),
        avg_punctuality=Avg("punctuality_rating"),
        avg_material=Avg("course_material_rating"),
    )

    context = {
    "student_count": student_count,
    "lecturer_count": lecturer_count,
    "course_count": course_count,
    "feedback_count": feedback_count,
    "complaint_count": complaint_count,
    }

    context.update(get_report_data())

    return render(
        request,
        "admin_portal/dashboard.html",
        context
    )

@login_required(login_url="admin_login")
def manage_students(request):

    if not request.user.is_staff:
        return redirect("login")

    search = request.GET.get("search", "")

    students = Student.objects.all().order_by("matric_no")

    if search:

        students = students.filter(
            full_name__icontains=search
        ) | Student.objects.filter(
            matric_no__icontains=search
        )

    return render(
        request,
        "admin_portal/students.html",
        {
            "students": students,
            "search": search
        }
    )
@login_required(login_url="admin_login")
def student_details(request, student_id):

    if not request.user.is_staff:
        return redirect("login")

    student = Student.objects.get(id=student_id)

    feedback_count = Feedback.objects.filter(
        student=student
    ).count()

    context = {

        "student": student,

        "feedback_count": feedback_count,

    }

    return render(
        request,
        "admin_portal/student_details.html",
        context
    )

@login_required(login_url="admin_login")
def manage_lecturers(request):

    if not request.user.is_staff:
        return redirect("login")

    search = request.GET.get("search", "")

    lecturers = Lecturer.objects.all().order_by("lecturer_id")

    if search:

        lecturers = lecturers.filter(
            full_name__icontains=search
        ) | Lecturer.objects.filter(
            lecturer_id__icontains=search
        )

    return render(
        request,
        "admin_portal/lecturers.html",
        {
            "lecturers": lecturers,
            "search": search
        }
    )

@login_required(login_url="admin_login")
def manage_courses(request):

    if not request.user.is_staff:
        return redirect("login")

    search = request.GET.get("search", "")

    courses = Course.objects.select_related("lecturer").all().order_by("course_code")

    if search:

        courses = courses.filter(
            course_code__icontains=search
        ) | Course.objects.filter(
            course_title__icontains=search
        )

    return render(
        request,
        "admin_portal/courses.html",
        {
            "courses": courses,
            "search": search
        }
    )
@login_required(login_url="admin_login")
def manage_feedback(request):

    if not request.user.is_staff:
        return redirect("login")

    search = request.GET.get("search", "")

    feedback_list = Feedback.objects.select_related(
        "student",
        "course",
        "course__lecturer"
    ).order_by("-submitted_at")

    if search:
        feedback_list = feedback_list.filter(
            student__full_name__icontains=search
        )

    return render(
        request,
        "admin_portal/feedback.html",
        {
            "feedback_list": feedback_list,
            "search": search,
        }
    )
@login_required(login_url="admin_login")
def manage_complaints(request):

    if not request.user.is_staff:
        return redirect("login")

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    complaints = AnonymousComplaint.objects.all().order_by("-submitted_at")

    if search:
        complaints = complaints.filter(
            message__icontains=search
        )

    if category:
        complaints = complaints.filter(category=category)

    context = {
        "complaints": complaints,
        "search": search,
        "category": category,
        "categories": AnonymousComplaint.CATEGORY_CHOICES,
    }

    return render(
        request,
        "admin_portal/complaints.html",
        context
    )

@login_required(login_url="admin_login")
def lecturer_performance(request):

    lecturers = Lecturer.objects.all()

    performance = []

    for lecturer in lecturers:

        feedbacks = Feedback.objects.filter(
            course__lecturer=lecturer
        )

        total = feedbacks.count()

        averages = feedbacks.aggregate(
            teaching=Avg("teaching_rating"),
            communication=Avg("communication_rating"),
            punctuality=Avg("punctuality_rating"),
            material=Avg("course_material_rating"),
        )

        overall = (
            (averages["teaching"] or 0) +
            (averages["communication"] or 0) +
            (averages["punctuality"] or 0) +
            (averages["material"] or 0)
        ) / 4

        performance.append({
            "lecturer": lecturer,
            "feedbacks": total,
            "teaching": round(averages["teaching"] or 0, 1),
            "communication": round(averages["communication"] or 0, 1),
            "punctuality": round(averages["punctuality"] or 0, 1),
            "material": round(averages["material"] or 0, 1),
            "overall": round(overall, 1),
        })

    performance = sorted(
        performance,
        key=lambda x: x["overall"],
        reverse=True
    )

    return render(
        request,
        "admin_portal/lecturer_performance.html",
        {
            "performance": performance
        }
    )

@login_required(login_url="admin_login")
def reports(request):

    if not request.user.is_staff:
        return redirect("login")

    context = get_report_data()

    return render(
        request,
        "admin_portal/reports.html",
        context
    )