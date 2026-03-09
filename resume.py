"""
resume.py — Generate a PDF resume from website_data.json using fpdf2.

Usage:
    python resume.py              -> writes output/resume.pdf
    generate_pdf(data) -> bytes   -> call from Flask route
"""

import os
import json
import datetime
from fpdf import FPDF, XPos, YPos


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_data():
    """Load and pre-process website_data.json (mirrors main.py logic)."""
    with open("website_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Group experience by company, sorted newest-first
    grouped_experience = []
    if "experience" in data:
        current_company = None
        sorted_exp = sorted(data["experience"], key=lambda x: int(x["period"][:4]), reverse=True)
        for job in sorted_exp:
            if job["company"] != current_company:
                grouped_experience.append({"company": job["company"], "roles": []})
                current_company = job["company"]
            grouped_experience[-1]["roles"].append({
                "role": job["role"],
                "period": job["period"],
                "details": job.get("details", ""),
            })
    data["grouped_experience"] = grouped_experience

    projects = data.get("projects", [])
    data["featured_project"] = next((p for p in projects if p.get("featured")), None)
    data["other_projects"] = [p for p in projects if not p.get("featured")]

    return data


# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------

class ResumePDF(FPDF):
    """A clean, single-column resume PDF."""

    ACCENT = (59, 130, 246)      # blue-500
    TEXT   = (17, 24, 39)        # gray-900
    MUTED  = (75, 85, 99)        # gray-600
    RULE   = (209, 213, 219)     # gray-300

    def __init__(self):
        super().__init__()
        self.set_margins(18, 16, 18)
        self.set_auto_page_break(auto=True, margin=16)

    # --- Section heading -------------------------------------------------

    def section_heading(self, title: str):
        self.ln(5)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 6, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Ruled line
        self.set_draw_color(*self.RULE)
        self.set_line_width(0.3)
        self.line(self.get_x(), self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)
        self.set_text_color(*self.TEXT)

    # --- Body text -------------------------------------------------------

    def body(self, text: str, size: int = 9):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*self.TEXT)
        self.multi_cell(0, 4.5, text)

    def muted_cell(self, text: str, size: float = 8.5, indent: float = 0):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*self.MUTED)
        if indent:
            self.set_x(self.l_margin + indent)
        self.multi_cell(0, 4, text)


def _build_contact_line(data: dict) -> str:
    """Assemble a compact contact string from available URLs."""
    ci = data.get("contact_info", {})
    parts = []
    if ci.get("github_url"):
        parts.append(ci["github_url"].replace("https://", ""))
    if ci.get("linkedin_url"):
        parts.append(ci["linkedin_url"].replace("https://", ""))
    if ci.get("email"):
        parts.append(ci["email"])
    return "  |  ".join(parts)


def generate_pdf(data: dict) -> bytes:
    """Generate resume PDF from pre-processed data dict. Returns raw bytes."""

    pdf = ResumePDF()
    pdf.add_page()

    # ---- Header -----------------------------------------------------------
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*ResumePDF.ACCENT)
    pdf.cell(0, 10, data.get("hero_title", ""), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*ResumePDF.MUTED)
    subtitle = data.get("hero_subtitle", "")
    pdf.cell(0, 6, subtitle, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    contact_line = _build_contact_line(data)
    if contact_line:
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*ResumePDF.MUTED)
        pdf.cell(0, 5, contact_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(3)
    pdf.set_draw_color(*ResumePDF.RULE)
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())

    # ---- About Me ---------------------------------------------------------
    about = data.get("about_me", "").strip()
    if about:
        pdf.section_heading("About Me")
        pdf.body(about)

    # ---- Experience -------------------------------------------------------
    grouped = data.get("grouped_experience", [])
    if grouped:
        pdf.section_heading("Experience")
        for group in grouped:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*ResumePDF.TEXT)
            pdf.cell(0, 5, group["company"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            for role in group["roles"]:
                pdf.ln(1)
                pdf.set_font("Helvetica", "BI", 9)
                pdf.set_text_color(*ResumePDF.TEXT)
                role_line = f"  {role['role']}  -  {role['period']}"
                pdf.cell(0, 4.5, role_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

                details = role.get("details", "").strip()
                if details:
                    pdf.muted_cell(details, indent=4)

            pdf.ln(3)

    # ---- Projects ---------------------------------------------------------
    all_projects = []
    if data.get("featured_project"):
        all_projects.append(data["featured_project"])
    all_projects.extend(data.get("other_projects", []))

    if all_projects:
        pdf.section_heading("Projects")
        for proj in all_projects:
            title = proj.get("title", "")
            stack = proj.get("tech_stack", [])
            stack_str = "  -  " + ", ".join(stack) if stack else ""

            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(*ResumePDF.TEXT)
            pdf.cell(0, 5, title + stack_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            desc = proj.get("description", "").strip()
            if desc:
                pdf.muted_cell(desc, indent=2)

            url = proj.get("url", "").strip()
            if url:
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(*ResumePDF.ACCENT)
                pdf.set_x(pdf.l_margin + 2)
                pdf.cell(0, 4, url, new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=url)

            pdf.ln(2)

    # ---- Skills -----------------------------------------------------------
    skills = data.get("skills", [])
    if skills:
        pdf.section_heading("Skills")
        skill_names = [s["name"] for s in skills]
        # Wrap into rows of ~6
        row_size = 6
        rows = [skill_names[i:i+row_size] for i in range(0, len(skill_names), row_size)]
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*ResumePDF.TEXT)
        for row in rows:
            pdf.cell(0, 5, "  |  ".join(row), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    # ---- Certifications ---------------------------------------------------
    certs = data.get("certifications", [])
    if certs:
        pdf.section_heading("Certifications")
        for cert in certs:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*ResumePDF.TEXT)
            pdf.cell(0, 5, cert.get("name", ""), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            desc = cert.get("description", "").strip()
            if desc:
                pdf.muted_cell(desc, indent=2)

            link = cert.get("link", "").strip()
            if link:
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(*ResumePDF.ACCENT)
                pdf.set_x(pdf.l_margin + 2)
                pdf.cell(0, 4, link, new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=link)

            pdf.ln(2)

    # ---- Footer -----------------------------------------------------------
    pdf.set_y(-12)
    now = datetime.datetime.now().strftime("%B %Y")
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(*ResumePDF.MUTED)
    pdf.cell(0, 5, f"Generated {now}", align="C")

    return bytes(pdf.output())


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    data = _load_data()
    pdf_bytes = generate_pdf(data)

    os.makedirs("output", exist_ok=True)
    out_path = os.path.join("output", "resume.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"PDF written to {out_path}")
