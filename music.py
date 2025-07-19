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
  <title>{{ artist_name }}</title>
  <link rel="icon" href="{{ artist_icon }}">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-color: #0e0f2c;
      --accent-color: #c1a1ff;
      --text-color: #ffffff;
      --soft-white: #dcdcff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', sans-serif;
      color: var(--text-color);
      background: linear-gradient(to bottom, #0e0f2c, #1f1f3c);
      overflow-x: hidden;
    }

    #vanta-bg {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100vh;
      z-index: -1;
    }

    header {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      position: relative;
    }

    header::after {
      content: '';
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
    }

    header h1 {
      font-family: 'Playfair Display', serif;
      font-size: 4rem;
      color: var(--soft-white);
      z-index: 1;
      position: relative;
    }

    .section {
      padding: 80px 20px;
      max-width: 900px;
      margin: 0 auto;
    }

    .section h2 {
      font-size: 2.5rem;
      color: var(--accent-color);
      margin-bottom: 20px;
    }

    .about, .music, .contact {
      background: rgba(255, 255, 255, 0.02);
      border-radius: 12px;
      padding: 40px;
      backdrop-filter: blur(8px);
      box-shadow: 0 0 20px rgba(193, 161, 255, 0.2);
    }

    .music iframe {
      width: 100%;
      height: 160px;
      border: none;
      border-radius: 8px;
    }

    footer {
      text-align: center;
      padding: 40px 20px;
      font-size: 0.9rem;
      color: #aaa;
    }
  </style>
</head>
<body>
  <div id="vanta-bg"></div>
  <header>
    <h1>{{ artist_name }}</h1>
  </header>

  <section class="section about">
    <h2>About</h2>
    <p>{{ artist_about }}</p>
  </section>

  <section class="section music">
    <h2>Latest Music</h2>
    <iframe style="border: 0; width: 100%; height: 120px;" src="https://bandcamp.com/EmbeddedPlayer/album=1491704455/size=large/bgcol=181a1b/linkcol=056cc4/tracklist=false/artwork=small/transparent=true/" seamless><a href="https://divora.bandcamp.com/album/origins-of-the-gyre-dnd-6">Origins Of The Gyre - DND 6 by Divora</a></iframe>
  </section>

  <section class="section contact">
    <h2>Contact</h2>
    <p>Email: <a href="mailto:{{ artist_contact_email }}" style="color: var(--accent-color);">{{ artist_contact_email }}</a></p>
    <p>Follow on:
      <a href="{{ artist_links.bandcamp }}" style="color: var(--accent-color);">Bandcamp</a>
    </p>
  </section>

  <footer>
    &copy; {{ copyright_string }} {{ artist_name }}. All rights reserved.
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.fog.min.js"></script>
  <script>
    VANTA.FOG({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      highlightColor: 0xaaffcc,
      midtoneColor: 0x44ffd9,
      lowlightColor: 0x2255aa,
      baseColor: 0x0e0f2c,
      blurFactor: 0.7,
      speed: 1.5,
      zoom: 0.85
    });
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
