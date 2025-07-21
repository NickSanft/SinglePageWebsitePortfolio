import datetime
import os
from flask import Flask, render_template_string
import json

app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- Using placeholders for template data -->
  <title>{{ artist_name }} | Official Website</title>
  <link rel="icon" href="{{ artist_icon }}">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
  
  <!-- Feather Icons for social links -->
  <script src="https://unpkg.com/feather-icons"></script>

  <style>
    /* --- Root Variables --- */
    :root {
      --bg-color: #0e0f2c;
      --primary-glow: #1f1f3c;
      --accent-color: #c1a1ff;
      --accent-glow: rgba(193, 161, 255, 0.25);
      --text-color: #e6e6ff;
      --soft-white: #f0f0ff;
      --glass-bg: rgba(255, 255, 255, 0.05);
      --glass-border: rgba(255, 255, 255, 0.1);
    }

    /* --- General Body & Reset --- */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Inter', sans-serif;
      color: var(--text-color);
      background-color: var(--bg-color); /* Fallback background */
      overflow-x: hidden;
    }

    /* --- Vanta.js Animated Background --- */
    #vanta-bg {
      position: fixed;
      top: 0; left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -1;
    }

    /* --- Main Content Container --- */
    .content-wrapper {
      position: relative;
      z-index: 1;
    }

    /* --- Hero Header Section --- */
    header.hero {
      height: 100vh; /* Full viewport height */
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      position: relative;
      padding: 20px;
    }

    header.hero h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(3rem, 10vw, 6rem); /* Responsive font size */
      font-weight: 600;
      color: var(--soft-white);
      text-shadow: 0 0 20px var(--accent-glow);
      animation: fadeIn 2s ease-in-out;
    }

    /* Scroll down indicator */
    .scroll-down {
        position: absolute;
        bottom: 40px;
        color: var(--soft-white);
        text-decoration: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        opacity: 0;
        animation: fadeIn 2s 1.5s ease-in-out forwards;
    }

    /* --- Glassmorphism Card Style --- */
    .glass-card {
      background: var(--glass-bg);
      border-radius: 16px;
      padding: clamp(20px, 5vw, 40px); /* Responsive padding */
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid var(--glass-border);
      box-shadow: 0 8px 32px 0 var(--accent-glow);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(193, 161, 255, 0.35);
    }

    /* --- Section Styling --- */
    .section {
      padding: 100px 20px;
      max-width: 900px;
      margin: 0 auto;
    }

    .section h2 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2rem, 6vw, 2.8rem);
      color: var(--accent-color);
      margin-bottom: 30px;
      text-align: center;
    }
    
    p {
        line-height: 1.7;
        font-weight: 300;
    }

    /* --- About Section Specifics --- */
    .about-content {
        display: grid;
        grid-template-columns: 1fr;
        gap: 40px;
        align-items: center;
    }

    @media (min-width: 768px) {
        .about-content {
            grid-template-columns: 2fr 1fr;
            text-align: left;
        }
    }

    .artist-image {
        width: 100%;
        max-width: 250px;
        height: auto;
        border-radius: 12px;
        justify-self: center;
        box-shadow: 0 0 25px var(--accent-glow);
    }

    /* --- Music Section --- */
    .music-embed {
      width: 100%;
      border-radius: 8px;
      overflow: hidden; /* Ensures the iframe corners are rounded */
    }

    .music-embed iframe {
      width: 100%;
      height: 160px;
      border: none;
    }

    /* --- Contact Section --- */
    .contact .content {
        text-align: center;
    }

    .contact p {
        margin-bottom: 20px;
    }

    .contact a {
      color: var(--accent-color);
      text-decoration: none;
      font-weight: 400;
      transition: color 0.3s ease, text-shadow 0.3s ease;
    }

    .contact a:hover {
      color: var(--soft-white);
      text-shadow: 0 0 10px var(--accent-glow);
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-top: 20px;
    }
    .social-links a {
        color: var(--text-color);
    }
    .social-links a:hover {
        color: var(--accent-color);
        transform: scale(1.1);
    }
    .social-links i {
        width: 28px;
        height: 28px;
    }

    /* --- Footer --- */
    footer {
      text-align: center;
      padding: 50px 20px;
      font-size: 0.9rem;
      color: #aaa;
    }

    /* --- Animations --- */
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    /* For scroll animations */
    .scroll-animate {
      opacity: 0;
      transform: translateY(30px);
      transition: opacity 0.8s ease-out, transform 0.8s ease-out;
    }

    .scroll-animate.in-view {
      opacity: 1;
      transform: translateY(0);
    }

  </style>
