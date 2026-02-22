from django import template

register = template.Library()

# Default Font Awesome icons for common skill names (when icon_class is empty or not FA)
SKILL_FA_ICONS = {
    "Python": "fa-brands fa-python",
    "Django": "fa-solid fa-server",
    "Django/DRF": "fa-solid fa-server",
    "DRF": "fa-solid fa-server",
    "Robocorp": "fa-solid fa-robot",
    "Docker": "fa-brands fa-docker",
    "FastAPI": "fa-solid fa-bolt",
    "PostgreSQL": "fa-solid fa-database",
    "Selenium": "fa-solid fa-spider",
    "CI/CD": "fa-solid fa-arrows-rotate",
    "Celery": "fa-solid fa-list-check",
    "RabbitMQ": "fa-solid fa-rabbit",
    "Laravel": "fa-brands fa-laravel",
    "Nginx": "fa-solid fa-server",
    "Paramiko": "fa-solid fa-terminal",
    "Grafana": "fa-solid fa-chart-line",
    "Redis": "fa-solid fa-database",
    "Git": "fa-brands fa-git-alt",
    "GitHub": "fa-brands fa-github",
    "Linux": "fa-brands fa-linux",
    "AWS": "fa-brands fa-aws",
    "JavaScript": "fa-brands fa-js",
    "React": "fa-brands fa-react",
    "HTML": "fa-brands fa-html5",
    "CSS": "fa-brands fa-css3-alt",
    "PHP": "fa-brands fa-php",
    "MySQL": "fa-solid fa-database",
    "MongoDB": "fa-solid fa-database",
    "RPA": "fa-solid fa-robot",
    "DevOps": "fa-solid fa-gears",
    "Backend": "fa-solid fa-code",
    "Frontend": "fa-solid fa-palette",
}

DEFAULT_SKILL_ICON = "fa-solid fa-code"


@register.filter
def skill_fa_icon(skill):
    """Return Font Awesome icon class for a skill. Uses icon_class if it's a FA class, else mapping or default."""
    if skill.icon_class and "fa-" in skill.icon_class:
        return skill.icon_class
    return SKILL_FA_ICONS.get(skill.name, DEFAULT_SKILL_ICON)
