from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default="Shekhar's Portfolio")
    meta_title = models.CharField(max_length=255, default="Shekhar Dhakal | Backend & RPA Architect")
    meta_description = models.TextField(
        default="Portfolio of Shekhar Dhakal, a Backend Engineer specialized in high-performance Python ecosystems and Robotic Process Automation (RPA)."
    )
    meta_keywords = models.CharField(max_length=500, default="backend, rpa, python, django, devops")

    # Section Titles
    about_section_title = models.CharField(max_length=100, default="01. Background")
    skills_section_title = models.CharField(max_length=100, default="02. Expertise")
    experience_section_title = models.CharField(max_length=100, default="03. Career Path")
    portfolio_section_title = models.CharField(max_length=100, default="04. Selected Projects")
    contact_section_title = models.CharField(max_length=100, default="05. Contact")

    # Contact Info
    email = models.EmailField(default="shekhardhakal2015@gmail.com")
    phone = models.CharField(max_length=50, default="+977 9840177381")
    address = models.CharField(max_length=255, blank=True)
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short location display e.g. Kathmandu, Nepal",
    )

    # Social Media
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)

    def __str__(self):
        return "Site Configuration"


class Profile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    current_company = models.CharField(max_length=200, blank=True, help_text="e.g. MetaCloud Solution Pvt Ltd")
    current_role_location = models.CharField(
        max_length=200, blank=True, help_text="e.g. Software Engineer (Lalitpur, Nepal)"
    )
    about_bullet_1 = models.TextField(blank=True)
    about_bullet_2 = models.TextField(blank=True)
    about_bullet_3 = models.TextField(blank=True)

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-subscribed_at"]


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("Frontend", "Frontend"),
        ("Backend", "Backend"),
        ("RPA", "RPA"),
        ("DevOps", "DevOps"),
        ("Other", "Other"),
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome class (e.g. fa-brands fa-python, fa-solid fa-robot). Leave blank to use default icon by skill name.",
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    tech_stack = models.CharField(max_length=200, help_text="Comma separated list or description")
    live_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    icon_name = models.CharField(
        max_length=50, blank=True, help_text="Lucide icon name, e.g. layers, trending-up"
    )
    accent_color = models.CharField(
        max_length=30, blank=True, help_text="e.g. primary, secondary, accent, blue-400"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(
        default=False, help_text="Use primary color for timeline dot"
    )

    def __str__(self):
        return f"{self.role} at {self.company}"

    class Meta:
        ordering = ["order"]


class Education(models.Model):
    duration = models.CharField(max_length=100)
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    year = models.CharField(max_length=20, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
