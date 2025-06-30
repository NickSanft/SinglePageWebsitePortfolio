from flask import Flask, render_template_string
import os
import json

app = Flask(__name__)


# Load data from external JSON file
def load_data():
    # Create a dummy website_data.json if it doesn't exist for demonstration
    if not os.path.exists("website_data.json"):
        dummy_data = {
            "projects": [
                {"title": "Project Alpha", "description": "A web application built with React and Node.js."},
                {"title": "Project Beta", "description": "Mobile app development using Flutter."},
                {"title": "Project Gamma", "description": "Data analysis project with Python and Pandas."}
            ],
            "experience": [
                {"role": "Software Engineer", "period": "Jan 2022 - Present",
                 "details": "Developed and maintained web services using Python and Django."},
                {"role": "Junior Developer", "period": "Jul 2020 - Dec 2021",
                 "details": "Assisted in front-end development with HTML, CSS, and JavaScript."}
            ],
            "skills": [
                "Python", "JavaScript", "React", "Node.js", "Tailwind CSS", "Flask", "SQL", "Git", "Cloud Computing"
            ]
        }
        with open("website_data.json", "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=4)

    with open("website_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


# Tailwind CSS with Dark Mode and theme toggle logic + interactive animated background
template = """
<!DOCTYPE html>
<html lang="en"> <!-- Removed hardcoded 'dark' class -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Developer Portfolio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class' // Ensure Tailwind is configured for class-based dark mode
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

        // Variable to hold the mousemove event listener function
        let mouseMoveListener = null;

        // Function to apply/remove the mousemove effect
        function applyMouseMoveEffect(enable) {
            const bg = document.getElementById('background-effect');
            if (enable) {
                if (!mouseMoveListener) { // Only add if not already added
                    mouseMoveListener = function(event) {
                        const x = event.clientX;
                        const y = event.clientY;
                        bg.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(59,130,246,0.15), transparent 60%)`;
                    };
                    document.addEventListener('mousemove', mouseMoveListener);
                }
            } else {
                if (mouseMoveListener) { // Only remove if exists
                    document.removeEventListener('mousemove', mouseMoveListener);
                    mouseMoveListener = null;
                    bg.style.background = 'none'; // Clear background when disabled
                }
            }
        }

        // Function to toggle mousemove effect and save preference to localStorage
        function toggleMouseMoveEffect() {
            const isEnabled = localStorage.getItem('mouseEffect') !== 'disabled';
            if (isEnabled) {
                applyMouseMoveEffect(false);
                localStorage.setItem('mouseEffect', 'disabled');
            } else {
                applyMouseMoveEffect(true);
                localStorage.setItem('mouseEffect', 'enabled');
            }
            // Update button text
            updateMouseMoveButtonText();
        }

        // Function to update the mousemove button text
        function updateMouseMoveButtonText() {
            const button = document.getElementById('toggle-mouse-effect-button');
            if (button) {
                const isEnabled = localStorage.getItem('mouseEffect') !== 'disabled';
                button.textContent = isEnabled ? 'Disable Mouse Effect' : 'Enable Mouse Effect';
            }
        }


        // On page load, apply theme and mouse effect based on localStorage or system preference
        document.addEventListener('DOMContentLoaded', () => {
            // Apply theme
            if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }

            // Apply mouse effect
            const storedMouseEffect = localStorage.getItem('mouseEffect');
            if (storedMouseEffect === 'disabled') {
                applyMouseMoveEffect(false);
            } else {
                // Default to enabled if no preference or 'enabled'
                applyMouseMoveEffect(true);
            }
            // Update button text after initial load
            updateMouseMoveButtonText();
        });
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        html {
            scroll-behavior: smooth;
        }
        .background-effect {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
            transition: background 0.1s ease-out; /* Smooth transition for background effect */
        }
    </style>
</head>
<body class="bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans">
    <div class="background-effect" id="background-effect"></div>

    <!-- Theme and Mouse Effect Toggles -->
    <div class="fixed top-4 right-4 z-50 flex space-x-2">
        <button
            onclick="toggleTheme()"
            class="px-4 py-2 rounded shadow transition-colors duration-300
                   bg-gray-200 text-gray-800
                   dark:bg-gray-700 dark:text-gray-100
                   hover:bg-gray-300 dark:hover:bg-gray-600">
            Toggle Theme
        </button>
        <button
            id="toggle-mouse-effect-button"
            onclick="toggleMouseMoveEffect()"
            class="px-4 py-2 rounded shadow transition-colors duration-300
                   bg-gray-200 text-gray-800
                   dark:bg-gray-700 dark:text-gray-100
                   hover:bg-gray-300 dark:hover:bg-gray-600">
            <!-- Button text will be set by JavaScript -->
        </button>
    </div>

    <!-- Navigation Bar -->
    <nav class="sticky top-0 bg-gray-900 text-white shadow z-40">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="#" class="text-2xl font-bold">MyPortfolio</a>
            <div class="space-x-6">
                <a href="#about" class="hover:text-gray-300">About</a>
                <a href="#experience" class="hover:text-gray-300">Experience</a>
                <a href="#skills" class="hover:text-gray-300">Skills</a>
                <a href="#projects" class="hover:text-gray-300">Projects</a>
                <a href="#contact" class="hover:text-gray-300">Contact</a>
            </div>
        </div>
    </nav>

    <!-- About Section -->
    <section id="about" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">About Me</h2>
            <p class="text-lg">Hello! I'm a software developer with a passion for building clean and efficient solutions...</p>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-20">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-3xl font-bold mb-4">Work Experience</h2>
            <ul class="space-y-4">
                {% for job in experience %}
                <li class="p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800">
                    <strong class="text-xl">{{ job.role }}</strong> - <span class="text-gray-600 dark:text-gray-400">{{ job.period }}</span><br>
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
                <li class="p-4 rounded-lg shadow-md bg-gray-100 dark:bg-gray-800">
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
                <a href="https://github.com/yourusername" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300"><i class="fab fa-github fa-2x"></i></a>
                <a href="https://linkedin.com/in/yourusername" class="text-gray-700 dark:text-white hover:text-blue-500 dark:hover:text-blue-400 transition-colors duration-300"><i class="fab fa-linkedin fa-2x"></i></a>
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
    return render_template_string(template, projects=data["projects"], experience=data["experience"],
                                  skills=data["skills"])


def write_static_html():
    data = load_data()
    rendered = render_template_string(template, projects=data["projects"], experience=data["experience"],
                                      skills=data["skills"])
    os.makedirs("output", exist_ok=True)
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(rendered)


if __name__ == "__main__":
    with app.app_context():
        write_static_html()
    app.run(debug=True)
