import datetime
import os
from flask import Flask, render_template_string
import json

app = Flask(__name__)

# The HTML, CSS, and JavaScript are combined here.
# I've implemented the visual enhancements and the new synth section.
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
      --synth-active-step: rgba(193, 161, 255, 0.8);
      --synth-step-bg: rgba(255, 255, 255, 0.1);
      --synth-step-hover: rgba(255, 255, 255, 0.2);
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
      cursor: none; /* Hide default cursor to replace with custom one */
    }

    /* --- NEW: Aurora Background Glow --- */
    body::before {
      content: '';
      position: fixed;
      top: 50%;
      left: 50%;
      width: 80vw;
      height: 80vh;
      background: radial-gradient(circle, rgba(193, 161, 255, 0.1) 0%, rgba(193, 161, 255, 0) 70%);
      transform: translate(-50%, -50%);
      animation: slow-spin 25s linear infinite;
      z-index: -1;
    }

    /* --- Vanta.js Animated Background --- */
    #vanta-bg {
      position: fixed;
      top: 0; left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -2; /* Pushed back behind the aurora */
    }

    /* --- NEW: Interactive Cursor Glow --- */
    .cursor-glow {
      position: fixed;
      top: 0;
      left: 0;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--accent-color);
      pointer-events: none;
      transform: translate(-50%, -50%);
      z-index: 9999;
      filter: blur(15px);
      opacity: 0;
      transition: opacity 0.4s ease, transform 0.1s ease-out;
    }
    body:hover .cursor-glow {
        opacity: 0.5;
    }
    .cursor-point {
        position: fixed;
        top: 0;
        left: 0;
        width: 6px;
        height: 6px;
        background-color: var(--soft-white);
        border-radius: 50%;
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 9999;
        transition: transform 0.2s ease-out;
    }
    a:hover ~ .cursor-point, a:hover ~ .cursor-glow, .synth-control button:hover ~ .cursor-point, .synth-control button:hover ~ .cursor-glow {
        transform: translate(-50%, -50%) scale(2.5);
    }


    /* --- Sticky Navigation Bar --- */
    .sticky-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 15px 20px;
        z-index: 100;
        background: rgba(14, 15, 44, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        display: flex;
        justify-content: center;
        align-items: center;
        transform: translateY(-100%);
        transition: transform 0.4s ease-in-out;
    }

    .sticky-nav.visible {
        transform: translateY(0);
    }

    .nav-links {
        display: flex;
        gap: 30px;
        list-style: none;
    }

    .nav-links a {
        color: var(--soft-white);
        text-decoration: none;
        font-weight: 400;
        font-size: 1rem;
        transition: color 0.3s ease, text-shadow 0.3s ease;
    }

    .nav-links a:hover {
        color: var(--accent-color);
        text-shadow: 0 0 8px var(--accent-glow);
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
      font-size: clamp(3rem, 10vw, 6rem);
      font-weight: 600;
      text-shadow: 0 0 20px var(--accent-glow);
      /* UPDATED: Floating animation */
      animation: fadeIn 2s ease-in-out, float 8s ease-in-out 2s infinite;
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
      padding: clamp(20px, 5vw, 40px);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid var(--glass-border);
      /* UPDATED: Softer, more diffused shadow */
      box-shadow: 0 15px 45px -5px var(--accent-glow);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px -5px rgba(193, 161, 255, 0.4);
    }

    /* --- Section Styling --- */
    .section {
      padding: 100px 20px;
      max-width: 900px;
      margin: 0 auto;
    }

    /* UPDATED: Gradient text for all h1 and h2 headers */
    h1, .section h2 {
      font-family: 'Playfair Display', serif;
      letter-spacing: 1.5px; /* Airy letter spacing */
      background: linear-gradient(120deg, var(--accent-color), var(--soft-white));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-fill-color: transparent;
    }

    .section h2 {
      font-size: clamp(2rem, 6vw, 2.8rem);
      margin-bottom: 30px;
      text-align: center;
    }

    /* UPDATED: Subtle text shadow for readability */
    p {
        line-height: 1.7;
        font-weight: 300;
        text-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
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

    .artist-image-container {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        overflow: hidden;
        justify-self: center;
        box-shadow: 0 0 25px var(--accent-glow);
        border: 2px solid var(--glass-border);
    }

    .artist-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* --- Music Section --- */
    .music-grid {
        display: flex;
        flex-direction: column;
        gap: 30px;
        margin-top: 40px;
    }

    .music-item {
        color: var(--text-color);
        display: flex;
        flex-direction: column;
        gap: 15px;
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }

    .scroll-animate.in-view .music-item {
        opacity: 1;
        transform: translateY(0);
    }

    .music-embed-item {
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
    }

    .music-embed-item iframe {
        width: 100%;
        height: 120px;
        border: none;
        display: block;
    }

    /* --- UPDATED: Synth Section --- */
    #synth-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .synth-controls {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px 25px;
        margin-bottom: 20px;
    }
    .synth-control {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    .synth-control label {
        font-size: 0.9rem;
        font-weight: 300;
    }
    .synth-control button, .synth-control input[type="range"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        color: var(--text-color);
        padding: 10px 15px;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        transition: background 0.3s, box-shadow 0.3s;
    }
    .synth-control button:hover {
        background: var(--synth-step-hover);
        box-shadow: 0 0 10px var(--accent-glow);
    }
    .synth-control input[type="range"] {
        -webkit-appearance: none;
        appearance: none;
        width: 120px;
        height: 5px;
        background: var(--glass-border);
        outline: none;
        border-radius: 5px;
        padding: 0;
    }
    .synth-control input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 15px;
        height: 15px;
        background: var(--accent-color);
        cursor: pointer;
        border-radius: 50%;
    }
    .synth-control input[type="range"]::-moz-range-thumb {
        width: 15px;
        height: 15px;
        background: var(--accent-color);
        cursor: pointer;
        border-radius: 50%;
    }

    .sequencer {
        display: flex;
        flex-direction: column;
        gap: 15px;
        width: 100%;
        overflow-x: auto;
        padding: 10px;
        border: 1px solid var(--glass-border);
        border-radius: 8px;
    }
    .instrument-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .instrument-label {
        font-weight: 600;
        width: 80px;
        text-align: right;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .step-grid {
        display: grid;
        grid-template-columns: repeat(16, 1fr);
        gap: 5px;
        min-width: 500px;
    }
    .step {
        width: 100%;
        padding-bottom: 100%; /* Aspect ratio 1:1 */
        background: var(--synth-step-bg);
        border: 1px solid var(--glass-border);
        border-radius: 4px;
        transition: background-color 0.1s;
        cursor: pointer;
    }
    .step:hover {
        background: var(--synth-step-hover);
    }
    .step.active {
        background: var(--accent-color);
        box-shadow: 0 0 8px var(--accent-glow);
    }
    .step.current {
        outline: 2px solid var(--synth-active-step);
        outline-offset: 2px;
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
        transition: transform 0.3s ease, color 0.3s ease;
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

    @keyframes float {
      0%, 100% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-10px);
      }
    }

    @keyframes slow-spin {
      from { transform: translate(-50%, -50%) rotate(0deg); }
      to { transform: translate(-50%, -50%) rotate(360deg); }
    }

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

  <div id="vanta-bg"></div>
  <div class="cursor-glow"></div>
  <div class="cursor-point"></div>

  <nav class="sticky-nav">
    <ul class="nav-links">
        <li><a href="#about">About</a></li>
        <li><a href="#music">Music</a></li>
        <li><a href="#create">Create</a></li>
        <li><a href="#contact">Contact</a></li>
    </ul>
  </nav>

  <div class="content-wrapper">
    <header class="hero">
      <h1>{{ artist_name }}</h1>
      <a href="#about" class="scroll-down">
        <span>Discover More</span>
        <i data-feather="arrow-down" width="20" height="20"></i>
      </a>
    </header>

    <main>
      <section id="about" class="section scroll-animate">
        <div class="glass-card">
          <h2>About The Artist</h2>
          <div class="about-content">
            <p>{{ artist_about }}</p>
            <div class="artist-image-container">
                <img src="{{ artist_image }}" alt="A photo of {{ artist_name }}" class="artist-image" onerror="this.parentElement.style.display='none'">
            </div>
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

      <section id="all-music" class="section scroll-animate">
        <div class="glass-card">
            <h2>More Music</h2>
            <div class="music-grid">
                {% for music in all_music %}
                <div class="music-item">
                    <div class="music-embed-item">
                        <iframe src="{{ music.artwork_url }}" seamless><a href="{{ music.music_url }}">{{ music.music_title }}</a></iframe>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
      </section>

      <!-- UPDATED: Synth Section -->
      <section id="create" class="section scroll-animate">
        <div class="glass-card">
          <h2>Create A Melody</h2>
          <p style="text-align:center; margin-bottom: 30px;">Click the grid to make a simple tune. Press play to hear your creation.</p>
          <div id="synth-container">
            <div class="synth-controls">
              <div class="synth-control">
                <button id="play-stop-btn">Play</button>
              </div>
              <div class="synth-control">
                <label for="tempo-slider">Tempo: <span id="tempo-value">120</span> BPM</label>
                <input type="range" id="tempo-slider" min="60" max="180" value="120">
              </div>
               <div class="synth-control">
                <label for="reverb-slider">Reverb</label>
                <input type="range" id="reverb-slider" min="0" max="1" step="0.05" value="0.2">
              </div>
              <div class="synth-control">
                <label for="delay-slider">Delay</label>
                <input type="range" id="delay-slider" min="0" max="1" step="0.05" value="0.1">
              </div>
              <div class="synth-control">
                  <button id="randomize-btn">Randomize</button>
              </div>
              <div class="synth-control">
                  <button id="clear-btn">Clear</button>
              </div>
            </div>
            <div class="sequencer">
              <!-- Grid will be generated by JS -->
            </div>
          </div>
        </div>
      </section>

      <section id="contact" class="section scroll-animate">
        <div class="glass-card">
            <div class="content">
                <h2>Get In Touch</h2>
                <p>For bookings, collaborations, or other inquiries, please reach out via email.</p>
                <p><a href="mailto:{{ artist_contact_email }}">{{ artist_contact_email }}</a></p>
                <div class="social-links">
                    <a href="{{ artist_links.bandcamp }}" target="_blank" aria-label="Bandcamp"><i data-feather="music"></i></a>
                    <a href="{{ artist_links.spotify }}" target="_blank" aria-label="Spotify"><i data-feather="headphones"></i></a>
                    <a href="{{ artist_links.instagram }}" target="_blank" aria-label="Instagram"><i data-feather="instagram"></i></a>
                    <a href="{{ artist_links.twitter }}" target="_blank" aria-label="Twitter"><i data-feather="twitter"></i></a>
                    <a href="{{ artist_links.kofi }}" target="_blank" aria-label="Ko-fi"><i data-feather="coffee"></i></a>
                </div>
            </div>
        </div>
      </section>
    </main>

    <footer>
      &copy; {{ copyright_string }} {{ artist_name }}. All rights reserved.
    </footer>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.fog.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.7.77/Tone.js"></script>

  <script>
    // --- Vanta.js Initialization ---
    VANTA.FOG({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      highlightColor: 0x8d80b5,
      midtoneColor: 0x8b6bad,
      lowlightColor: 0x3c3c8c,
      baseColor: 0x0e0f2c,
      blurFactor: 0.60,
      speed: 1.20,
      zoom: 0.80
    });

    // --- Feather Icons Initialization ---
    feather.replace();

    // --- Scroll Animation Logic ---
    const scrollElements = document.querySelectorAll(".scroll-animate");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          const listItems = entry.target.querySelectorAll('.music-item');
          if (listItems.length > 0) {
            listItems.forEach((item, index) => {
              item.style.transitionDelay = `${index * 150}ms`;
            });
          }
        }
      });
    }, {
      threshold: 0.1
    });
    scrollElements.forEach(el => observer.observe(el));

    // --- Sticky Nav Logic ---
    const nav = document.querySelector('.sticky-nav');
    const heroHeader = document.querySelector('.hero');
    const navObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                nav.classList.add('visible');
            } else {
                nav.classList.remove('visible');
            }
        });
    }, { rootMargin: `-${heroHeader.offsetHeight - 1}px 0px 0px 0px` });
    navObserver.observe(heroHeader);

    // --- Interactive Cursor Logic ---
    const cursorGlow = document.querySelector('.cursor-glow');
    const cursorPoint = document.querySelector('.cursor-point');
    document.addEventListener('mousemove', (e) => {
      cursorGlow.style.left = `${e.clientX}px`;
      cursorGlow.style.top = `${e.clientY}px`;
      cursorPoint.style.left = `${e.clientX}px`;
      cursorPoint.style.top = `${e.clientY}px`;
    });

    // --- UPDATED: Synthesizer Logic with Tone.js ---
    document.addEventListener('DOMContentLoaded', () => {
        const sequencerContainer = document.querySelector('.sequencer');
        const playStopBtn = document.getElementById('play-stop-btn');
        const tempoSlider = document.getElementById('tempo-slider');
        const tempoValue = document.getElementById('tempo-value');
        const clearBtn = document.getElementById('clear-btn');
        const randomizeBtn = document.getElementById('randomize-btn');
        const reverbSlider = document.getElementById('reverb-slider');
        const delaySlider = document.getElementById('delay-slider');

        // Effects chain
        const reverb = new Tone.Reverb({ decay: 1.5, wet: 0.2 }).toDestination();
        const feedbackDelay = new Tone.FeedbackDelay("8n", 0.5).connect(reverb);

        const synths = {
            'Lead': new Tone.Synth({ oscillator: { type: 'triangle' }, envelope: { attack: 0.02, decay: 0.1, sustain: 0.3, release: 1 } }).connect(feedbackDelay),
            'Pad': new Tone.PolySynth(Tone.Synth, { oscillator: { type: 'sine' }, envelope: { attack: 0.5, decay: 0.1, sustain: 0.8, release: 1.2 } }).connect(feedbackDelay),
            'Bass': new Tone.MonoSynth({ oscillator: { type: 'fmsine' }, envelope: { attack: 0.01, decay: 0.3, sustain: 0.1, release: 0.8 } }).connect(feedbackDelay),
            'Hi-Hat': new Tone.MetalSynth({ frequency: 200, envelope: { attack: 0.001, decay: 0.1, release: 0.01 }, harmonicity: 5.1, modulationIndex: 32, resonance: 4000, octaves: 1.5 }).connect(feedbackDelay),
            'Drum': new Tone.MembraneSynth({ pitchDecay: 0.05, octaves: 10, oscillator: { type: 'sine' }, envelope: { attack: 0.001, decay: 0.4, sustain: 0.01, release: 1.4, attackCurve: 'exponential' } }).connect(feedbackDelay)
        };

        const notes = {
            'Lead': ['C5', 'D5', 'E5', 'G5', 'A5'],
            'Pad': [['C4', 'E4', 'G4'], ['D4', 'F4', 'A4']],
            'Bass': ['C3', 'D3', 'E3', 'G3', 'A3'],
            'Hi-Hat': ['C7'],
            'Drum': ['C2']
        };

        const numSteps = 16;
        let grid = {};

        // Generate the grid
        Object.keys(notes).forEach(instrument => {
            grid[instrument] = [];
            const instrumentNotes = notes[instrument];
            instrumentNotes.forEach(note => {
                const row = [];
                const instrumentRow = document.createElement('div');
                instrumentRow.classList.add('instrument-row');

                const label = document.createElement('div');
                label.classList.add('instrument-label');
                const noteLabel = Array.isArray(note) ? note.join('+') : note;
                label.textContent = `${instrument} (${noteLabel})`;
                instrumentRow.appendChild(label);

                const stepGrid = document.createElement('div');
                stepGrid.classList.add('step-grid');

                for (let i = 0; i < numSteps; i++) {
                    const step = document.createElement('div');
                    step.classList.add('step');
                    step.dataset.step = i;
                    step.dataset.note = JSON.stringify(note); // Store note as string
                    step.dataset.instrument = instrument;
                    step.addEventListener('click', () => {
                        step.classList.toggle('active');
                    });
                    stepGrid.appendChild(step);
                    row.push(step);
                }
                instrumentRow.appendChild(stepGrid);
                sequencerContainer.appendChild(instrumentRow);
                grid[instrument].push(row);
            });
        });

        let sequence = new Tone.Sequence((time, col) => {
            // Update current step visual
            document.querySelectorAll('.step').forEach(s => s.classList.remove('current'));
            document.querySelectorAll(`.step[data-step='${col}']`).forEach(s => s.classList.add('current'));

            Object.keys(grid).forEach(instrument => {
                grid[instrument].forEach(row => {
                    const step = row[col];
                    if (step.classList.contains('active')) {
                        const noteToPlay = JSON.parse(step.dataset.note);
                        synths[instrument].triggerAttackRelease(noteToPlay, '8n', time);
                    }
                });
            });
        }, Array.from(Array(numSteps).keys()), '16n').start(0);

        // Controls
        playStopBtn.addEventListener('click', async () => {
            await Tone.start();
            if (Tone.Transport.state === 'started') {
                Tone.Transport.stop();
                playStopBtn.textContent = 'Play';
            } else {
                Tone.Transport.start();
                playStopBtn.textContent = 'Stop';
            }
        });

        tempoSlider.addEventListener('input', (e) => {
            Tone.Transport.bpm.value = e.target.value;
            tempoValue.textContent = e.target.value;
        });

        reverbSlider.addEventListener('input', (e) => {
            reverb.wet.value = e.target.value;
        });

        delaySlider.addEventListener('input', (e) => {
            feedbackDelay.wet.value = e.target.value;
        });

        clearBtn.addEventListener('click', () => {
            document.querySelectorAll('.step.active').forEach(s => s.classList.remove('active'));
        });

        randomizeBtn.addEventListener('click', () => {
            document.querySelectorAll('.step').forEach(s => {
                s.classList.toggle('active', Math.random() > 0.8);
            });
        });

        // Set initial tempo & effects
        Tone.Transport.bpm.value = 120;
        reverb.wet.value = 0.2;
        feedbackDelay.wet.value = 0.1;
    });

  </script>

