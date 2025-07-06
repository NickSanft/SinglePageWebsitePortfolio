from flask import Flask, render_template_string, send_from_directory
import os
import json
import datetime
import requests
import zipfile
import io

# --- UPDATED: Simplified Flask app setup, will add explicit routes ---
app = Flask(__name__, static_url_path='', static_folder='output')


# Load and process data from external JSON file
def load_data():
    # Create a dummy website_data.json if it doesn't exist for demonstration
    if not os.path.exists("website_data.json"):
        dummy_data = {
            "website_title": "My Awesome Developer Portfolio",
            "portfolio_name": "MyPortfolio",
            "hero_title": "Your Name",
            "hero_subtitle": "Software Developer | Python & JavaScript Enthusiast",
            "hero_image_url": "https://placehold.co/256x256/e0e0e0/333333?text=You",
            "about_me": "Hello! I'm a software developer with a passion for building clean and efficient solutions. I specialize in web development and enjoy working with Python, JavaScript, and modern front-end frameworks. My goal is to create impactful and user-friendly applications.",
            "theme_colors": {
                "light": {
                    "background": "#f9fafb",
                    "text_primary": "#111827",
                    "text_secondary": "#4b5563",
                    "card_background": "#ffffff",
                    "accent": "#3b82f6",
                    "accent_hover": "#2563eb",
                    "spotlight_color": "rgba(255, 255, 255, 0.2)"
                },
                "dark": {
                    "background": "#111827",
                    "text_primary": "#f9fafb",
                    "text_secondary": "#d1d5db",
                    "card_background": "#1f2937",
                    "accent": "#60a5fa",
                    "accent_hover": "#3b82f6",
                    "spotlight_color": "rgba(255, 255, 255, 0.1)"
                }
            },
            "projects": [
                {
                    "title": "Project Alpha",
                    "description": "A full-stack web application for managing tasks and collaborating with teams, built with a modern MERN stack.",
                    "url": "https://github.com/yourusername/project-alpha",
                    "icon": "fas fa-laptop-code",
                    "featured": True,
                    "image_url": "https://placehold.co/600x400/3b82f6/ffffff?text=Project+Alpha",
                    "tech_stack": ["React", "Node.js", "Express", "MongoDB"]
                },
                {
                    "title": "Project Beta",
                    "description": "Cross-platform mobile app for tracking personal fitness goals, with real-time data synchronization using Firebase.",
                    "url": "https://github.com/yourusername/project-beta",
                    "icon": "fas fa-mobile-alt",
                    "featured": False,
                    "image_url": "https://placehold.co/600x400/10b981/ffffff?text=Project+Beta",
                    "tech_stack": ["Flutter", "Firebase", "Dart"]
                },
                {
                    "title": "Project Gamma",
                    "description": "A data analysis and visualization dashboard for exploring sales trends, powered by Python.",
                    "url": "https://github.com/yourusername/project-gamma",
                    "icon": "fas fa-chart-line",
                    "featured": False,
                    "image_url": "https://placehold.co/600x400/f59e0b/ffffff?text=Project+Gamma",
                    "tech_stack": ["Python", "Pandas", "Matplotlib", "Flask"]
                }
            ],
            "experience": [
                {"role": "Software Engineer", "company": "Tech Solutions Inc.", "period": "Jan 2022 - Present",
                 "details": "Developed and maintained web services using Python and Django."},
                {"role": "Senior Software Engineer", "company": "Tech Solutions Inc.", "period": "Jan 2024 - Present",
                 "details": "Led a team in developing scalable microservices and mentored junior developers."},
                {"role": "Junior Developer", "company": "Innovate Co.", "period": "Jul 2020 - Dec 2021",
                 "details": "Assisted in front-end development with HTML, CSS, and JavaScript."},
                {"role": "Intern", "company": "Innovate Co.", "period": "May 2020 - Jun 2020",
                 "details": "Gained hands-on experience with version control and agile methodologies."}
            ],
            "skills": [
                {"name": "Python", "icon": "fab fa-python"},
                {"name": "JavaScript", "icon": "fab fa-js"},
                {"name": "React", "icon": "fab fa-react"},
                {"name": "Node.js", "icon": "fab fa-node-js"},
                {"name": "Tailwind CSS", "icon": "fab fa-css3-alt"},
                {"name": "Flask", "icon": "fas fa-flask"},
                {"name": "SQL", "icon": "fas fa-database"},
                {"name": "Git", "icon": "fab fa-git-alt"},
                {"name": "Cloud Computing", "icon": "fas fa-cloud"}
            ],
            "contact_info": {
                "github_url": "https://github.com/yourusername",
                "linkedin_url": "https://linkedin.com/in/yourusername",
                "bandcamp_url": "https://yourusername.bandcamp.com",
                "kofi_url": "https://ko-fi.com/yourusername"
            },
            "copyright_name": "Your Name",
            "copyright_start_year": 2024
        }
        with open("website_data.json", "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=4)

    with open("website_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Separate featured project from others
    projects = data.get("projects", [])
    data["featured_project"] = next((p for p in projects if p.get("featured")), None)
    data["other_projects"] = [p for p in projects if not p.get("featured")]

    # Group experience by company
    grouped_experience = []
    if "experience" in data:
        current_company = None
        sorted_experience = sorted(data["experience"], key=lambda x: x['period'], reverse=True)
        for job in sorted_experience:
            if job["company"] != current_company:
                grouped_experience.append({"company": job["company"], "roles": []})
                current_company = job["company"]
            grouped_experience[-1]["roles"].append(
                {"role": job["role"], "period": job["period"], "details": job["details"]})
    data["grouped_experience"] = grouped_experience

    # Generate dynamic copyright string
    start_year = data.get("copyright_start_year")
    current_year = datetime.datetime.now().year
    if start_year and start_year < current_year:
        data["copyright_string"] = f"{start_year} - {current_year}"
    else:
        data["copyright_string"] = str(current_year)

    return data


# === UPDATED: Template refactored with Jinja2 Macros for readability and maintainability ===
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ website_title }}</title>
    <script src="/static/tailwindcss.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
    <link rel="stylesheet" href="/static/fontawesome-free-6.4.0-web/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        heading: ['Poppins', 'sans-serif'],
                    },
                    keyframes: {
                        flash: {
                          '0%, 100%': { backgroundColor: 'transparent' },
                          '50%': { backgroundColor: 'rgba(59, 130, 246, 0.2)' },
                        }
                    },
                    animation: {
                        flash: 'flash 1s ease-in-out',
                    }
                },
            },
        }

        let defaultSectionOrder = [];

        function toggleTheme() {
            document.documentElement.classList.toggle('dark');
            localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        }

        function applyInteractiveCardEffect() {
            document.addEventListener('mousemove', e => {
                const cards = document.querySelectorAll('.interactive-card');
                for (const card of cards) {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouseX', `${x}px`);
                    card.style.setProperty('--mouseY', `${y}px`);
                }
            });
        }

        function updateScrollProgress() {
            const progressBar = document.getElementById('scroll-progress-bar');
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = document.documentElement.scrollTop;
            const percentage = (scrolled / scrollHeight) * 100;
            progressBar.style.width = percentage + '%';
        }

        function toggleBackToTopButton() {
            const backToTopBtn = document.getElementById('back-to-top-btn');
            if (window.scrollY > 300) {
                backToTopBtn.classList.remove('opacity-0', 'invisible');
                backToTopBtn.classList.add('opacity-100', 'visible');
            } else {
                backToTopBtn.classList.remove('opacity-100', 'visible');
                backToTopBtn.classList.add('opacity-0', 'invisible');
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            applyInteractiveCardEffect();
            window.addEventListener('scroll', updateScrollProgress);
            window.addEventListener('scroll', toggleBackToTopButton);

            const observerOptions = { root: null, rootMargin: '0px', threshold: 0.1 };
            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        const staggerItems = entry.target.querySelectorAll('.stagger-item');
                        staggerItems.forEach((item, index) => {
                            setTimeout(() => { item.classList.add('is-visible'); }, index * 100);
                        });
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            document.querySelectorAll('.fade-in-section').forEach(element => { observer.observe(element); });
            document.getElementById('back-to-top-btn').addEventListener('click', () => { window.scrollTo({ top: 0, behavior: 'smooth' }); });

            initSectionReordering();
        });
    </script>
    <style>
        :root {
            --color-background: {{ theme_colors.light.background }};
            --color-text-primary: {{ theme_colors.light.text_primary }};
            --color-text-secondary: {{ theme_colors.light.text_secondary }};
            --color-card-background: {{ theme_colors.light.card_background }};
            --color-accent: {{ theme_colors.light.accent }};
            --color-accent-hover: {{ theme_colors.light.accent_hover }};
            --color-spotlight: {{ theme_colors.light.spotlight_color }};
        }
        .dark {
            --color-background: {{ theme_colors.dark.background }};
            --color-text-primary: {{ theme_colors.dark.text_primary }};
            --color-text-secondary: {{ theme_colors.dark.text_secondary }};
            --color-card-background: {{ theme_colors.dark.card_background }};
            --color-accent: {{ theme_colors.dark.accent }};
            --color-accent-hover: {{ theme_colors.dark.accent_hover }};
            --color-spotlight: {{ theme_colors.dark.spotlight_color }};
        }
        html { scroll-behavior: smooth; }
        body { 
            font-family: 'Inter', sans-serif; 
            background-color: var(--color-background);
            color: var(--color-text-primary);
            transition: background-color 0.3s, color 0.3s; 
        }
        #scroll-progress-bar { position: fixed; top: 0; left: 0; height: 4px; background-color: var(--color-accent); width: 0%; z-index: 50; transition: width 0.1s linear; }
        #back-to-top-btn { position: fixed; bottom: 1.5rem; right: 1.5rem; background-color: var(--color-accent); color: white; padding: 0.75rem; border-radius: 9999px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out, background-color 0.3s; opacity: 0; visibility: hidden; z-index: 40; cursor: pointer; }
        #back-to-top-btn:hover { background-color: var(--color-accent-hover); }
        #back-to-top-btn:focus-visible { outline: none; box-shadow: 0 0 0 3px var(--color-accent); }
        .interactive-card { position: relative; overflow: hidden; background-color: var(--color-card-background); }
        .interactive-card::before { content: ""; position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: inherit; background: radial-gradient(400px circle at var(--mouseX) var(--mouseY), var(--color-spotlight), transparent 40%); opacity: 0; transition: opacity 0.3s ease-in-out; z-index: 1; }
        .interactive-card:hover::before { opacity: 1; }
        .interactive-card > * { position: relative; z-index: 2; }
        .fade-in-section { opacity: 0; transition: opacity 0.5s ease-out; }
        .fade-in-section.is-visible { opacity: 1; }
        .stagger-item { opacity: 0; transform: translateY(20px); transition: opacity 0.5s cubic-bezier(0.5, 0, 0, 1.5), transform 0.5s cubic-bezier(0.5, 0, 0, 1.5); }
        .stagger-item.is-visible { opacity: 1; transform: translateY(0); }
        @media (prefers-reduced-motion: reduce) { .fade-in-section, .stagger-item, #back-to-top-btn { transition: none !important; transform: none !important; opacity: 1 !important; } }

        #fontFamilySelect {
          color: black;
          background-color: white;
        }

        .dark #fontFamilySelect {
          color: white;
          background-color: #2d2d2d;
        }
        .sortable-ghost {
            opacity: 0.4;
            background-color: var(--color-accent);
        }
        .sortable-chosen {
            cursor: grabbing;
        }
        .grabbing {
            cursor: grabbing;
            outline: 2px solid var(--color-accent);
            outline-offset: 2px;
        }
        .nav-link {
            position: relative;
            text-decoration: none;
            padding-bottom: 4px;
        }
        .nav-link::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--color-accent);
            transform: scaleX(0);
            transform-origin: center;
            transition: transform 0.3s ease-out;
        }
        .nav-link:hover::after {
            transform: scaleX(1);
        }
    </style>
