import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Output directory for sample PDFs
OUT_DIR = os.path.join(os.path.dirname(__file__), "sample_pdfs")
os.makedirs(OUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=16,
    leading=20,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#475569'),
    spaceAfter=12
)

section_heading = ParagraphStyle(
    'SectionHeading',
    parent=styles['Heading2'],
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#1e293b'),
    spaceBefore=8,
    spaceAfter=6
)

cell_label = ParagraphStyle(
    'CellLabel',
    parent=styles['Normal'],
    fontSize=8,
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#475569')
)

cell_value = ParagraphStyle(
    'CellValue',
    parent=styles['Normal'],
    fontSize=8.5,
    fontName='Helvetica',
    textColor=colors.HexColor('#0f172a')
)

# ----------------------------------------------------------------------
# PDF 1: Complete Employee Onboarding Profile & I-9 Data Sheet
# ----------------------------------------------------------------------
def generate_employee_profile_pdf():
    pdf_path = os.path.join(OUT_DIR, "1_employee_i9_input_data_sheet.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    story.append(Paragraph("EMPLOYEE ONBOARDING &amp; FORM I-9 SOURCE DATA SHEET", title_style))
    story.append(Paragraph("Official Source Document for Automated I-9 Ingestion &amp; Field Mapping", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=12))

    story.append(Paragraph("Section 1: Employee Personal Information", section_heading))
    sec1_data = [
        [Paragraph("FIELD NAME", cell_label), Paragraph("VALUE (FOR I-9 SECTION 1 MAPPING)", cell_label)],
        [Paragraph("Last Name (Family Name)", cell_value), Paragraph("Smith", cell_value)],
        [Paragraph("First Name (Given Name)", cell_value), Paragraph("John", cell_value)],
        [Paragraph("Middle Initial", cell_value), Paragraph("A", cell_value)],
        [Paragraph("Other Last Names Used", cell_value), Paragraph("N/A", cell_value)],
        [Paragraph("Residential Address", cell_value), Paragraph("123 Innovation Way", cell_value)],
        [Paragraph("Apartment / Suite", cell_value), Paragraph("Apt 4B", cell_value)],
        [Paragraph("City", cell_value), Paragraph("San Jose", cell_value)],
        [Paragraph("State", cell_value), Paragraph("CA", cell_value)],
        [Paragraph("ZIP Code", cell_value), Paragraph("95112", cell_value)],
        [Paragraph("Date of Birth (mm/dd/yyyy)", cell_value), Paragraph("05/14/1992", cell_value)],
        [Paragraph("U.S. Social Security Number", cell_value), Paragraph("123-45-6789", cell_value)],
        [Paragraph("Employee Email Address", cell_value), Paragraph("john.smith@example.com", cell_value)],
        [Paragraph("Employee Telephone Number", cell_value), Paragraph("408-555-0199", cell_value)],
        [Paragraph("Citizenship / Immigration Status", cell_value), Paragraph("1. A citizen of the United States", cell_value)],
        [Paragraph("Signature Attestation Date", cell_value), Paragraph("09/03/2026", cell_value)],
    ]

    t1 = Table(sec1_data, colWidths=[190, 350])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Section 2: Employer &amp; Employment Verification Information", section_heading))
    sec2_data = [
        [Paragraph("FIELD NAME", cell_label), Paragraph("VALUE (FOR I-9 SECTION 2 MAPPING)", cell_label)],
        [Paragraph("First Day of Employment (Hire Date)", cell_value), Paragraph("09/01/2026", cell_value)],
        [Paragraph("Employer / Authorized Rep Name", cell_value), Paragraph("Williams, Sarah", cell_value)],
        [Paragraph("Employer Title", cell_value), Paragraph("HR Director", cell_value)],
        [Paragraph("Employer Business Name", cell_value), Paragraph("CloudTech Solutions Inc.", cell_value)],
        [Paragraph("Employer Business Address", cell_value), Paragraph("500 Tech Parkway, Suite 200", cell_value)],
        [Paragraph("Employer City, State, ZIP", cell_value), Paragraph("San Jose, CA 95110", cell_value)],
        [Paragraph("Employer Verification Date", cell_value), Paragraph("09/03/2026", cell_value)],
    ]

    t2 = Table(sec2_data, colWidths=[190, 350])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)

    doc.build(story)
    print(f"[+] Created: {pdf_path}")


