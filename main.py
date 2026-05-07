from flask import Flask, render_template, send_from_directory, Response
import os
import json
import datetime
import platform
import subprocess
import re
import requests
import zipfile
import io
from urllib.parse import urljoin

app = Flask(__name__, static_url_path='', static_folder='output')


def fetch_latest_bandcamp_album(artist_url):
    """Fetch the latest album from a Bandcamp artist's discography page.
    Returns a dict with artwork_url (embed), music_url, and music_title,
    or None if fetching fails."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        # Get discography page — albums appear newest first
        resp = requests.get(artist_url.rstrip('/') + '/music', headers=headers, timeout=10)
        resp.raise_for_status()

        album_match = re.search(r'<a href="(/album/[^"]+)">', resp.text)
        if not album_match:
            return None

        album_path = album_match.group(1)
        album_url = artist_url.rstrip('/') + album_path

        # Get album page for embed ID and title
        resp = requests.get(album_url, headers=headers, timeout=10)
        resp.raise_for_status()

        id_match = re.search(
            r'<meta\s+name="bc-page-properties"\s+content="\{&quot;item_type&quot;:&quot;a&quot;,&quot;item_id&quot;:(\d+)',
            resp.text
        )
        if not id_match:
            return None
        album_id = id_match.group(1)

        title_match = re.search(r'<title>([^|]+)\|', resp.text)
        title = title_match.group(1).strip() if title_match else album_path.replace('/album/', '').replace('-', ' ').title()

        embed_url = (
            f"https://bandcamp.com/EmbeddedPlayer/album={album_id}"
            f"/size=large/bgcol=181a1b/linkcol=056cc4/tracklist=false/artwork=small/transparent=true/"
        )

        return {
            "artwork_url": embed_url,
            "music_url": album_url,
            "music_title": title,
        }
    except Exception as e:
        print(f"Warning: could not fetch latest Bandcamp album — {e}")
        return None


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
            "stats": [
                {"value": 5, "suffix": "+", "label": "Years Experience"},
                {"value": 25, "suffix": "+", "label": "Projects Shipped"},
                {"value": 10, "suffix": "+", "label": "Technologies"}
            ],
            # === NEW: Professional framing for the interactive section ===
            "sandbox_title": "Interactive UI Sandbox",
            "sandbox_description": "This interactive sandbox showcases a range of front-end development skills. The theme customization is built with CSS variables and managed via JavaScript's localStorage for state persistence. The section reordering utilizes the SortableJS library and direct DOM manipulation to provide a dynamic user experience, complete with keyboard accessibility.",
            "theme_colors": {
                "light": {
                    "background": "#f9fafb",
                    "text_primary": "#111827",
                    "text_secondary": "#4b5563",
                    "card_background": "#ffffff",
                    "accent": "#2563eb",
                    "accent_hover": "#1d4ed8",
                    "spotlight_color": "rgba(255, 255, 255, 0.2)"
                },
                "dark": {
                    "background": "#111827",
                    "text_primary": "#f9fafb",
                    "text_secondary": "#d1d5db",
                    "card_background": "#1f2937",
                    "accent": "#93c5fd",
                    "accent_hover": "#60a5fa",
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
                {"name": "Python", "icon": "fab fa-python", "proficiency": 92},
                {"name": "JavaScript", "icon": "fab fa-js", "proficiency": 85},
                {"name": "React", "icon": "fab fa-react", "proficiency": 78},
                {"name": "Node.js", "icon": "fab fa-node-js", "proficiency": 75},
                {"name": "Tailwind CSS", "icon": "fab fa-css3-alt", "proficiency": 88},
                {"name": "Flask", "icon": "fas fa-flask", "proficiency": 80},
                {"name": "SQL", "icon": "fas fa-database", "proficiency": 70},
                {"name": "Git", "icon": "fab fa-git-alt", "proficiency": 90},
                {"name": "Cloud Computing", "icon": "fas fa-cloud", "proficiency": 65}
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "description": "Validated expertise in designing distributed systems on AWS.",
                    "link": "https://aws.amazon.com/certification/",
                    "issuer_logo_url": "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg"
                },
                {
                    "name": "Professional Data Engineer",
                    "description": "Demonstrated proficiency in data processing systems and machine learning models.",
                    "link": "https://cloud.google.com/certification/data-engineer",
                    "issuer_logo_url": "https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg"
                },
                {
                    "name": "Meta Back-End Developer",
                    "description": "Comprehensive course covering Python, Django, APIs, and database management.",
                    "link": "https://www.coursera.org/",
                    "issuer_logo_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/Coursera-Logo_600x600.svg"
                }
            ],
            "contact_info": {
                "email": "you@example.com",
                "github_url": "https://github.com/yourusername",
                "linkedin_url": "https://linkedin.com/in/yourusername",
                "bandcamp_url": "https://yourusername.bandcamp.com",
                "kofi_url": "https://ko-fi.com/yourusername",
                "resume_url": "#"
            },
            "copyright_name": "Your Name",
            "copyright_start_year": 2024,
            "site_url": ""
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
        def _period_year(job):
            m = re.search(r'\b(19|20)\d{2}\b', job.get('period', '') or '')
            return int(m.group()) if m else 0
        sorted_experience = sorted(data["experience"], key=_period_year, reverse=True)
        for job in sorted_experience:
            if job["company"] != current_company:
                grouped_experience.append({"company": job["company"], "roles": []})
                current_company = job["company"]
            grouped_experience[-1]["roles"].append(
                {"role": job["role"], "period": job["period"], "details": job.get("details", "")})
    data["grouped_experience"] = grouped_experience

    # Flat sorted experience — one entry per role, company_start flags first role per company
    flat_experience = []
    prev_company = None
    for group in grouped_experience:
        for role in group["roles"]:
            flat_experience.append({
                "role": role["role"],
                "period": role["period"],
                "details": role.get("details", ""),
                "company": group["company"],
                "is_company_start": group["company"] != prev_company,
            })
            prev_company = group["company"]
    data["flat_experience"] = flat_experience

    # Generate dynamic copyright string
    start_year = data.get("copyright_start_year")
    current_year = datetime.datetime.now().year
    if start_year and start_year < current_year:
        data["copyright_string"] = f"{start_year} - {current_year}"
    else:
        data["copyright_string"] = str(current_year)

    # Compute absolute OG image URL
    site_url = data.get("site_url", "")
    hero_image = data.get("hero_image_url", "")
    if site_url and hero_image and not hero_image.startswith("http"):
        data["og_image_url"] = urljoin(site_url, hero_image)
    else:
        data["og_image_url"] = hero_image

    # Compute sameAs list for JSON-LD
    contact = data.get("contact_info", {})
    data["social_same_as"] = [
        v for k, v in contact.items()
        if k in ("github_url", "linkedin_url") and v
    ]

    # Fetch latest Bandcamp album (falls back to existing latest_music in JSON)
    bandcamp_url = contact.get("bandcamp_url", "")
    if bandcamp_url:
        latest = fetch_latest_bandcamp_album(bandcamp_url)
        if latest:
            data["latest_music"] = latest

    return data


@app.route("/")
def serve_index():
    data = load_data()
    return render_template('index.html', static_root="/static/", pdf_url="/resume.pdf", tailwind_mode="cdn", **data)


_FALLBACK_404_DATA = {
    "website_title": "Page Not Found",
    "theme_colors": {
        "light": {"background": "#f9fafb", "text_primary": "#111827", "text_secondary": "#4b5563", "card_background": "#ffffff", "accent": "#2563eb", "accent_hover": "#1d4ed8"},
        "dark":  {"background": "#111827", "text_primary": "#f9fafb", "text_secondary": "#d1d5db", "card_background": "#1f2937", "accent": "#93c5fd", "accent_hover": "#60a5fa"},
    },
}


@app.errorhandler(404)
def not_found(e):
    try:
        data = load_data()
    except Exception as ex:
        print(f"404 handler: load_data failed — {ex}")
        data = _FALLBACK_404_DATA
    return render_template('404.html', static_root="/static/", tailwind_mode="cdn", **data), 404


@app.route("/resume.pdf")
def serve_resume():
    from resume import generate_pdf, _load_data
    data = _load_data()
    pdf_bytes = generate_pdf(data)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": "inline; filename=resume.pdf"},
    )


@app.route('/<path:path>')
def serve_static_root(path):
    return send_from_directory('output', path)


_TAILWIND_VERSION = "v3.4.17"
_TAILWIND_BINARIES = {
    ("windows", "amd64"): "tailwindcss-windows-x64.exe",
    ("windows", "arm64"): "tailwindcss-windows-arm64.exe",
    ("darwin",  "arm64"): "tailwindcss-macos-arm64",
    ("darwin",  "amd64"): "tailwindcss-macos-x64",
    ("linux",   "amd64"): "tailwindcss-linux-x64",
    ("linux",   "arm64"): "tailwindcss-linux-arm64",
}

def _get_tailwind_cli(static_dir):
    """Download the Tailwind standalone CLI if not already present; return its path."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    # Normalise arm variants
    if "arm" in machine or "aarch" in machine:
        arch = "arm64"
    else:
        arch = "amd64"
    binary_name = _TAILWIND_BINARIES.get((system, arch))
    if not binary_name:
        raise RuntimeError(f"No Tailwind CLI binary for {system}/{arch}")
    local_name = "tailwindcss.exe" if system == "windows" else "tailwindcss"
    cli_path = os.path.join(static_dir, local_name)
    if not os.path.exists(cli_path):
        url = f"https://github.com/tailwindlabs/tailwindcss/releases/download/{_TAILWIND_VERSION}/{binary_name}"
        print(f"Downloading Tailwind CLI {_TAILWIND_VERSION}...")
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(cli_path, "wb") as f:
            f.write(resp.content)
        if system != "windows":
            os.chmod(cli_path, 0o755)
        print("Downloaded Tailwind CLI.")
    return cli_path