</head>
<body class="bg-[var(--color-background)] text-[var(--color-text-primary)] font-sans">

{# === MACRO DEFINITIONS === #}

{% macro nav_link(href, text) %}
    <a href="{{ href }}" class="nav-link hover:text-[var(--color-accent)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2 rounded">{{ text }}</a>
{% endmacro %}

{% macro skill_item(skill) %}
    <div class="stagger-item flex flex-col items-center justify-center p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800 text-[var(--color-text-primary)] transform hover:scale-105 transition-transform duration-300">
        <i class="{{ skill.icon }} text-4xl mb-2 text-[var(--color-accent)]"></i>
        <span>{{ skill.name }}</span>
    </div>
{% endmacro %}

{% macro project_card(project, is_featured=false) %}
    {% if is_featured %}
        <div class="mb-16 stagger-item">
            <div class="interactive-card rounded-lg shadow-xl overflow-hidden md:flex transform hover:-translate-y-2 transition-transform duration-300">
                <div class="md:w-1/2 bg-gray-200 dark:bg-gray-700">
                    <img src="{{ project.image_url }}" alt="{{ project.title }} screenshot" class="object-cover w-full h-full min-h-[250px]">
                </div>
                <div class="p-8 md:w-1/2 flex flex-col justify-center">
                    <div>
                        <h3 class="font-heading text-2xl font-bold mb-2">
                            <i class="{{ project.icon }} text-[var(--color-accent)] mr-2"></i>
                            {{ project.title }}
                        </h3>
                        <p class="text-[var(--color-text-secondary)] mb-4">{{ project.description }}</p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            {% for tech in project.tech_stack %}
                            <span class="bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full dark:bg-blue-900 dark:text-blue-200">{{ tech }}</span>
                            {% endfor %}
                        </div>
                        {% if project.url %}
                        <a href="{{ project.url }}" target="_blank" rel="noopener noreferrer" class="inline-block mt-2 font-semibold text-[var(--color-accent)] hover:underline">
                            View Project <i class="fas fa-external-link-alt ml-1 text-xs"></i>
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    {% else %}
        <div class="interactive-card p-6 rounded-lg shadow-lg stagger-item flex flex-col transform hover:-translate-y-1 transition-transform duration-300">
            <div class="flex-grow">
                <h3 class="font-heading text-2xl font-bold mb-2">
                    <i class="{{ project.icon }} text-[var(--color-accent)] mr-2"></i>
                    {{ project.title }}
                </h3>
                <p class="text-[var(--color-text-secondary)] mb-4">{{ project.description }}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                    {% for tech in project.tech_stack %}
                    <span class="bg-gray-200 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-gray-700 dark:text-gray-300">{{ tech }}</span>
                    {% endfor %}
                </div>
            </div>
            {% if project.url %}
            <a href="{{ project.url }}" target="_blank" rel="noopener noreferrer" class="font-semibold text-[var(--color-accent)] hover:underline self-start">
                View Project <i class="fas fa-external-link-alt ml-1 text-xs"></i>
            </a>
            {% endif %}
        </div>
    {% endif %}
{% endmacro %}

{% macro experience_group(group) %}
    <li class="interactive-card p-6 rounded-lg shadow-lg stagger-item transform hover:-translate-y-2 transition-transform duration-300">
        <h3 class="font-heading text-2xl font-bold mb-4 text-[var(--color-text-primary)]">{{ group.company }}</h3>
        <ul class="space-y-4 pl-5 border-l-2 border-[var(--color-accent)]">
            {% for job in group.roles %}
            <li class="stagger-item">
                <strong class="text-xl text-[var(--color-text-primary)]">{{ job.role }}</strong>
                <span class="block text-sm text-gray-500 dark:text-gray-400">{{ job.period }}</span>
                <p class="mt-1 text-[var(--color-text-secondary)]">{{ job.details }}</p>
            </li>
            {% endfor %}
        </ul>
    </li>
{% endmacro %}

{% macro social_link(url, label, icon_class) %}
    <a href="{{ url }}" aria-label="{{ label }}" class="text-[var(--color-text-primary)] hover:text-[var(--color-accent)] transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2 rounded-full"><i class="{{ icon_class }} fa-2x"></i></a>
{% endmacro %}


{# === MAIN DOCUMENT STRUCTURE === #}

    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-4 focus:left-4 focus:px-4 focus:py-2 focus:bg-[var(--color-card-background)] focus:text-[var(--color-text-primary)] focus:rounded-lg">
      Skip to main content
    </a>

    <div id="scroll-progress-bar"></div>

    <nav class="sticky top-0 shadow-md z-40 transition-colors duration-300 bg-[var(--color-card-background)]">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold font-heading text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2 rounded">{{ portfolio_name }}</a>
            <div class="flex items-center space-x-4">
                <div class="hidden sm:flex space-x-8 text-[var(--color-text-primary)]">
                    {{ nav_link("#about", "About") }}
                    {{ nav_link("#experience", "Experience") }}
                    {{ nav_link("#skills", "Skills") }}
                    {{ nav_link("#projects", "Projects") }}
                    {{ nav_link("#contact", "Contact") }}
                </div>
                <button onclick="toggleTheme()" aria-label="Toggle Theme" class="px-3 py-2 rounded-md shadow transition-colors duration-300 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-accent)] focus-visible:ring-offset-2">
                    <i class="fas fa-moon hidden dark:inline"></i>
                    <i class="fas fa-sun inline dark:hidden"></i>
                </button>
            </div>
        </div>
    </nav>

    <main id="main-content" class="container mx-auto px-4">
        <section id="about" class="py-24 md:py-32 fade-in-section">
            <div class="max-w-6xl mx-auto flex flex-col-reverse md:flex-row items-center justify-center gap-10 md:gap-16">
                <div class="text-center md:text-left stagger-item">
                    <h1 class="font-heading text-4xl md:text-6xl font-bold mb-2 text-[var(--color-text-primary)]">{{ hero_title }}</h1>
                    <p class="font-heading text-xl md:text-2xl text-[var(--color-accent)] font-semibold mb-4">{{ hero_subtitle }}</p>
                    <p class="text-lg text-[var(--color-text-secondary)] max-w-2xl">{{ about_me }}</p>
                </div>
                <div class="flex-shrink-0 stagger-item">
                     <img src="{{ hero_image_url }}" alt="A picture of {{ copyright_name }}" class="rounded-full w-48 h-48 md:w-64 md:h-64 object-cover shadow-2xl border-4 border-white dark:border-gray-700 transform hover:scale-105 transition-transform duration-300">
                </div>
            </div>
        </section>

        <section id="experience" class="py-24 fade-in-section">
            <div class="max-w-4xl mx-auto">
                <h2 class="font-heading text-4xl font-bold mb-12 text-center">Work Experience</h2>
                <ul class="space-y-8">
                    {% for group in grouped_experience %}
                        {{ experience_group(group) }}
                    {% endfor %}
                </ul>
            </div>
        </section>

        <section id="skills" class="py-24 fade-in-section">
            <div class="max-w-4xl mx-auto text-center">
                <h2 class="font-heading text-4xl font-bold mb-12">Skills</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
                    {% for skill in skills %}
                        {{ skill_item(skill) }}
                    {% endfor %}
                </div>
            </div>
        </section>

        <section id="projects" class="py-24 fade-in-section">
            <div class="max-w-5xl mx-auto">
                <h2 class="font-heading text-4xl font-bold mb-12 text-center">Projects</h2>
                {% if featured_project %}
                    {{ project_card(featured_project, is_featured=true) }}
                {% endif %}
                <div class="grid md:grid-cols-2 gap-8">
                    {% for project in other_projects %}
                        {{ project_card(project) }}
                    {% endfor %}
                </div>
            </div>
        </section>

        <section id="play" class="py-24 fade-in-section">
          <div id="play-controls" class="max-w-4xl mx-auto text-center">
            <h2 class="font-heading text-4xl font-bold mb-8">Play with this website!</h2>
            <div class="grid md:grid-cols-2 gap-12 text-left">
                <div>
                    <h3 class="font-heading text-2xl font-semibold mb-4 text-center md:text-left">Customize Theme</h3>
                    <p class="mb-4 text-[var(--color-text-secondary)]">Choose your own theme colors below. Your changes will apply separately for light and dark mode and be saved locally.</p>
                    <div class="mb-6">
                      <button onclick="setMode('light')" class="px-4 py-2 rounded bg-gray-300 text-black dark:bg-gray-600 dark:text-white hover:bg-gray-400 dark:hover:bg-gray-500 mr-2">Edit Light Theme</button>
                      <button onclick="setMode('dark')" class="px-4 py-2 rounded bg-gray-800 text-white hover:bg-gray-700 mr-2">Edit Dark Theme</button>
                    </div>
                    <div class="grid sm:grid-cols-2 gap-6">
                      <div>
                        <label class="block mb-2 font-semibold" for="backgroundColorPicker">Background</label>
                        <input type="color" id="backgroundColorPicker" class="w-full h-10 cursor-pointer" oninput="updateColor('--color-background', this.value)">
                      </div>
                      <div>
                        <label class="block mb-2 font-semibold" for="textPrimaryColorPicker">Primary Text</label>
                        <input type="color" id="textPrimaryColorPicker" class="w-full h-10 cursor-pointer" oninput="updateColor('--color-text-primary', this.value)">
                      </div>
                      <div>
                        <label class="block mb-2 font-semibold" for="textSecondaryColorPicker">Secondary Text</label>
                        <input type="color" id="textSecondaryColorPicker" class="w-full h-10 cursor-pointer" oninput="updateColor('--color-text-secondary', this.value)">
                      </div>
                      <div>
                        <label class="block mb-2 font-semibold" for="cardBackgroundColorPicker">Card Background</label>
                        <input type="color" id="cardBackgroundColorPicker" class="w-full h-10 cursor-pointer" oninput="updateColor('--color-card-background', this.value)">
                      </div>
                      <div>
                        <label class="block mb-2 font-semibold" for="accentColorPicker">Accent</label>
                        <input type="color" id="accentColorPicker" class="w-full h-10 cursor-pointer" oninput="updateColor('--color-accent', this.value)">
                      </div>
                      <div>
                        <label class="block mb-2 font-semibold" for="accentHoverColorPicker">Accent Hover</label>
                        <input type="color" id="accentHoverColorPicker" class="w-full h-10 cursor-pointer" oninput="updateColor('--color-accent-hover', this.value)">
                      </div>
                    </div>
                </div>
                <div>
                    <h3 class="font-heading text-2xl font-semibold mb-4 text-center md:text-left">Arrange Sections</h3>
                    <p class="mb-4 text-[var(--color-text-secondary)]">Drag and drop the sections below, or use your keyboard (Enter/Space to grab, Arrows to move, Esc to drop).</p>
                    <ol id="section-sorter" class="space-y-2">
                        <li data-section-id="experience" tabindex="0" aria-roledescription="Draggable section" aria-grabbed="false" class="p-3 rounded-lg shadow-md cursor-grab bg-gray-100 dark:bg-gray-800 text-[var(--color-text-primary)] flex items-center focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"><i class="fas fa-grip-vertical mr-3 text-gray-400"></i>Experience</li>
                        <li data-section-id="skills" tabindex="0" aria-roledescription="Draggable section" aria-grabbed="false" class="p-3 rounded-lg shadow-md cursor-grab bg-gray-100 dark:bg-gray-800 text-[var(--color-text-primary)] flex items-center focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"><i class="fas fa-grip-vertical mr-3 text-gray-400"></i>Skills</li>
                        <li data-section-id="projects" tabindex="0" aria-roledescription="Draggable section" aria-grabbed="false" class="p-3 rounded-lg shadow-md cursor-grab bg-gray-100 dark:bg-gray-800 text-[var(--color-text-primary)] flex items-center focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"><i class="fas fa-grip-vertical mr-3 text-gray-400"></i>Projects</li>
                        <li data-section-id="play" tabindex="0" aria-roledescription="Draggable section" aria-grabbed="false" class="p-3 rounded-lg shadow-md cursor-grab bg-gray-100 dark:bg-gray-800 text-[var(--color-text-primary)] flex items-center focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"><i class="fas fa-grip-vertical mr-3 text-gray-400"></i>Play Section</li>
                    </ol>
                </div>
            </div>
            <div class="mt-12">
                <button onclick="resetAllCustomizations()" class="px-6 py-3 rounded-lg bg-red-500 text-white hover:bg-red-600 font-semibold">Reset All Customizations</button>
            </div>
          </div>
        </section>
    </main>

    <footer id="contact" class="py-24 bg-gray-100 dark:bg-gray-800 fade-in-section">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <h2 class="font-heading text-3xl font-bold mb-4">Contact</h2>
            <p class="mb-6 text-[var(--color-text-secondary)]">Feel free to connect with me!</p>
            <div class="flex justify-center space-x-6">
                {{ social_link(contact_info.github_url, "GitHub", "fab fa-github") }}
                {{ social_link(contact_info.linkedin_url, "LinkedIn", "fab fa-linkedin") }}
                {{ social_link(contact_info.bandcamp_url, "Bandcamp", "fab fa-bandcamp") }}
                {{ social_link(contact_info.kofi_url, "Ko-fi", "fas fa-coffee") }}
            </div>
            <p class="mt-8 text-sm text-gray-500 dark:text-gray-400">&copy; {{ copyright_string }} {{ copyright_name }}</p>
        </div>
    </footer>

<script>
function initSectionReordering() {
    const sorter = document.getElementById('section-sorter');
    let grabbedItem = null;

    defaultSectionOrder = Array.from(sorter.children).map(item => item.dataset.sectionId);

    const savedOrder = JSON.parse(localStorage.getItem('sectionOrder'));
    if (savedOrder) {
        applySectionOrder(savedOrder);
    }

    Sortable.create(sorter, {
        animation: 150,
        ghostClass: 'sortable-ghost',
        chosenClass: 'sortable-chosen',
        onEnd: function () {
            const newOrder = Array.from(sorter.children).map(item => item.dataset.sectionId);
            saveSectionOrder(newOrder);
            applySectionOrder(newOrder);
        },
    });

    sorter.addEventListener('keydown', (e) => {
        const target = e.target;
        if (target.tagName !== 'LI') return;

        if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            if (grabbedItem === target) {
                // Drop item
                grabbedItem.classList.remove('grabbing');
                grabbedItem.setAttribute('aria-grabbed', 'false');
                grabbedItem = null;
            } else {
                // Grab item
                if (grabbedItem) {
                    grabbedItem.classList.remove('grabbing');
                    grabbedItem.setAttribute('aria-grabbed', 'false');
                }
                grabbedItem = target;
                grabbedItem.classList.add('grabbing');
                grabbedItem.setAttribute('aria-grabbed', 'true');
            }
        }

        if (grabbedItem) {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prevSibling = grabbedItem.previousElementSibling;
                if (prevSibling) {
                    sorter.insertBefore(grabbedItem, prevSibling);
                    grabbedItem.focus();
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                const nextSibling = grabbedItem.nextElementSibling;
                if (nextSibling) {
                    sorter.insertBefore(grabbedItem, nextSibling.nextElementSibling);
                    grabbedItem.focus();
                }
            } else if (e.key === 'Escape') {
                grabbedItem.classList.remove('grabbing');
                grabbedItem.setAttribute('aria-grabbed', 'false');
                grabbedItem = null;
            }

            if (['ArrowUp', 'ArrowDown'].includes(e.key)) {
                const newOrder = Array.from(sorter.children).map(item => item.dataset.sectionId);
                saveSectionOrder(newOrder);
                applySectionOrder(newOrder);
            }
        }
    });
}

function saveSectionOrder(order) {
    localStorage.setItem('sectionOrder', JSON.stringify(order));
}

function applySectionOrder(order) {
    const mainContent = document.getElementById('main-content');
    const sorter = document.getElementById('section-sorter');

    order.forEach(sectionId => {
        const sectionElement = document.getElementById(sectionId);
        if (sectionElement) {
            mainContent.appendChild(sectionElement);
        }
    });

    order.forEach(sectionId => {
        const listItem = sorter.querySelector(`[data-section-id="${sectionId}"]`);
        if (listItem) {
            sorter.appendChild(listItem);
        }
    });
}

function resetAllCustomizations() {
  localStorage.removeItem('customColors');
  localStorage.removeItem('theme');
  localStorage.removeItem('sectionOrder');

  const colorVars = [
    '--color-background', '--color-text-primary', '--color-text-secondary',
    '--color-card-background', '--color-accent', '--color-accent-hover'
  ];
  colorVars.forEach(v => document.documentElement.style.removeProperty(v));

  setMode('dark');
  applySectionOrder(defaultSectionOrder);

  // Add flash effect for visual feedback
  const playControls = document.getElementById('play-controls');
  playControls.classList.add('animate-flash');
  setTimeout(() => {
    playControls.classList.remove('animate-flash');
  }, 1000);
}

function idToCssVar(id) {
  const map = {
    'backgroundColorPicker': '--color-background',
    'textPrimaryColorPicker': '--color-text-primary',
    'textSecondaryColorPicker': '--color-text-secondary',
    'cardBackgroundColorPicker': '--color-card-background',
    'accentColorPicker': '--color-accent',
    'accentHoverColorPicker': '--color-accent-hover'
  };
  return map[id] || '';
}

function updateColor(cssVar, value) {
  document.documentElement.style.setProperty(cssVar, value);
  saveThemeColor(cssVar, value);
}

function saveThemeColor(cssVar, value) {
  let colors = JSON.parse(localStorage.getItem('customColors') || '{}');
  const mode = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  if (!colors[mode]) colors[mode] = {};
  colors[mode][cssVar] = value;
  localStorage.setItem('customColors', JSON.stringify(colors));
}

function applySavedThemeColors() {
  const colors = JSON.parse(localStorage.getItem('customColors') || '{}');
  const mode = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  if (colors[mode]) {
    for (const [key, value] of Object.entries(colors[mode])) {
      document.documentElement.style.setProperty(key, value);
    }
  }
}

function updatePickers() {
  const colorVars = [
    '--color-background',
    '--color-text-primary',
    '--color-text-secondary',
    '--color-card-background',
    '--color-accent',
    '--color-accent-hover'
  ];
  const pickerIds = [
    'backgroundColorPicker',
    'textPrimaryColorPicker',
    'textSecondaryColorPicker',
    'cardBackgroundColorPicker',
    'accentColorPicker',
    'accentHoverColorPicker'
  ];
  colorVars.forEach((v, i) => {
    const originalValue = document.documentElement.style.getPropertyValue(v);
    document.documentElement.style.removeProperty(v);
    const val = getComputedStyle(document.documentElement).getPropertyValue(v).trim() || '#000000';
    document.getElementById(pickerIds[i]).value = val;
    if (originalValue) {
        document.documentElement.style.setProperty(v, originalValue);
    }
  });
}

function setMode(mode) {
  if (mode === 'dark') {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
  applySavedThemeColors();
  updatePickers();
}

window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) setMode(savedTheme);

  applySavedThemeColors();
  updatePickers();
});
</script>

    <button id="back-to-top-btn" title="Go to top">
        <i class="fas fa-arrow-up"></i>
    </button>

