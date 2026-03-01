from flask import Flask, render_template, send_from_directory
import os
import json
import datetime
import requests
import zipfile
import io

app = Flask(__name__, static_url_path='', static_folder='output')


# Load and process data from the external JSON file
def load_data():
    # Create a dummy website_data.json if it doesn't exist for demonstration
    if not os.path.exists("website_data.json"):
        dummy_data = {
            "website_title": "My Awesome Developer Portfolio",
            # === NEW: Replaced portfolio_name with an SVG logo ===
            "logo_svg": '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
            "hero_title": "Your Name",
            "hero_subtitle": "Software Developer | Python & JavaScript Enthusiast",
            "hero_image_url": "https://placehold.co/256x256/e0e0e0/333333?text=You",
            "about_me": "Hello! I'm a software developer with a passion for building clean and efficient solutions. I specialize in web development and enjoy working with Python, JavaScript, and modern front-end frameworks. My goal is to create impactful and user-friendly applications.",
            # === NEW: Professional framing for the interactive section ===
            "sandbox_title": "Interactive UI Sandbox",
            "sandbox_description": "This interactive sandbox showcases a range of front-end development skills. The theme customization is built with CSS variables and managed via JavaScript's localStorage for state persistence. The section reordering utilizes the SortableJS library and direct DOM manipulation to provide a dynamic user experience, complete with keyboard accessibility.",
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
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "description": "Validated expertise in designing distributed systems on AWS.",
                    "link": "https://aws.amazon.com/certification/"
                },
                {
                    "name": "Professional Data Engineer",
                    "description": "Demonstrated proficiency in data processing systems and machine learning models.",
                    "link": "https://cloud.google.com/certification/data-engineer"
                },
                {
                    "name": "Meta Back-End Developer",
                    "description": "Comprehensive course covering Python, Django, APIs, and database management.",
                    "link": "https://www.coursera.org/"
                }
            ],
            "contact_info": {
                "github_url": "https://github.com/yourusername",
                "linkedin_url": "https://linkedin.com/in/yourusername",
                "bandcamp_url": "https://yourusername.bandcamp.com",
                "kofi_url": "https://ko-fi.com/yourusername",
                "resume_url": "#"
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
        sorted_experience = sorted(data["experience"], key=lambda x: int(x['period'][:4]), reverse=True)
        for job in sorted_experience:
            if job["company"] != current_company:
                grouped_experience.append({"company": job["company"], "roles": []})
                current_company = job["company"]
            grouped_experience[-1]["roles"].append(
                {"role": job["role"], "period": job["period"], "details": job.get("details", "")})
    data["grouped_experience"] = grouped_experience

    # Generate dynamic copyright string
    start_year = data.get("copyright_start_year")
    current_year = datetime.datetime.now().year
    if start_year and start_year < current_year:
        data["copyright_string"] = f"{start_year} - {current_year}"
    else:
        data["copyright_string"] = str(current_year)

    return data


@app.route("/")
def serve_index():
    data = load_data()
    return render_template('index.html', static_root="/static/", **data)


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

    sortable_url = "https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"
    sortable_local_path = os.path.join(static_dir, "Sortable.min.js")
    if not os.path.exists(sortable_local_path):
        try:
            print("Downloading Sortable.min.js...")
            response = requests.get(sortable_url, timeout=10)
            response.raise_for_status()
            with open(sortable_local_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Successfully downloaded Sortable.min.js.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading Sortable.min.js: {e}")

    data = load_data()
    rendered_for_file = render_template('index.html', static_root="static/", **data)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(rendered_for_file)


if __name__ == "__main__":
    with app.app_context():
        write_static_html()
        print(f"Static HTML file and assets generated in 'output/' directory.")

    print("Starting development server at http://localhost:5000")
    app.run(debug=True)
