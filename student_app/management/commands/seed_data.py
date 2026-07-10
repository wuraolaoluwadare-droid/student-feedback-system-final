from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from student_app.models import Student
from lecturer_app.models import Lecturer
from course_app.models import Course


class Command(BaseCommand):
    help = "Seed demo data (Students, Lecturers and Courses)"

    def handle(self, *args, **kwargs):

        # ===========================
        # STUDENTS
        # ===========================

        students = [

            ("22/PTS/SCI01/003", "Adogbajale Teniola"),
            ("24/PTS/SCI01/064", "Ogoji Oluwasanmi Emmanuel"),
            ("23/PTS/SCI01/042", "Olaniyi Nelson Ademola"),
            ("22/PTS/SCI01/002", "Adebayo Jesupemi Godwin"),
            ("22/PTS/SCI01/005", "Daramola Lawrence T"),
            ("24/PTS/SCI01/065", "Onigba Basheerat"),
            ("23/PTS/SCI01/039", "Adesola Marvellous Oluwatobi"),
            ("24/PTS/SCI01/066", "Onikotun Joel Olawale"),
            ("22/PTS/SCI01/009", "Ibukun Victor Toluwanimi"),
            ("22/PTS/SCI01/063", "Alufa Racheal Abiodun"),
            ("24/PTS/SCI01/062", "Afolayan Fidelis Oluwatosin"),
            ("22/PTS/SCI01/007", "Famuyibo Ayomide Faith"),
            ("22/PTS/SCI01/001", "Adebayo Ayomide Stephen"),
            ("22/PTS/SCI01/010", "Nwankwo Victor"),
            ("23/PTS/SCI01/043", "Oluwadare Oluwanifemi Wuraola"),
            ("22/PTS/SCI01/006", "Falade Akintomide Alexander"),
            ("23/PTS/SCI01/040", "Adeyemi Bosede Martha"),
            ("24/PTS/SCI01/061", "Abioye Babatunde John"),
            ("22/PTS/SCI01/011", "Ogunlade Bisola Blessing"),
            ("22/PTS/SCI01/004", "Agbelekale Toheeb Oriyomi"),
            ("22/PTS/SCI01/012", "Ogunlade Daniel Foluso"),
            ("22/PTS/SCI01/013", "Ogunlade John Bayode"),
            ("22/PTS/SCI01/008", "Gbadamosi Favour Mayowa"),
            ("22/PTS/SCI01/014", "Olabiyi Ayomikun"),
            ("23/PTS/SCI01/041", "Frank Enobong Samuel"),
            ("22/PTS/SCI01/016", "Oluwasola George Ayobami"),
            ("22/PTS/SCI01/017", "Oso Demilade Goodness"),
            ("22/PTS/SCI01/018", "Sani Mukhtar Adam"),

        ]

        for matric_no, full_name in students:

            user, created = User.objects.get_or_create(
                username=matric_no
            )

            user.set_password("student123")
            user.is_staff = False
            user.save()

            Student.objects.update_or_create(
                matric_no=matric_no,
                defaults={
                    "user": user,
                    "full_name": full_name,
                    "department": "Computer Science",
                    "level": "400",
                },
            )

        self.stdout.write(
            self.style.SUCCESS("✓ Students created successfully.")
        )

        # ===========================
        # LECTURERS
        # ===========================

        lecturers = [

            ("LEC001", "Dr. Awoyemi"),
            ("LEC002", "Dr. Tope-Oke"),
            ("LEC003", "Dr. James Akathin"),

        ]

        lecturer_objects = {}

        for lecturer_id, full_name in lecturers:

            lecturer, created = Lecturer.objects.update_or_create(

                lecturer_id=lecturer_id,

                defaults={
                    "full_name": full_name,
                    "department": "Computer Science",
                }

            )

            lecturer_objects[lecturer_id] = lecturer

        self.stdout.write(
            self.style.SUCCESS("✓ Lecturers created successfully.")
        )

        # ===========================
        # COURSES
        # ===========================

        courses = [

            (
                "CSC411",
                "Human Computer Interaction",
                "LEC001"
            ),

            (
                "CSC413",
                "Modelling and Simulation",
                "LEC002"
            ),

            (
                "CSC415",
                "Distributed Computing",
                "LEC003"
            ),

            (
                "CSC417",
                "Electronic Commerce Technology",
                "LEC002"
            ),

        ]

        for code, title, lecturer_id in courses:

            Course.objects.update_or_create(

                course_code=code,

                defaults={
                    "course_title": title,
                    "lecturer": lecturer_objects[lecturer_id],
                }

            )

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Courses created successfully."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "===================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "DATABASE SEEDED SUCCESSFULLY!"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "===================================="
            )
        )