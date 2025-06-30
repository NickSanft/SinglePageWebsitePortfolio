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
            "about_me": "Hello! I'm a software developer with a passion for building clean and efficient solutions. I specialize in web development and enjoy working with Python, JavaScript, and modern front-end frameworks. My goal is to create impactful and user-friendly applications.",
            "projects": [
                {"title": "Project Alpha", "description": "A web application built with React and Node.js."},
                {"title": "Project Beta", "description": "Mobile app development using Flutter."},
                {"title": "Project Gamma", "description": "Data analysis project with Python and Pandas."}
            ],
            "experience": [
                {"role": "Software Engineer", "company": "Tech Solutions Inc.", "period": "Jan 2022 - Present",
                 "details": "Developed and maintained web services using Python and Django."},
                {"role": "Junior Developer", "company": "Innovate Co.", "period": "Jul 2020 - Dec 2021",
                 "details": "Assisted in front-end development with HTML, CSS, and JavaScript."}
            ],
            "skills": [
                "Python", "JavaScript", "React", "Node.js", "Tailwind CSS", "Flask", "SQL", "Git", "Cloud Computing"
            ],
            "contact_info": { # Added contact information
                "github_url": "https://github.com/yourusername",
                "linkedin_url": "https://linkedin.com/in/yourusername",
                "bandcamp_url": "https://yourusername.bandcamp.com",
                "kofi_url": "https://ko-fi.com/yourusername" # Added Ko-fi URL
            }
        }
        with open("website_data.json", "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=4)

    with open("website_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


# Tailwind CSS with Dark Mode and theme toggle logic + interactive card spotlight effect
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ website_title }}</title> <!-- Dynamic website title -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class'
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

        // On page load, apply theme and initialize effects
        document.addEventListener('DOMContentLoaded', () => {
            // Apply theme based on localStorage or system preference
            if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }

            // Initialize the interactive card effect
            applyInteractiveCardEffect();
        });
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        html {
            scroll-behavior: smooth;
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
    </style>
</head>
<body class="bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans">

    <!-- Navigation Bar -->
    <nav class="sticky top-0 bg-gray-900 text-white shadow z-40">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold">MyPortfolio</a>

            <!-- Right side container for links and buttons -->
            <div class="flex items-center space-x-4">
                <!-- Navigation Links (hidden on small screens) -->
                <div class="hidden sm:flex space-x-6">
                    <a href="#about" class="hover:text-gray-300">About</a>
                    <a href="#experience" class="hover:text-gray-300">Experience</a>
                    <a href="#skills" class="hover:text-gray-300">Skills</a>
                    <a href="#projects" class="hover:text-gray-300">Projects</a>
                    <a href="#contact" class="hover:text-gray-300">Contact</a>
                </div>

                <!-- Theme Toggle Button -->
                <div class="flex space-x-2">
                    <button
                        onclick="toggleTheme()"
                        class="px-4 py-2 rounded shadow transition-colors duration-300
                               bg-gray-200 text-gray-800
                               dark:bg-gray-700 dark:text-gray-100
                               hover:bg-gray-300 dark:hover:bg-gray-600">
                        Toggle Theme
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- About Section -->
    <section id="about" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">About Me</h2>
            <p class="text-lg">{{ about_me }}</p> <!-- Populated from JSON -->
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Work Experience</h2>
            <ul class="space-y-4">
                {% for job in experience %}
                <li class="interactive-card p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800 relative overflow-hidden">
                    <strong class="text-xl">{{ job.role }}</strong> at <span class="font-semibold">{{ job.company }}</span> - <span class="text-gray-600 dark:text-gray-400">{{ job.period }}</span><br>
                    <p class="mt-2">{{ job.details }}</p>
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Skills</h2>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                {% for skill in skills %}
                <div class="p-4 rounded shadow text-center
                            bg-gray-200 dark:bg-gray-700
                            text-gray-800 dark:text-gray-100">
                    {{ skill }}
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Projects</h2>
            <ul class="space-y-4">
                {% for project in projects %}
                <li class="interactive-card p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800 relative overflow-hidden">
                    <strong class="text-xl">{{ project.title }}</strong> - <span class="text-gray-600 dark:text-gray-400">{{ project.description }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <h2 class="text-3xl font-bold mb-4">Contact</h2>
            <p class="mb-6">Feel free to connect with me on social media!</p>
            <div class="space-x-6">
                <a href="{{ contact_info.github_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300"><i class="fab fa-github fa-2x"></i></a>
                <a href="{{ contact_info.linkedin_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300"><i class="fab fa-linkedin fa-2x"></i></a>
                <a href="{{ contact_info.bandcamp_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300"><i class="fab fa-bandcamp fa-2x"></i></a>
                <a href="{{ contact_info.kofi_url }}" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300"><i class="fa fa-coffee fa-2x"></i></a> <!-- Changed to fa-coffee -->
            </div>
            <p class="mt-6 text-sm text-gray-500 dark:text-gray-400">&copy; 2025 Your Name</p>
        </div>
    </section>

</body>
</html>
"""


@app.route("/")
def index():
    data = load_data()
    return render_template_string(template,
                                  website_title=data.get("website_title", "Developer Portfolio"),
                                  about_me=data.get("about_me", "Hello! I'm a software developer..."),
                                  projects=data["projects"],
                                  experience=data["experience"],
                                  skills=data["skills"],
                                  contact_info=data.get("contact_info", {"github_url": "#", "linkedin_url": "#", "bandcamp_url": "#", "kofi_url": "#"})) # Pass contact info


def write_static_html():
    data = load_data()
    rendered = render_template_string(template,
                                      website_title=data.get("website_title", "Developer Portfolio"),
                                      about_me=data.get("about_me", "Hello! I'm a software developer..."),
                                      projects=data["projects"],
                                      experience=data["experience"],
                                      skills=data["skills"],
                                      contact_info=data.get("contact_info", {"github_url": "#", "linkedin_url": "#", "bandcamp_url": "#", "kofi_url": "#"})) # Pass contact info
    os.makedirs("output", exist_ok=True)
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(rendered)


if __name__ == "__main__":
    with app.app_context():
        write_static_html()
    app.run(debug=True)
