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


# Tailwind CSS with Dark Mode and theme toggle logic + interactive card spotlight effect
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ website_title }}</title>
    <!-- === UPDATED: Point to local static files with correct paths === -->
    <script src="/static/tailwindcss.js"></script>
    <link rel="stylesheet" href="/static/fontawesome-free-6.4.0-web/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        inter: ['Inter', 'sans-serif'],
                    },
                },
            },
        }

        // Function to toggle theme and save preference to localStorage
        function toggleTheme() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.theme = isDark ? 'dark' : 'light';
            applyNavbarTheme(); // Apply theme to navbar immediately
        }

        // Function to apply the interactive spotlight effect to cards
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

        // Function to apply the correct navbar theme classes
        function applyNavbarTheme() {
            const navbar = document.querySelector('nav');
            if (document.documentElement.classList.contains('dark')) {
                navbar.classList.remove('bg-white', 'text-gray-900');
                navbar.classList.add('bg-gray-800', 'text-gray-100');
            } else {
                navbar.classList.remove('bg-gray-800', 'text-gray-100');
                navbar.classList.add('bg-white', 'text-gray-900');
            }
        }

        // Function to update scroll progress bar
        function updateScrollProgress() {
            const progressBar = document.getElementById('scroll-progress-bar');
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = document.documentElement.scrollTop;
            const percentage = (scrolled / scrollHeight) * 100;
            progressBar.style.width = percentage + '%';
        }

        // Function to toggle back-to-top button visibility
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

        // Intersection Observer for fade-in/slide-up effect with staggering
        document.addEventListener('DOMContentLoaded', () => {
            if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            applyInteractiveCardEffect();
            applyNavbarTheme();
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
        });
    </script>
    <style>
        html { scroll-behavior: smooth; }
        body { font-family: 'Inter', sans-serif; transition: background-color 0.3s, color 0.3s; }
        #scroll-progress-bar { position: fixed; top: 0; left: 0; height: 4px; background-color: #3b82f6; width: 0%; z-index: 50; transition: width 0.1s linear; }
        #back-to-top-btn { position: fixed; bottom: 1.5rem; right: 1.5rem; background-color: #3b82f6; color: white; padding: 0.75rem; border-radius: 9999px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out; opacity: 0; visibility: hidden; z-index: 40; cursor: pointer; }
        #back-to-top-btn:hover { background-color: #2563eb; }
        #back-to-top-btn:focus-visible { outline: none; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5); }
        .interactive-card { position: relative; overflow: hidden; }
        .interactive-card::before { content: ""; position: absolute; left: 0; top: 0; width: 100%; height: 100%; border-radius: inherit; background: radial-gradient(400px circle at var(--mouseX) var(--mouseY), rgba(255, 255, 255, 0.2), transparent 40%); opacity: 0; transition: opacity 0.3s ease-in-out; z-index: 1; }
        .dark .interactive-card::before { background: radial-gradient(400px circle at var(--mouseX) var(--mouseY), rgba(255, 255, 255, 0.1), transparent 40%); }
        .interactive-card:hover::before { opacity: 1; }
        .interactive-card > * { position: relative; z-index: 2; }
        .fade-in-section { opacity: 0; transition: opacity 0.5s ease-out; }
        .fade-in-section.is-visible { opacity: 1; }
        .stagger-item { opacity: 0; transform: translateY(20px); transition: opacity 0.5s cubic-bezier(0.5, 0, 0, 1.5), transform 0.5s cubic-bezier(0.5, 0, 0, 1.5); }
        .stagger-item.is-visible { opacity: 1; transform: translateY(0); }
        @media (prefers-reduced-motion: reduce) { .fade-in-section, .stagger-item, #back-to-top-btn { transition: none !important; transform: none !important; opacity: 1 !important; } }
    </style>
</head>
<body class="bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100">

    <div id="scroll-progress-bar"></div>

    <nav class="sticky top-0 shadow-md z-40 transition-colors duration-300 bg-white dark:bg-gray-800">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold text-gray-900 dark:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">{{ portfolio_name }}</a>
            <div class="flex items-center space-x-4">
                <div class="hidden sm:flex space-x-6 text-gray-900 dark:text-gray-100">
                    <a href="#about" class="hover:text-blue-600 dark:hover:text-blue-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">About</a>
                    <a href="#experience" class="hover:text-blue-600 dark:hover:text-blue-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Experience</a>
                    <a href="#skills" class="hover:text-blue-600 dark:hover:text-blue-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Skills</a>
                    <a href="#projects" class="hover:text-blue-600 dark:hover:text-blue-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Projects</a>
                    <a href="#contact" class="hover:text-blue-600 dark:hover:text-blue-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Contact</a>
                </div>
                <button onclick="toggleTheme()" aria-label="Toggle Theme" class="px-3 py-2 rounded-md shadow transition-colors duration-300 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
                    <i class="fas fa-moon hidden dark:inline"></i>
                    <i class="fas fa-sun inline dark:hidden"></i>
                </button>
            </div>
        </div>
    </nav>

    <main class="container mx-auto px-4">
        <section id="about" class="py-20 md:py-32 fade-in-section">
            <div class="max-w-6xl mx-auto flex flex-col-reverse md:flex-row items-center justify-center gap-10 md:gap-16">
                <div class="text-center md:text-left stagger-item">
                    <h1 class="text-4xl md:text-6xl font-bold mb-2 text-gray-900 dark:text-white">{{ hero_title }}</h1>
                    <p class="text-xl md:text-2xl text-blue-600 dark:text-blue-400 font-semibold mb-4">{{ hero_subtitle }}</p>
                    <p class="text-lg text-gray-700 dark:text-gray-300 max-w-2xl">{{ about_me }}</p>
                </div>
                <div class="flex-shrink-0 stagger-item">
                     <img src="{{ hero_image_url }}" alt="A picture of {{ copyright_name }}" class="rounded-full w-48 h-48 md:w-64 md:h-64 object-cover shadow-2xl border-4 border-white dark:border-gray-700 transform hover:scale-105 transition-transform duration-300">
                </div>
            </div>
        </section>

        <section id="experience" class="py-20 fade-in-section">
            <div class="max-w-4xl mx-auto">
                <h2 class="text-4xl font-bold mb-8 text-center">Work Experience</h2>
                <ul class="space-y-8">
                    {% for company_group in grouped_experience %}
                    <li class="interactive-card p-6 rounded-lg shadow-lg bg-white dark:bg-gray-800 stagger-item">
                        <h3 class="text-2xl font-bold mb-4 text-gray-900 dark:text-white">{{ company_group.company }}</h3>
                        <ul class="space-y-4 pl-5 border-l-2 border-blue-500 dark:border-blue-400">
                            {% for job in company_group.roles %}
                            <li class="stagger-item">
                                <strong class="text-xl text-gray-800 dark:text-gray-200">{{ job.role }}</strong>
                                <span class="block text-sm text-gray-500 dark:text-gray-400">{{ job.period }}</span>
                                <p class="mt-1 text-gray-600 dark:text-gray-300">{{ job.details }}</p>
                            </li>
                            {% endfor %}
                        </ul>
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </section>

        <section id="skills" class="py-20 fade-in-section">
            <div class="max-w-4xl mx-auto text-center">
                <h2 class="text-4xl font-bold mb-8">Skills</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
                    {% for skill in skills %}
                    <div class="stagger-item flex flex-col items-center justify-center p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-100 transform hover:scale-105 transition-transform duration-300">
                        <i class="{{ skill.icon }} text-4xl mb-2 text-blue-500"></i>
                        <span>{{ skill.name }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>

        <section id="projects" class="py-20 fade-in-section">
            <div class="max-w-5xl mx-auto">
                <h2 class="text-4xl font-bold mb-12 text-center">Projects</h2>

                {% if featured_project %}
                <div class="mb-16 stagger-item">
                    <div class="interactive-card rounded-lg shadow-xl bg-white dark:bg-gray-800 overflow-hidden md:flex transform hover:-translate-y-2 transition-transform duration-300">
                        <div class="md:w-1/2 bg-gray-200 dark:bg-gray-700">
                            <img src="{{ featured_project.image_url }}" alt="{{ featured_project.title }} screenshot" class="object-cover w-full h-full min-h-[250px]">
                        </div>
                        <div class="p-8 md:w-1/2 flex flex-col justify-center">
                            <div>
                                <h3 class="text-2xl font-bold mb-2">
                                    <i class="{{ featured_project.icon }} text-blue-500 mr-2"></i>
                                    {{ featured_project.title }}
                                </h3>
                                <p class="text-gray-600 dark:text-gray-300 mb-4">{{ featured_project.description }}</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    {% for tech in featured_project.tech_stack %}
                                    <span class="bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full dark:bg-blue-900 dark:text-blue-200">{{ tech }}</span>
                                    {% endfor %}
                                </div>
                                {% if featured_project.url %}
                                <a href="{{ featured_project.url }}" target="_blank" rel="noopener noreferrer" class="inline-block mt-2 font-semibold text-blue-600 dark:text-blue-400 hover:underline">
                                    View Project <i class="fas fa-external-link-alt ml-1 text-xs"></i>
                                </a>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
                {% endif %}

                <div class="grid md:grid-cols-2 gap-8">
                    {% for project in other_projects %}
                    <div class="interactive-card p-6 rounded-lg shadow-lg bg-white dark:bg-gray-800 stagger-item flex flex-col transform hover:-translate-y-1 transition-transform duration-300">
                        <div class="flex-grow">
                            <h3 class="text-2xl font-bold mb-2">
                                <i class="{{ project.icon }} text-blue-500 mr-2"></i>
                                {{ project.title }}
                            </h3>
                            <p class="text-gray-600 dark:text-gray-300 mb-4">{{ project.description }}</p>
                            <div class="flex flex-wrap gap-2 mb-4">
                                {% for tech in project.tech_stack %}
                                <span class="bg-gray-200 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-gray-700 dark:text-gray-300">{{ tech }}</span>
                                {% endfor %}
                            </div>
                        </div>
                        {% if project.url %}
                        <a href="{{ project.url }}" target="_blank" rel="noopener noreferrer" class="font-semibold text-blue-600 dark:text-blue-400 hover:underline self-start">
                            View Project <i class="fas fa-external-link-alt ml-1 text-xs"></i>
                        </a>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
    </main>

    <footer id="contact" class="py-20 bg-gray-100 dark:bg-gray-800 fade-in-section">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <h2 class="text-3xl font-bold mb-4">Contact</h2>
            <p class="mb-6 text-gray-700 dark:text-gray-300">Feel free to connect with me!</p>
            <div class="flex justify-center space-x-6">
                <a href="{{ contact_info.github_url }}" aria-label="GitHub" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded-full"><i class="fab fa-github fa-2x"></i></a>
                <a href="{{ contact_info.linkedin_url }}" aria-label="LinkedIn" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded-full"><i class="fab fa-linkedin fa-2x"></i></a>
                <a href="{{ contact_info.bandcamp_url }}" aria-label="Bandcamp" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded-full"><i class="fab fa-bandcamp fa-2x"></i></a>
                <a href="{{ contact_info.kofi_url }}" aria-label="Ko-fi" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded-full"><i class="fas fa-coffee fa-2x"></i></a>
            </div>
            <p class="mt-8 text-sm text-gray-500 dark:text-gray-400">&copy; {{ copyright_string }} {{ copyright_name }}</p>
        </div>
    </footer>

    <button id="back-to-top-btn" title="Go to top">
        <i class="fas fa-arrow-up"></i>
    </button>

</body>
</html>
"""


# --- UPDATED: Add explicit routes for root and static files for the dev server ---
@app.route("/")
def serve_index():
    # This route will now serve the pre-generated index.html for the dev server
    return send_from_directory('output', 'index.html')


@app.route('/<path:path>')
def serve_static_root(path):
    # This is needed to serve files like favicon.ico from the root of output
    return send_from_directory('output', path)


def write_static_html():
    """
    Generates the static HTML file and downloads remote assets to a local
    'static' directory if they don't already exist.
    """
    output_dir = "output"
    static_dir = os.path.join(output_dir, "static")
    os.makedirs(static_dir, exist_ok=True)

    # --- UPDATED: Logic to download and extract Font Awesome zip ---
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

    # --- Logic to download Tailwind CSS ---
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

    # Generate the main index.html file
    data = load_data()
    rendered = render_template_string(template, **data)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(rendered)


if __name__ == "__main__":
    # Generate all static files before starting the server
    with app.app_context():
        write_static_html()
        print(f"Static HTML file and assets generated in 'output/' directory.")

    # Run the development server
    print("Starting development server at http://localhost:5000")
    app.run(debug=True)
