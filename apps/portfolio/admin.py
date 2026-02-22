from django.contrib import admin
from .models import (
    Profile,
    Skill,
    Project,
    ContactMessage,
    Experience,
    SiteConfiguration,
    NewsletterSubscriber,
    Education,
    Certification,
)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ("is_active",)
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "General SEO",
            {"fields": ("site_name", "meta_title", "meta_description", "meta_keywords")},
        ),
        (
            "Section Titles",
            {
                "fields": (
                    "about_section_title",
                    "skills_section_title",
                    "experience_section_title",
                    "portfolio_section_title",
                    "contact_section_title",
                )
            },
        ),
        (
            "Contact Information",
            {"fields": ("email", "phone", "address", "location")},
        ),
        (
            "Social Media Links",
            {"fields": ("github_link", "linkedin_link", "twitter_link", "facebook_link")},
        ),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    list_editable = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "order")
    list_editable = ("order",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "duration", "order")
    list_editable = ("order",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "year", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "created_at")
    readonly_fields = ("created_at",)