def _build_tailwind_css(cli_path, content_html_paths, output_css_path):
    """Run the Tailwind CLI to generate a purged, minified CSS file.
    content_html_paths can be a single path or a list of paths."""
    if isinstance(content_html_paths, str):
        content_html_paths = [content_html_paths]
    abs_paths = [os.path.abspath(p) for p in content_html_paths]
    config_js = os.path.join(os.path.dirname(output_css_path), "_tailwind_config.js")
    input_css = os.path.join(os.path.dirname(output_css_path), "_tailwind_input.css")
    try:
        with open(config_js, "w", encoding="utf-8") as f:
            f.write(f"""module.exports = {{
  darkMode: 'class',
  content: {json.dumps(abs_paths)},
  theme: {{
    extend: {{
      fontFamily: {{ sans: ['Inter', 'sans-serif'], heading: ['Poppins', 'sans-serif'] }},
      keyframes: {{ flash: {{ '0%, 100%': {{ backgroundColor: 'transparent' }}, '50%': {{ backgroundColor: 'rgba(59, 130, 246, 0.2)' }} }} }},
      animation: {{ flash: 'flash 1s ease-in-out' }},
    }},
  }},
}}
""")
        with open(input_css, "w", encoding="utf-8") as f:
            f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
        result = subprocess.run(
            [cli_path, "-i", input_css, "-o", output_css_path, "--config", config_js, "--minify"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        print(f"Built tailwind.css ({os.path.getsize(output_css_path) // 1024} KB).")
        return True
    finally:
        for p in (config_js, input_css):
            try:
                os.remove(p)
            except OSError:
                pass


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

    # --- Tailwind CSS build ---
    # Step 1: render with CDN mode so all class names are in the HTML for scanning
    scan_html_path = os.path.join(output_dir, "_scan.html")
    scan_404_path = os.path.join(output_dir, "_scan_404.html")
    scan_html = render_template('index.html', static_root="static/", pdf_url="resume.pdf", tailwind_mode="cdn", **data)
    scan_404 = render_template('404.html', static_root="static/", tailwind_mode="cdn", **data)
    with open(scan_html_path, "w", encoding="utf-8") as f:
        f.write(scan_html)
    with open(scan_404_path, "w", encoding="utf-8") as f:
        f.write(scan_404)

    tailwind_css_path = os.path.join(static_dir, "tailwind.css")
    tailwind_mode = "cdn"
    try:
        cli_path = _get_tailwind_cli(static_dir)
        _build_tailwind_css(cli_path, [scan_html_path, scan_404_path], tailwind_css_path)
        tailwind_mode = "built"
    except Exception as e:
        print(f"Tailwind CLI build failed, falling back to CDN bundle: {e}")
    finally:
        for p in (scan_html_path, scan_404_path):
            try:
                os.remove(p)
            except OSError:
                pass

    # Step 2: render final HTML with the determined tailwind_mode
    rendered_for_file = render_template('index.html', static_root="static/", pdf_url="resume.pdf", tailwind_mode=tailwind_mode, **data)
    rendered_404 = render_template('404.html', static_root="static/", tailwind_mode=tailwind_mode, **data)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(rendered_for_file)
    with open(os.path.join(output_dir, "404.html"), "w", encoding="utf-8") as f:
        f.write(rendered_404)

    # Export resume PDF
    try:
        from resume import generate_pdf
        pdf_bytes = generate_pdf(data)
        pdf_path = os.path.join(output_dir, "resume.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        print("resume.pdf written to output/")
    except Exception as e:
        print(f"Warning: could not generate resume.pdf — {e}")


if __name__ == "__main__":
    with app.app_context():
        write_static_html()
        print(f"Static HTML file and assets generated in 'output/' directory.")

    print("Starting development server at http://localhost:5000")
    app.run(debug=True)
