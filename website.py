from flask import Flask, render_template_string
import os
import json

app = Flask(__name__)


# Load data from external JSON file
def load_data():
    # Create a dummy website_data.json if it doesn't exist for demonstration
    if not os.path.exists("website_data.json"):
        dummy_data = {
            "website_title": "My Awesome Developer Portfolio",
            "portfolio_name": "MyPortfolio", # Added for configurable portfolio name
            "about_me": "Hello! I'm a software developer with a passion for building clean and efficient solutions. I specialize in web development and enjoy working with Python, JavaScript, and modern front-end frameworks. My goal is to create impactful and user-friendly applications.",
            "projects": [
                {"title": "Project Alpha", "description": "A web application built with React and Node.js.", "url": "https://github.com/yourusername/project-alpha", "icon": "fas fa-laptop-code"}, # Added URL and Icon
                {"title": "Project Beta", "description": "Mobile app development using Flutter.", "url": "https://github.com/yourusername/project-beta", "icon": "fas fa-mobile-alt"}, # Added URL and Icon
                {"title": "Project Gamma", "description": "Data analysis project with Python and Pandas.", "url": "https://github.com/yourusername/project-gamma", "icon": "fas fa-chart-line"} # Added URL and Icon
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
            "contact_info": { # Added contact information
                "github_url": "https://github.com/yourusername",
                "linkedin_url": "https://linkedin.com/in/yourusername",
                "bandcamp_url": "https://yourusername.bandcamp.com",
                "kofi_url": "https://ko-fi.com/yourusername"
            },
            "copyright_name": "Your Name" # Added copyright name
        }
        with open("website_data.json", "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=4)

    with open("website_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Group experience by company
    grouped_experience = []
    if "experience" in data:
        current_company = None
        for job in data["experience"]:
            if job["company"] != current_company:
                grouped_experience.append({
                    "company": job["company"],
                    "roles": []
                })
                current_company = job["company"]
            grouped_experience[-1]["roles"].append({
                "role": job["role"],
                "period": job["period"],
                "details": job["details"]
            })
    data["grouped_experience"] = grouped_experience
    return data


# Tailwind CSS with Dark Mode and theme toggle logic + interactive card spotlight effect
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ website_title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
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
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.theme = 'light';
            } else {
                document.documentElement.classList.add('dark');
                localStorage.theme = 'dark';
            }
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
                navbar.classList.add('bg-gray-900', 'text-gray-100');
            } else {
                navbar.classList.remove('bg-gray-900', 'text-gray-100');
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
            if (window.scrollY > 300) { // Show button after scrolling 300px
                backToTopBtn.classList.remove('opacity-0', 'invisible');
                backToTopBtn.classList.add('opacity-100', 'visible');
            } else {
                backToTopBtn.classList.remove('opacity-100', 'visible');
                backToTopBtn.classList.add('opacity-0', 'invisible');
            }
        }

        // Intersection Observer for fade-in/slide-up effect with staggering
        document.addEventListener('DOMContentLoaded', () => {
            // Apply theme based on localStorage or system preference
            if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }

            // Initialize the interactive card effect
            applyInteractiveCardEffect();
            applyNavbarTheme(); // Apply initial navbar theme on load

            // Add scroll event listeners
            window.addEventListener('scroll', updateScrollProgress);
            window.addEventListener('scroll', toggleBackToTopButton);

            const observerOptions = {
                root: null, // viewport
                rootMargin: '0px',
                threshold: 0.1 // 10% of the target element is visible
            };

            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible'); // Add the class to trigger section animation

                        // Staggered animation for children
                        const staggerItems = entry.target.querySelectorAll('.stagger-item');
                        staggerItems.forEach((item, index) => {
                            // Use setTimeout to apply 'is-visible' with a delay
                            setTimeout(() => {
                                item.classList.add('is-visible');
                            }, index * 100); // 100ms delay between each item
                        });

                        observer.unobserve(entry.target); // Stop observing once animated
                    }
                });
            }, observerOptions);

            // Observe sections for fade-in effect
            document.querySelectorAll('section.fade-in-section').forEach(section => {
                observer.observe(section);
            });

            // Smooth scroll for back to top button
            document.getElementById('back-to-top-btn').addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        html {
            scroll-behavior: smooth;
        }

        body {
            /* Subtle gradient background */
            background: linear-gradient(to bottom right, var(--tw-gradient-stops));
            --tw-gradient-stops: var(--tw-gradient-from, #f8fafc) var(--tw-gradient-to, #e2e8f0); /* light mode */
        }

        .dark body {
            --tw-gradient-stops: var(--tw-gradient-from, #1f2937) var(--tw-gradient-to, #111827); /* dark mode */
        }

        /* Scroll Progress Bar */
        #scroll-progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background-color: #3b82f6; /* Blue-500 */
            width: 0%;
            z-index: 50; /* Above navbar */
            transition: width 0.1s linear; /* Smooth update */
        }

        /* Back to Top Button */
        #back-to-top-btn {
            position: fixed;
            bottom: 1.5rem; /* 24px */
            right: 1.5rem; /* 24px */
            background-color: #3b82f6; /* Blue-500 */
            color: white;
            padding: 0.75rem; /* 12px */
            border-radius: 9999px; /* Full rounded */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
            opacity: 0;
            visibility: hidden;
            z-index: 40; /* Below progress bar, above content */
            cursor: pointer;
        }
        #back-to-top-btn:hover {
            background-color: #2563eb; /* Blue-600 */
        }
        /* Focus-visible for accessibility */
        #back-to-top-btn:focus-visible {
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5); /* Blue-500 with transparency */
        }


        /* Styles for the interactive card spotlight effect */
        .interactive-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            border-radius: inherit; /* Match the parent's border-radius */
            /* The spotlight gradient, positioned by JS */
            background: radial-gradient(
                400px circle at var(--mouseX) var(--mouseY),
                rgba(255, 255, 255, 0.2),
                transparent 40%
            );
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
            z-index: 1; /* Sit above the card background but below content */
        }

        /* In dark mode, we can use a slightly different effect if desired */
        .dark .interactive-card::before {
             background: radial-gradient(
                400px circle at var(--mouseX) var(--mouseY),
                rgba(255, 255, 255, 0.1), /* More subtle glow for dark background */
                transparent 40%
            );
        }

        /* Show the effect on hover */
        .interactive-card:hover::before {
            opacity: 1;
        }

        /* Ensure card content (text, etc.) sits above the spotlight effect */
        .interactive-card > * {
            position: relative;
            z-index: 2;
        }

        /* Styles for the main section fade-in effect (container) */
        .fade-in-section {
            opacity: 0;
            transition: opacity 0.5s ease-out; /* Faster fade for the section container */
        }
        .fade-in-section.is-visible {
            opacity: 1;
        }

        /* Styles for staggered items within sections */
        .stagger-item {
            opacity: 0;
            transform: translateY(20px); /* Start 20px below its final position */
            transition: opacity 0.5s cubic-bezier(0.5, 0, 0, 1.5),
                        transform 0.5s cubic-bezier(0.5, 0, 0, 1.5);
        }
        .stagger-item.is-visible {
            opacity: 1;
            transform: translateY(0);
        }


        /* Accessibility: Disable animations for users who prefer reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .fade-in-section, .stagger-item {
                transition: none !important;
                transform: none !important;
                opacity: 1 !important;
            }
            #back-to-top-btn {
                transition: none !important;
            }
        }
    </style>
</head>
<body class="bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-inter">

    <!-- Scroll Progress Bar -->
    <div id="scroll-progress-bar"></div>

    <nav class="sticky top-0 shadow z-40 transition-colors duration-300">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold text-gray-100 dark:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">{{ portfolio_name }}</a>

            <div class="flex items-center space-x-4">
                <div class="hidden sm:flex space-x-6">
                    <a href="#about" class="hover:text-gray-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">About</a>
                    <a href="#experience" class="hover:text-gray-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Experience</a>
                    <a href="#skills" class="hover:text-gray-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Skills</a>
                    <a href="#projects" class="hover:text-gray-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Projects</a>
                    <a href="#contact" class="hover:text-gray-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">Contact</a>
                </div>

                <div class="flex space-x-2">
                    <button
                        onclick="toggleTheme()"
                        class="px-4 py-2 rounded shadow transition-colors duration-300
                               bg-gray-200 text-gray-800
                               dark:bg-gray-700 dark:text-gray-100
                               hover:bg-gray-300 dark:hover:bg-gray-600
                               focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
                        Toggle Theme
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <section id="about" class="py-20 fade-in-section">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">About Me</h2>
            <p class="text-lg">{{ about_me }}</p>
        </div>
    </section>

    <section id="experience" class="py-20 fade-in-section">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Work Experience</h2>
            <ul class="space-y-6"> {# Increased space for grouped items #}
                {% for company_group in grouped_experience %}
                <li class="interactive-card p-6 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800 relative overflow-hidden stagger-item">
                    <h3 class="text-2xl font-bold mb-3">{{ company_group.company }}</h3>
                    <ul class="space-y-3 pl-4 border-l-2 border-gray-300 dark:border-gray-600">
                        {% for job in company_group.roles %}
                        <li class="stagger-item">
                            <strong class="text-xl">{{ job.role }}</strong> - <span class="text-gray-600 dark:text-gray-400">{{ job.period }}</span><br>
                            <p class="mt-1 text-sm">{{ job.details }}</p>
                        </li>
                        {% endfor %}
                    </ul>
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>

    <section id="skills" class="py-20 fade-in-section">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Skills</h2>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                {% for skill in skills %}
                <div class="stagger-item p-4 rounded shadow text-center
                            bg-gray-200 dark:bg-gray-700
                            text-gray-800 dark:text-gray-100">
                    {% if skill.icon %}<i class="{{ skill.icon }} mr-2"></i>{% endif %}
                    {{ skill.name }}
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="projects" class="py-20 fade-in-section">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Projects</h2>
            <ul class="space-y-4">
                {% for project in projects %}
                <li class="interactive-card p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800 relative overflow-hidden stagger-item">
                    <strong class="text-xl">
                        {% if project.url %}
                            <a href="{{ project.url }}" target="_blank" rel="noopener noreferrer" class="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded">
                                {% if project.icon %}<i class="{{ project.icon }} mr-2"></i>{% endif %}
                                {{ project.title }}
                            </a>
                        {% else %}
                            {% if project.icon %}<i class="{{ project.icon }} mr-2"></i>{% endif %}
                            {{ project.title }}
                        {% endif %}
                    </strong> - <span class="text-gray-600 dark:text-gray-400">{{ project.description }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>

    <section id="contact" class="py-20 fade-in-section">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <h2 class="text-3xl font-bold mb-4">Contact</h2>
            <p class="mb-6">Feel free to connect with me on social media!</p>
            <div class="space-x-6">
                <a href="{{ contact_info.github_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded"><i class="fab fa-github fa-2x"></i></a>
                <a href="{{ contact_info.linkedin_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded"><i class="fab fa-linkedin fa-2x"></i></a>
                <a href="{{ contact_info.bandcamp_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded"><i class="fab fa-bandcamp fa-2x"></i></a>
                <a href="{{ contact_info.kofi_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded"><i class="fa fa-coffee fa-2x"></i></a>
            </div>
            <p class="mt-6 text-sm text-gray-500 dark:text-gray-400">&copy; 2025 {{ copyright_name }}</p>
        </div>
    </section>

    <!-- Back to Top Button -->
    <button id="back-to-top-btn" title="Go to top">
        <i class="fas fa-arrow-up"></i>
    </button>

</body>
</html>
"""


@app.route("/")
def index():
    data = load_data()
    return render_template_string(template,
                                  website_title=data.get("website_title", "Developer Portfolio"),
                                  portfolio_name=data.get("portfolio_name", "MyPortfolio"), # Pass portfolio name
                                  about_me=data.get("about_me", "Hello! I'm a software developer..."),
                                  projects=data["projects"],
                                  # Pass the grouped experience data
                                  grouped_experience=data["grouped_experience"],
                                  skills=data["skills"],
                                  contact_info=data.get("contact_info", {"github_url": "#", "linkedin_url": "#", "bandcamp_url": "#", "kofi_url": "#"}),
                                  copyright_name=data.get("copyright_name", "Your Name"))


def write_static_html():
    data = load_data()
    rendered = render_template_string(template,
                                      website_title=data.get("website_title", "Developer Portfolio"),
                                      portfolio_name=data.get("portfolio_name", "MyPortfolio"), # Pass portfolio name
                                      about_me=data.get("about_me", "Hello! I'm a software developer..."),
                                      projects=data["projects"],
                                      # Pass the grouped experience data
                                      grouped_experience=data["grouped_experience"],
                                      skills=data["skills"],
                                      contact_info=data.get("contact_info", {"github_url": "#", "linkedin_url": "#", "bandcamp_url": "#", "kofi_url": "#"}),
                                      copyright_name=data.get("copyright_name", "Your Name"))
    os.makedirs("output", exist_ok=True)
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(rendered)


if __name__ == "__main__":
    with app.app_context():
        write_static_html()
    app.run(debug=True)