# ----------------------------------------------------------------------
# PDF 2: List A Document - Synthetic U.S. Passport PDF
# ----------------------------------------------------------------------
def generate_passport_pdf():
    pdf_path = os.path.join(OUT_DIR, "2_sample_list_a_us_passport.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    story.append(Paragraph("UNITED STATES OF AMERICA - PASSPORT IDENTIFICATION", title_style))
    story.append(Paragraph("Form I-9 Acceptable Document - LIST A (Establishes Identity &amp; Work Auth)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceAfter=14))

    passport_data = [
        [Paragraph("PASSPORT METADATA FIELD", cell_label), Paragraph("EXTRACTED FIELD VALUE FOR FORM I-9", cell_label)],
        [Paragraph("Document Title", cell_value), Paragraph("U.S. Passport", cell_value)],
        [Paragraph("Issuing Authority", cell_value), Paragraph("U.S. Department of State", cell_value)],
        [Paragraph("Passport / Document Number", cell_value), Paragraph("A12345678", cell_value)],
        [Paragraph("Surname / Last Name", cell_value), Paragraph("SMITH", cell_value)],
        [Paragraph("Given Names / First &amp; Middle", cell_value), Paragraph("JOHN A", cell_value)],
        [Paragraph("Nationality", cell_value), Paragraph("UNITED STATES OF AMERICA", cell_value)],
        [Paragraph("Date of Birth", cell_value), Paragraph("05/14/1992", cell_value)],
        [Paragraph("Place of Birth", cell_value), Paragraph("CALIFORNIA, U.S.A.", cell_value)],
        [Paragraph("Date of Issue", cell_value), Paragraph("08/15/2024", cell_value)],
        [Paragraph("Expiration Date", cell_value), Paragraph("08/14/2034", cell_value)],
        [Paragraph("Document Verification Status", cell_value), Paragraph("UNEXPIRED - VALID FOR EMPLOYMENT", cell_value)],
    ]

    t = Table(passport_data, colWidths=[190, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eff6ff')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#93c5fd')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    doc.build(story)
    print(f"[+] Created: {pdf_path}")


# ----------------------------------------------------------------------
# PDF 3: List B & C Documents - Driver's License + Social Security Card
# ----------------------------------------------------------------------
def generate_dl_ssn_pdf():
    pdf_path = os.path.join(OUT_DIR, "3_sample_list_b_dl_and_list_c_ssn.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    story.append(Paragraph("LIST B (DRIVER'S LICENSE) &amp; LIST C (SOCIAL SECURITY CARD)", title_style))
    story.append(Paragraph("Form I-9 Acceptable Documents Combination (Identity + Work Authorization)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f766e'), spaceAfter=12))

    story.append(Paragraph("LIST B: Identity Document (Driver's License)", section_heading))
    dl_data = [
        [Paragraph("FIELD NAME", cell_label), Paragraph("DOCUMENT VALUE", cell_label)],
        [Paragraph("Document Title", cell_value), Paragraph("Driver's License", cell_value)],
        [Paragraph("Issuing Authority", cell_value), Paragraph("California DMV", cell_value)],
        [Paragraph("Document Number (DL #)", cell_value), Paragraph("D9876543", cell_value)],
        [Paragraph("Full Name", cell_value), Paragraph("JOHN A SMITH", cell_value)],
        [Paragraph("Address", cell_value), Paragraph("123 INNOVATION WAY, SAN JOSE, CA 95112", cell_value)],
        [Paragraph("Date of Birth", cell_value), Paragraph("05/14/1992", cell_value)],
        [Paragraph("Issue Date", cell_value), Paragraph("05/14/2024", cell_value)],
        [Paragraph("Expiration Date", cell_value), Paragraph("05/14/2029", cell_value)],
    ]
    t1 = Table(dl_data, colWidths=[190, 350])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0fdfa')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    story.append(Paragraph("LIST C: Employment Authorization Document (Social Security Card)", section_heading))
    ssn_data = [
        [Paragraph("FIELD NAME", cell_label), Paragraph("DOCUMENT VALUE", cell_label)],
        [Paragraph("Document Title", cell_value), Paragraph("Social Security Card", cell_value)],
        [Paragraph("Issuing Authority", cell_value), Paragraph("Social Security Administration", cell_value)],
        [Paragraph("Document Number (SSN)", cell_value), Paragraph("123-45-6789", cell_value)],
        [Paragraph("Name on Card", cell_value), Paragraph("JOHN A. SMITH", cell_value)],
        [Paragraph("Card Restrictions", cell_value), Paragraph("None (Unrestricted - Valid for Employment)", cell_value)],
        [Paragraph("Expiration Date", cell_value), Paragraph("N/A", cell_value)],
    ]
    t2 = Table(ssn_data, colWidths=[190, 350])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0fdfa')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#99f6e4')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)

    doc.build(story)
    print(f"[+] Created: {pdf_path}")


# ----------------------------------------------------------------------
# PDF 4: Pre-filled Form I-9 Reference Template PDF
# ----------------------------------------------------------------------
def generate_filled_i9_template_pdf():
    pdf_path = os.path.join(OUT_DIR, "4_prefilled_form_i9_reference_template.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    story = []

    story.append(Paragraph("FORM I-9 PRE-FILLED REFERENCE TEMPLATE", title_style))
    story.append(Paragraph("Complete Layout of Populated Form I-9 (USCIS Edition 01/20/25)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#b45309'), spaceAfter=12))

    story.append(Paragraph("Section 1: Employee Information &amp; Attestation (Populated)", section_heading))
    s1_rows = [
        [Paragraph("Last Name: <b>Smith</b>", cell_value), Paragraph("First Name: <b>John</b>", cell_value), Paragraph("Middle Initial: <b>A</b>", cell_value), Paragraph("Other Names: <b>N/A</b>", cell_value)],
        [Paragraph("Address: <b>123 Innovation Way</b>", cell_value), Paragraph("Apt: <b>Apt 4B</b>", cell_value), Paragraph("City: <b>San Jose</b>", cell_value), Paragraph("State: <b>CA</b> ZIP: <b>95112</b>", cell_value)],
        [Paragraph("DOB: <b>05/14/1992</b>", cell_value), Paragraph("SSN: <b>123-45-6789</b>", cell_value), Paragraph("Email: <b>john.smith@example.com</b>", cell_value), Paragraph("Tel: <b>408-555-0199</b>", cell_value)],
        [Paragraph("Status: <b>[X] 1. Citizen of U.S.</b>", cell_value), Paragraph("A-Number: <i>N/A</i>", cell_value), Paragraph("I-94 #: <i>N/A</i>", cell_value), Paragraph("Sig Date: <b>09/03/2026</b>", cell_value)],
    ]
    t1 = Table(s1_rows, colWidths=[135, 135, 135, 135])
    t1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d97706')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffbeb')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Section 2: Employer Review &amp; Verification (List A - Passport)", section_heading))
    s2_rows = [
        [Paragraph("Document Title 1", cell_label), Paragraph("U.S. Passport", cell_value)],
        [Paragraph("Issuing Authority", cell_label), Paragraph("U.S. Department of State", cell_value)],
        [Paragraph("Document Number", cell_label), Paragraph("A12345678", cell_value)],
        [Paragraph("Expiration Date", cell_label), Paragraph("08/14/2034", cell_value)],
        [Paragraph("First Day of Employment (Hire Date)", cell_label), Paragraph("09/01/2026", cell_value)],
        [Paragraph("Employer Representative Name &amp; Title", cell_label), Paragraph("Williams, Sarah, HR Director", cell_value)],
        [Paragraph("Employer Business Name &amp; Address", cell_label), Paragraph("CloudTech Solutions Inc., 500 Tech Parkway, Suite 200, San Jose, CA 95110", cell_value)],
        [Paragraph("Employer Signature Date", cell_label), Paragraph("09/03/2026", cell_value)],
    ]
    t2 = Table(s2_rows, colWidths=[190, 350])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d97706')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffbeb')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)

    doc.build(story)
    print(f"[+] Created: {pdf_path}")


if __name__ == "__main__":
    generate_employee_profile_pdf()
    generate_passport_pdf()
    generate_dl_ssn_pdf()
    generate_filled_i9_template_pdf()
    print("\n[✓] All 4 Sample Reference PDFs generated successfully in 'sample_pdfs/' directory!")