</body>
</html>
'''


def load_data():
    # Create a dummy data file if it doesn't exist
    if not os.path.exists('website_data.json'):
        dummy_data = {
            "artist_name": "Etherea",
            "artist_icon": "https://placehold.co/32x32/0e0f2c/c1a1ff?text=E",
            "artist_about": "Etherea is a solo artist crafting ambient soundscapes that blend dreamy synthesizers with organic textures. Inspired by lucid dreams and foggy coastlines, the music invites listeners into a state of reflective tranquility. Each track is a journey through sound, designed to soothe the mind and stir the soul.",
            "artist_image": "https://placehold.co/400x400/1f1f3c/e6e6ff?text=Etherea",
            "artist_hero_image": "",
            "latest_music": {
                "music_title": "Crystal Caverns by Etherea",
                "music_url": "https://bandcamp.com",
                "artwork_url": "https://bandcamp.com/EmbeddedPlayer/track=123456789/size=large/bgcol=333333/linkcol=c1a1ff/tracklist=false/artwork=small/transparent=true/"
            },
            "all_music": [
                {
                    "music_title": "First Song by Etherea",
                    "music_url": "https://bandcamp.com",
                    "artwork_url": "https://bandcamp.com/EmbeddedPlayer/track=111111/size=large/bgcol=333333/linkcol=c1a1ff/tracklist=false/artwork=none/transparent=true/"
                },
                {
                    "music_title": "Second Song by Etherea",
                    "music_url": "https://bandcamp.com",
                    "artwork_url": "https://bandcamp.com/EmbeddedPlayer/track=222222/size=large/bgcol=333333/linkcol=c1a1ff/tracklist=false/artwork=none/transparent=true/"
                },
                {
                    "music_title": "Third Song by Etherea",
                    "music_url": "https://bandcamp.com",
                    "artwork_url": "https://bandcamp.com/EmbeddedPlayer/track=333333/size=large/bgcol=333333/linkcol=c1a1ff/tracklist=false/artwork=none/transparent=true/"
                }
            ],
            "artist_contact_email": "contact@ethereamusic.com",
            "contact_info": {
                "bandcamp": "https://bandcamp.com",
                "spotify": "https://spotify.com",
                "instagram": "https://instagram.com",
                "twitter": "https://twitter.com",
                "kofi": "https://ko-fi.com"
            },
            "copyright_start_year": 2023
        }
        with open('website_data.json', 'w') as f:
            json.dump(dummy_data, f, indent=4)

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
                                  all_music=data['all_music'],
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
    print("Static HTML exported to ./output/music/index.html")


@app.route('/')
def home():
    export_static_html()
    data = load_data()
    return render_html(data)


if __name__ == '__main__':
    # Ensure dummy data exists for local execution
    load_data()
    app.run(debug=True)