</head>
<body>
  
  <!-- Vanta.js background will attach here -->
  <div id="vanta-bg"></div>

  <div class="content-wrapper">
    <!-- 
      IMPROVEMENT: Full-screen hero header.
      This creates a more impactful and immersive first impression.
    -->
    <header class="hero">
      <h1>{{ artist_name }}</h1>
      <a href="#about" class="scroll-down">
        <span>Discover More</span>
        <i data-feather="arrow-down" width="20" height="20"></i>
      </a>
    </header>

    <main>
      <!-- 
        IMPROVEMENT: Scroll-triggered animations.
        The `scroll-animate` class is used by JavaScript to fade sections in
        as they enter the viewport, making the page feel more dynamic.
      -->
      <section id="about" class="section scroll-animate">
        <div class="glass-card">
          <h2>About The Artist</h2>
          <!-- 
            IMPROVEMENT: Better layout for content.
            Using CSS Grid to place the artist image alongside the text
            creates a more engaging and professional layout.
          -->
          <div class="about-content">
            <p>{{ artist_about }}</p>
            <img src="{{ artist_image }}" alt="A photo of {{ artist_name }}" class="artist-image" onerror="this.style.display='none'">
          </div>
        </div>
      </section>

      <section id="music" class="section scroll-animate">
        <div class="glass-card">
          <h2>Latest Music</h2>
          <div class="music-embed">
            <iframe style="border: 0; width: 100%; height: 120px;" src="{{ latest_music.artwork_url }}" seamless><a href="{{ latest_music.music_url }}">{{ latest_music.music_title }}</a></iframe>
          </div>
        </div>
      </section>

      <section id="contact" class="section scroll-animate">
        <div class="glass-card">
            <div class="content">
                <h2>Get In Touch</h2>
                <p>For bookings, collaborations, or other inquiries, please reach out via email.</p>
                <p><a href="mailto:{{ artist_contact_email }}">{{ artist_contact_email }}</a></p>
                
                <!-- 
                    IMPROVEMENT: Styled social media icons.
                    Using icons provides a clean, universally understood way to link
                    to social profiles, improving the UI.
                -->
                <div class="social-links">
                    <a href="{{ artist_links.bandcamp }}" target="_blank" aria-label="Bandcamp"><i data-feather="music"></i></a>
                    <a href="{{ artist_links.spotify }}" target="_blank" aria-label="Spotify"><i data-feather="headphones"></i></a>
                    <a href="{{ artist_links.instagram }}" target="_blank" aria-label="Instagram"><i data-feather="instagram"></i></a>
                    <a href="{{ artist_links.twitter }}" target="_blank" aria-label="Twitter"><i data-feather="twitter"></i></a>
                </div>
            </div>
        </div>
      </section>
    </main>

    <footer>
      &copy; {{ copyright_string }} {{ artist_name }}. All rights reserved.
    </footer>
  </div>

  <!-- Vanta.js and its dependency -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.fog.min.js"></script>
  
  <script>
    // --- Vanta.js Initialization ---
    // IMPROVEMENT: Tweaked Vanta.js settings for a more subtle and cohesive feel.
    // Colors are now more aligned with the CSS variable palette.
    VANTA.FOG({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      highlightColor: 0x8d80b5, // Was 0xaaffcc
      midtoneColor: 0x8b6bad,   // Was 0x44ffd9
      lowlightColor: 0x3c3c8c,  // Was 0x2255aa
      baseColor: 0x0e0f2c,
      blurFactor: 0.60,         // Slightly less blurry
      speed: 1.20,
      zoom: 0.80
    });

    // --- Feather Icons Initialization ---
    feather.replace();

    // --- Scroll Animation Logic ---
    // IMPROVEMENT: Using Intersection Observer for performant scroll animations.
    // This is more efficient than listening to every scroll event.
    const scrollElements = document.querySelectorAll(".scroll-animate");

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
        }
      });
    }, {
      threshold: 0.1 // Trigger when 10% of the element is visible
    });

    scrollElements.forEach(el => observer.observe(el));
  </script>

</body>
</html>
'''

def load_data():
    with open('website_data.json', 'r') as f:
        data = json.load(f)

    start_year = data.get("copyright_start_year")
    current_year = datetime.datetime.now().year
    if start_year and start_year < current_year:
        data["copyright_string"] = f"{start_year} - {current_year}"
    else:
        data["copyright_string"] = str(current_year)
    return data

def render_html(data):
    return render_template_string(html,
        artist_name=data['artist_name'],
        artist_about=data['artist_about'],
        latest_music=data['latest_music'],
        artist_hero_image=data['artist_hero_image'],
        artist_contact_email=data['artist_contact_email'],
        artist_links=data['contact_info'],
        artist_image=data['artist_image'],
        artist_icon=data['artist_icon'],
        copyright_string=data.get('copyright_string')
    )

def export_static_html():
    data = load_data()
    rendered = render_html(data)
    output_dir = os.path.join("output", "music")
    os.makedirs(output_dir, exist_ok=True)
    with open("./output/music/index.html", "w", encoding="utf-8") as f:
        f.write(rendered)
    print("Static HTML exported to index.html")

@app.route('/')
def home():
    export_static_html()
    data = load_data()
    return render_html(data)

if __name__ == '__main__':
    app.run(debug=True)
