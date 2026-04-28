"""Generate sample Memphis 311 inspection form PDFs for Activity 4.

Creates realistic-looking inspection forms that Azure Document Intelligence
can process. Uses reportlab to draw text fields on a single-page PDF.

Usage:
    python data/generate_forms.py

Output:
    data/forms/inspection_form_01.pdf
    data/forms/inspection_form_02.pdf
    data/forms/inspection_form_03.pdf
"""
import os
import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
except ImportError:
    print("reportlab is required: pip install reportlab")
    sys.exit(1)


FORM_DATA = [
    {
        "filename": "inspection_form_01.pdf",
        "case_id": "CASE-2026-001",
        "inspector": "James Williams",
        "date": "01/15/2026",
        "location": "1234 Poplar Ave, Memphis, TN 38104",
        "ward": "District 7",
        "violation_type": "Road Damage",
        "severity": "High",
        "description": (
            "Large pothole approximately 18 inches in diameter and 4 inches deep "
            "located in the eastbound lane of Poplar Avenue, 200 feet west of "
            "the Overton Park entrance. The pothole has exposed the gravel base "
            "layer and poses a hazard to vehicles and cyclists. Immediate repair "
            "recommended before further deterioration occurs."
        ),
        "photos_attached": "2",
        "followup": "Yes",
        "phone": "(901) 555-0147",
    },
    {
        "filename": "inspection_form_02.pdf",
        "case_id": "CASE-2026-003",
        "inspector": "Patricia Johnson",
        "date": "02/03/2026",
        "location": "567 Beale St, Memphis, TN 38103",
        "ward": "District 3",
        "violation_type": "Property Violation",
        "severity": "Medium",
        "description": (
            "Multiple instances of graffiti spray paint found on the south-facing "
            "wall of the vacant commercial building at 567 Beale Street. Tags cover "
            "approximately 40 square feet of brick surface. Also observed illegal "
            "dumping of household furniture (couch, mattress) on the adjacent vacant "
            "lot. Property owner notification required."
        ),
        "photos_attached": "3",
        "followup": "Yes",
        "phone": "(901) 555-0283",
    },
    {
        "filename": "inspection_form_03.pdf",
        "case_id": "CASE-2026-009",
        "inspector": "Michael Davis",
        "date": "01/28/2026",
        "location": "890 Front St, Memphis, TN 38103",
        "ward": "District 1",
        "violation_type": "Utility Issue",
        "severity": "High",
        "description": (
            "Active water main leak detected at the intersection of Front Street "
            "and Monroe Avenue. Water is flowing across the sidewalk and into the "
            "street, creating icy conditions during cold weather. Estimated flow "
            "rate suggests a significant pipe rupture. MLGW has been notified for "
            "emergency response. Area cordoned off with traffic cones."
        ),
        "photos_attached": "1",
        "followup": "No",
        "phone": "(901) 555-0391",
    },
]


def draw_field(c, label: str, value: str, x: float, y: float, width: float = 4.5 * inch):
    """Draw a labeled field with underline on the canvas."""
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, f"{label}:")
    label_width = c.stringWidth(f"{label}:", "Helvetica-Bold", 10)
    c.setFont("Helvetica", 10)
    c.drawString(x + label_width + 8, y, value)
    # Draw underline
    c.line(x + label_width + 6, y - 2, x + width, y - 2)


def draw_form(output_path: str, data: dict):
    """Generate a single inspection form PDF."""
    c = canvas.Canvas(output_path, pagesize=letter)
    page_width, page_height = letter

    # Header
    y = page_height - 0.75 * inch
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_width / 2, y, "CITY OF MEMPHIS")
    y -= 22
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_width / 2, y, "311 FACILITIES INSPECTION REPORT")
    y -= 16
    c.setFont("Helvetica", 9)
    c.drawCentredString(page_width / 2, y, "Division of Public Works — Code Enforcement")

    # Horizontal rule
    y -= 12
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1.5)
    c.line(0.75 * inch, y, page_width - 0.75 * inch, y)

    # Form fields
    left = 0.75 * inch
    field_width = 6 * inch
    y -= 30

    draw_field(c, "Case ID", data["case_id"], left, y, field_width)
    y -= 28
    draw_field(c, "Inspector Name", data["inspector"], left, y, field_width)
    y -= 28
    draw_field(c, "Date", data["date"], left, y, 2.5 * inch)
    draw_field(c, "Phone", data["phone"], left + 3 * inch, y, 2.8 * inch)
    y -= 28
    draw_field(c, "Location", data["location"], left, y, field_width)
    y -= 28
    draw_field(c, "Ward", data["ward"], left, y, 2.5 * inch)
    draw_field(c, "Severity", data["severity"], left + 3 * inch, y, 2.8 * inch)
    y -= 28
    draw_field(c, "Violation Type", data["violation_type"], left, y, field_width)

    # Description (multiline)
    y -= 35
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left, y, "Description:")
    y -= 18
    c.setFont("Helvetica", 10)

    # Word-wrap the description
    words = data["description"].split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if c.stringWidth(test_line, "Helvetica", 10) < field_width:
            line = test_line
        else:
            c.drawString(left, y, line)
            y -= 15
            line = word
    if line:
        c.drawString(left, y, line)
        y -= 15

    # Bottom fields
    y -= 20
    draw_field(c, "Photos Attached", data["photos_attached"], left, y, 2.5 * inch)
    draw_field(c, "Follow-up Required", data["followup"], left + 3 * inch, y, 2.8 * inch)

    # Footer
    y -= 40
    c.setLineWidth(1)
    c.line(left, y, left + 2.5 * inch, y)
    c.setFont("Helvetica", 9)
    c.drawString(left, y - 14, "Inspector Signature")

    c.line(left + 3.5 * inch, y, left + 6 * inch, y)
    c.drawString(left + 3.5 * inch, y - 14, "Date")

    # Page footer
    c.setFont("Helvetica", 8)
    c.drawCentredString(
        page_width / 2, 0.5 * inch,
        "Memphis 311 — Call (901) 636-6500 or visit memphistn.gov/311"
    )

    c.save()


def main():
    """Generate all sample inspection form PDFs."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "forms")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating {len(FORM_DATA)} inspection forms in {output_dir}/")
    for data in FORM_DATA:
        output_path = os.path.join(output_dir, data["filename"])
        draw_form(output_path, data)
        print(f"  Created: {data['filename']}")

    print(f"\nDone! {len(FORM_DATA)} inspection forms generated.")


if __name__ == "__main__":
    main()