</body>
</html>
"""


@app.route("/")
def serve_index():
    data = load_data()
    return render_template_string(template, **data)


@app.route('/<path:path>')
def serve_static_root(path):
    return send_from_directory('output', path)


def write_static_html():
    """
    Generates the static HTML file and downloads remote assets to a local
    'static' directory if they don't already exist.
    """
    output_dir = "output"
    static_dir = os.path.join(output_dir, "static")
    os.makedirs(static_dir, exist_ok=True)

    fa_version = "6.4.0"
    fa_zip_url = f"https://use.fontawesome.com/releases/v{fa_version}/fontawesome-free-{fa_version}-web.zip"
    fa_extract_path = os.path.join(static_dir, f"fontawesome-free-{fa_version}-web")

    if not os.path.exists(fa_extract_path):
        try:
            print(f"Downloading Font Awesome v{fa_version}...")
            response = requests.get(fa_zip_url, timeout=30)
            response.raise_for_status()

            print("Extracting Font Awesome...")
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(static_dir)
            print("Successfully downloaded and extracted Font Awesome.")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading Font Awesome: {e}")
        except zipfile.BadZipFile:
            print("Error: Downloaded file is not a valid zip file.")

    tailwind_url = "https://cdn.tailwindcss.com"
    tailwind_local_path = os.path.join(static_dir, "tailwindcss.js")
    if not os.path.exists(tailwind_local_path):
        try:
            print(f"Downloading tailwindcss.js...")
            response = requests.get(tailwind_url, timeout=10)
            response.raise_for_status()
            with open(tailwind_local_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Successfully downloaded tailwindcss.js.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading tailwindcss.js: {e}")

    data = load_data()
    # For the dev server, use absolute paths
    server_template = template

    # For the static file, use relative paths
    file_template = template.replace('src="/static/', 'src="static/').replace('href="/static/', 'href="static/')
    rendered_for_file = render_template_string(file_template, **data)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(rendered_for_file)


if __name__ == "__main__":
    with app.app_context():
        write_static_html()
        print(f"Static HTML file and assets generated in 'output/' directory.")

    print("Starting development server at http://localhost:5000")
    app.run(debug=True)
