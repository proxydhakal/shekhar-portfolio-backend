"""
Django management command to insert initial portfolio data.
Run: python manage.py insert_portfolio_data
Use --clear to delete existing data before inserting (optional).
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eportfolio_project.settings")
django.setup()

from django.core.management.base import BaseCommand
from apps.portfolio.models import (
    SiteConfiguration,
    Profile,
    Skill,
    Project,
    Experience,
    Education,
    Certification,
)


class Command(BaseCommand):
    help = "Insert initial portfolio data (site config, profile, skills, projects, experience, education, certifications)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing portfolio data (except SiteConfiguration) before inserting.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear_data()
        self._insert_site_config()
        self._insert_profile()
        self._insert_skills()
        self._insert_projects()
        self._insert_experiences()
        self._insert_education()
        self._insert_certifications()
        self.stdout.write(self.style.SUCCESS("Portfolio data inserted successfully."))

    def _clear_data(self):
        Certification.objects.all().delete()
        Education.objects.all().delete()
        Experience.objects.all().delete()
        Project.objects.all().delete()
        Skill.objects.all().delete()
        Profile.objects.all().delete()
        self.stdout.write("Cleared existing portfolio data.")

    def _insert_site_config(self):
        config, created = SiteConfiguration.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "Shekhar's Portfolio",
                "meta_title": "Shekhar Dhakal | Python Developer & RPA Specialist",
                "meta_description": "Portfolio of Shekhar Dhakal, a Backend Engineer specialized in high-performance Python ecosystems and Robotic Process Automation (RPA).",
                "meta_keywords": "backend, rpa, python, django, devops, fastapi, robocorp",
                "about_section_title": "01. Background",
                "skills_section_title": "Tech Stack",
                "experience_section_title": "cat career_logs.txt",
                "portfolio_section_title": "Production Projects",
                "contact_section_title": "05. Contact",
                "email": "shekhardhakal2015@gmail.com",
                "phone": "+977 9840177381",
                "address": "",
                "location": "Kathmandu, Nepal",
                "github_link": "https://github.com/proxydhakal",
                "linkedin_link": "https://www.linkedin.com/in/proxydhakal",
                "twitter_link": "",
                "facebook_link": "",
            },
        )
        if not created:
            config.meta_title = "Shekhar Dhakal | Python Developer & RPA Specialist"
            config.meta_description = "Portfolio of Shekhar Dhakal, a Backend Engineer specialized in high-performance Python ecosystems and Robotic Process Automation (RPA)."
            config.meta_keywords = "backend, rpa, python, django, devops, fastapi, robocorp"
            config.email = "shekhardhakal2015@gmail.com"
            config.phone = "+977 9840177381"
            config.location = "Kathmandu, Nepal"
            config.github_link = "https://github.com/proxydhakal"
            config.linkedin_link = "https://www.linkedin.com/in/proxydhakal"
            config.save()
        self.stdout.write("  SiteConfiguration: OK")

    def _insert_profile(self):
        profile, created = Profile.objects.get_or_create(
            name="Shekhar Dhakal",
            defaults={
                "name": "Shekhar Dhakal",
                "role": "Python Developer & RPA Specialist",
                "bio": "Result-driven developer with 3+ years experience building scalable applications and automating mission-critical banking processes.",
                "hero_title": "",
                "hero_subtitle": "python developer --rpa-specialist",
                "current_company": "MetaCloud Solution Pvt Ltd",
                "current_role_location": "Software Engineer (Lalitpur, Nepal)",
                "about_bullet_1": "I am a Python Developer specializing in RPA and DevOps Enthusiast.",
                "about_bullet_2": "Skilled in Django, FastAPI, Robocorp, and Docker, with a track record of building secure APIs and high-performance automation bots.",
                "about_bullet_3": "Passionate about clean code, system design, and continuous improvement in automated workflows.",
            },
        )
        if not created:
            profile.role = "Python Developer & RPA Specialist"
            profile.bio = "Result-driven developer with 3+ years experience building scalable applications and automating mission-critical banking processes."
            profile.hero_subtitle = "python developer --rpa-specialist"
            profile.current_company = "MetaCloud Solution Pvt Ltd"
            profile.current_role_location = "Software Engineer (Lalitpur, Nepal)"
            profile.about_bullet_1 = "I am a Python Developer specializing in RPA and DevOps Enthusiast."
            profile.about_bullet_2 = "Skilled in Django, FastAPI, Robocorp, and Docker, with a track record of building secure APIs and high-performance automation bots."
            profile.about_bullet_3 = "Passionate about clean code, system design, and continuous improvement in automated workflows."
            profile.save()
        self.stdout.write("  Profile: OK")

    def _insert_skills(self):
        skills_data = [
            {"name": "Python", "category": "Backend", "icon_class": "box", "order": 1},
            {"name": "Robocorp", "category": "RPA", "icon_class": "bot", "order": 2},
            {"name": "Django/DRF", "category": "Backend", "icon_class": "server", "order": 3},
            {"name": "Docker", "category": "DevOps", "icon_class": "container", "order": 4},
            {"name": "FastAPI", "category": "Backend", "icon_class": "zap", "order": 5},
            {"name": "PostgreSQL", "category": "Backend", "icon_class": "database", "order": 6},
        ]
        for s in skills_data:
            Skill.objects.update_or_create(name=s["name"], defaults=s)
        self.stdout.write("  Skills: %d items" % len(skills_data))

    def _insert_projects(self):
        projects_data = [
            {
                "title": "Bot Management System",
                "description": "Manage and schedule bots via a clean Django web interface, supporting cron expressions and real-time live logs. Reliable execution with Celery and built-in retry logic.",
                "tech_stack": "Celery, RabbitMQ",
                "live_link": "",
                "github_link": "",
                "order": 1,
                "icon_name": "layers",
                "accent_color": "primary",
            },
            {
                "title": "Sanima Auction Hub",
                "description": "Designed a scalable auction platform using Laravel and Docker containers. Successfully supported 1000+ concurrent users with minimal downtime.",
                "tech_stack": "Laravel, Nginx",
                "live_link": "https://auctionhub.sanimabank.com",
                "github_link": "",
                "order": 2,
                "icon_name": "trending-up",
                "accent_color": "secondary",
            },
            {
                "title": "Card Service Automation",
                "description": "Automated instant/credit card activations using Selenium, FTP, and Bash. Reduced manual effort and ensured strict compliance with security protocols.",
                "tech_stack": "Selenium, Bash",
                "live_link": "",
                "github_link": "",
                "order": 3,
                "icon_name": "credit-card",
                "accent_color": "accent",
            },
            {
                "title": "Network Automation Tool",
                "description": "Created a Django-based tool to auto-configure Cisco switches using Paramiko. Added real-time network monitoring with Prometheus and Grafana.",
                "tech_stack": "Paramiko, Grafana",
                "live_link": "",
                "github_link": "",
                "order": 4,
                "icon_name": "activity",
                "accent_color": "blue-400",
            },
        ]
        for p in projects_data:
            Project.objects.update_or_create(title=p["title"], defaults=p)
        self.stdout.write("  Projects: %d items" % len(projects_data))

    def _insert_experiences(self):
        experiences_data = [
            {
                "company": "MetaCloud Solution Pvt Ltd",
                "role": "Software Engineer",
                "duration": "April 2025 — PRESENT",
                "description": "• Deployed automation bots using Robocorp (Python, Playwright) with structured logging.\n• Built secure APIs with FastAPI and set up CI/CD pipelines for staging/production.\n• Designed dashboards with Prometheus/Grafana to track bot efficiency.",
                "order": 1,
                "is_primary": True,
            },
            {
                "company": "Sanima Bank Limited",
                "role": "RPA/Web Developer",
                "duration": "July 2024 — April 2025",
                "description": "• Developed backend services to orchestrate RPA workflows, resulting in 70% processing time reduction.\n• Integrated RESTful APIs with routers and firewalls for unified enterprise management.\n• Containerized microservices with Docker to improve scalability.",
                "order": 2,
                "is_primary": False,
            },
            {
                "company": "Jyoti Bikash Bank Limited",
                "role": "Web Developer",
                "duration": "August 2022 — June 2024",
                "description": "• Developed web applications using PHP (CodeIgniter) and Python (Django).\n• Designed ETL pipelines and database schemas to generate financial reports.\n• Automated workflows such as card activation, reducing manual banking effort.",
                "order": 3,
                "is_primary": False,
            },
            {
                "company": "Upwork Inc.",
                "role": "Python Developer",
                "duration": "Oct 2019 — Present",
                "description": "• Proficient in web scraping using BeautifulSoup and Selenium for dynamic data collection.\n• Conducted data mining using Pandas to support business decision making.",
                "order": 4,
                "is_primary": False,
            },
        ]
        for e in experiences_data:
            Experience.objects.update_or_create(
                company=e["company"], role=e["role"], defaults=e
            )
        self.stdout.write("  Experiences: %d items" % len(experiences_data))

    def _insert_education(self):
        edu, _ = Education.objects.update_or_create(
            institution="HERALD COLLEGE KATHMANDU",
            defaults={
                "duration": "2016 — 2019",
                "degree": "Bachelor in Computer Science",
                "description": "Gained a solid foundation on Information Technology with Artificial Intelligence and Machine Learning as core subjects.",
                "order": 1,
            },
        )
        self.stdout.write("  Education: 1 item")

    def _insert_certifications(self):
        certs_data = [
            {"title": "Python and Django", "issuer": "Broadway Infosys", "year": "2019", "order": 1},
            {"title": "Data Science & ML", "issuer": "Deerwalk Training", "year": "2023", "order": 2},
            {"title": "DevOps Certification", "issuer": "Broadway Infosys", "year": "2024", "order": 3},
        ]
        for c in certs_data:
            Certification.objects.update_or_create(
                title=c["title"], issuer=c["issuer"], defaults=c
            )
        self.stdout.write("  Certifications: %d items" % len(certs_data))
