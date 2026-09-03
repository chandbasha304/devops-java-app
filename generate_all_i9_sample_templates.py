import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

OUT_DIR = os.path.join(os.path.dirname(__file__), "sample_pdfs")
os.makedirs(OUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontSize=8.5,
    textColor=colors.HexColor('#475569'),
    spaceAfter=8
)

section_heading = ParagraphStyle(
    'SectionHeading',
    parent=styles['Heading2'],
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor('#1e293b'),
    spaceBefore=6,
    spaceAfter=4
)

cell_label = ParagraphStyle(
    'CellLabel',
    parent=styles['Normal'],
    fontSize=7.5,
    fontName='Helvetica-Bold',
    textColor=colors.HexColor('#475569')
)

cell_value = ParagraphStyle(
    'CellValue',
    parent=styles['Normal'],
    fontSize=8,
    fontName='Helvetica',
    textColor=colors.HexColor('#0f172a')
)

# 6 Complete Realistic I-9 Scenarios
SAMPLES = [
    {
        "id": "scenario_1",
        "file_name": "i9_template_1_us_citizen_passport.pdf",
        "title": "FORM I-9 TEMPLATE 1: U.S. CITIZEN (LIST A - U.S. PASSPORT)",
        "subtitle": "Scenario 1: Standard U.S. Citizen presenting unexpired U.S. Passport for List A",
        "badge_color": "#1e3a8a",
        "table_bg": "#eff6ff",
        "border_color": "#3b82f6",
        "section_1": {
            "last_name": "Davis",
            "first_name": "Michael",
            "middle_initial": "R",
            "other_names": "N/A",
            "address": "742 Evergreen Terrace",
            "apt": "Apt 12",
            "city": "Springfield",
            "state": "IL",
            "zip": "62704",
            "dob": "11/12/1988",
            "ssn": "234-56-7890",
            "email": "michael.davis@email.com",
            "phone": "217-555-0143",
            "status": "[X] 1. A citizen of the United States",
            "status_details": "N/A (U.S. Citizen)",
            "sig_date": "08/15/2026"
        },
        "section_2": {
            "mode": "List A (Single Document for Identity & Work Authorization)",
            "doc_title_1": "U.S. Passport",
            "issuing_auth_1": "U.S. Department of State",
            "doc_num_1": "C98234112",
            "exp_date_1": "10/20/2032",
            "doc_title_2": "N/A",
            "issuing_auth_2": "N/A",
            "doc_num_2": "N/A",
            "exp_date_2": "N/A",
            "hire_date": "08/15/2026",
            "employer_rep": "Vance, Robert, VP of HR",
            "employer_biz": "Acme Global Technologies Inc.",
            "employer_addr": "100 Tech Blvd, Suite 500, Chicago, IL 60601",
            "employer_sig_date": "08/17/2026"
        }
    },
    {
        "id": "scenario_2",
        "file_name": "i9_template_2_us_citizen_dl_and_ssn.pdf",
        "title": "FORM I-9 TEMPLATE 2: U.S. CITIZEN (LIST B DRIVER'S LICENSE + LIST C SSN)",
        "subtitle": "Scenario 2: U.S. Citizen presenting State DL (Identity) and Unrestricted SS Card (Work Auth)",
        "badge_color": "#047857",
        "table_bg": "#ecfdf5",
        "border_color": "#10b981",
        "section_1": {
            "last_name": "Martinez",
            "first_name": "Emily",
            "middle_initial": "J",
            "other_names": "N/A",
            "address": "1450 Elmwood Ave",
            "apt": "Apt 2B",
            "city": "Austin",
            "state": "TX",
            "zip": "78704",
            "dob": "03/25/1994",
            "ssn": "345-67-8901",
            "email": "emily.martinez@email.com",
            "phone": "512-555-0188",
            "status": "[X] 1. A citizen of the United States",
            "status_details": "N/A (U.S. Citizen)",
            "sig_date": "09/01/2026"
        },
        "section_2": {
            "mode": "List B (Identity) AND List C (Employment Authorization)",
            "doc_title_1": "List B: Driver's License",
            "issuing_auth_1": "Texas DPS",
            "doc_num_1": "TX88492011",
            "exp_date_1": "03/25/2030",
            "doc_title_2": "List C: Social Security Card (Unrestricted)",
            "issuing_auth_2": "Social Security Administration",
            "doc_num_2": "345-67-8901",
            "exp_date_2": "N/A (Does not expire)",
            "hire_date": "09/01/2026",
            "employer_rep": "Ray, Lisa, Talent Acquisition Manager",
            "employer_biz": "Apex Digital Media Inc.",
            "employer_addr": "300 Congress Ave, Suite 800, Austin, TX 78701",
            "employer_sig_date": "09/02/2026"
        }
    },
    {
        "id": "scenario_3",
        "file_name": "i9_template_3_permanent_resident_green_card.pdf",
        "title": "FORM I-9 TEMPLATE 3: PERMANENT RESIDENT (LIST A - FORM I-551 GREEN CARD)",
        "subtitle": "Scenario 3: Lawful Permanent Resident presenting Permanent Resident Card (Form I-551)",
        "badge_color": "#b45309",
        "table_bg": "#fffbeb",
        "border_color": "#f59e0b",
        "section_1": {
            "last_name": "Gomez",
            "first_name": "Carlos",
            "middle_initial": "A",
            "other_names": "N/A",
            "address": "880 Biscayne Blvd",
            "apt": "Suite 1200",
            "city": "Miami",
            "state": "FL",
            "zip": "33132",
            "dob": "07/09/1986",
            "ssn": "456-78-9012",
            "email": "carlos.gomez@email.com",
            "phone": "305-555-0177",
            "status": "[X] 3. A lawful permanent resident",
            "status_details": "USCIS / A-Number: A-098765432",
            "sig_date": "09/10/2026"
        },
        "section_2": {
            "mode": "List A (Permanent Resident Card)",
            "doc_title_1": "Permanent Resident Card (Form I-551)",
            "issuing_auth_1": "USCIS",
            "doc_num_1": "SRC2190012345",
            "exp_date_1": "05/18/2031",
            "doc_title_2": "N/A",
            "issuing_auth_2": "N/A",
            "doc_num_2": "N/A",
            "exp_date_2": "N/A",
            "hire_date": "09/10/2026",
            "employer_rep": "Miller, David, People Operations Lead",
            "employer_biz": "Sunshine Logistics LLC",
            "employer_addr": "1200 Ocean Dr, Miami, FL 33139",
            "employer_sig_date": "09/11/2026"
        }
    },
    {
        "id": "scenario_4",
        "file_name": "i9_template_4_work_authorized_ead_card.pdf",
        "title": "FORM I-9 TEMPLATE 4: ALIEN AUTHORIZED TO WORK (LIST A - FORM I-766 EAD)",
        "subtitle": "Scenario 4: Foreign national with Employment Authorization Document (EAD Card)",
        "badge_color": "#6d28d9",
        "table_bg": "#f5f3ff",
        "border_color": "#8b5cf6",
        "section_1": {
            "last_name": "Patel",
            "first_name": "Priya",
            "middle_initial": "S",
            "other_names": "N/A",
            "address": "520 Pike St",
            "apt": "Apt 18C",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "dob": "09/18/1996",
            "ssn": "567-89-0123",
            "email": "priya.patel@email.com",
            "phone": "206-555-0122",
            "status": "[X] 4. An alien authorized to work until 06/30/2028",
            "status_details": "USCIS / A-Number: A-201884931",
            "sig_date": "09/15/2026"
        },
        "section_2": {
            "mode": "List A (Employment Authorization Document)",
            "doc_title_1": "Employment Authorization Document (Form I-766)",
            "issuing_auth_1": "USCIS",
            "doc_num_1": "WAC2290045678",
            "exp_date_1": "06/30/2028",
            "doc_title_2": "N/A",
            "issuing_auth_2": "N/A",
            "doc_num_2": "N/A",
            "exp_date_2": "N/A",
            "hire_date": "09/15/2026",
            "employer_rep": "Wu, Jennifer, HR Business Partner",
            "employer_biz": "CloudWave Systems Corporation",
            "employer_addr": "400 Pine St, Suite 600, Seattle, WA 98101",
            "employer_sig_date": "09/16/2026"
        }
    },
    {
        "id": "scenario_5",
        "file_name": "i9_template_5_h1b_visa_passport_and_i94.pdf",
        "title": "FORM I-9 TEMPLATE 5: H-1B VISA (LIST A - FOREIGN PASSPORT + FORM I-94)",
        "subtitle": "Scenario 5: Nonimmigrant worker presenting Foreign Passport + Form I-94 Arrival Record",
        "badge_color": "#be123c",
        "table_bg": "#fff1f2",
        "border_color": "#f43f5e",
        "section_1": {
            "last_name": "Petrov",
            "first_name": "Alexey",
            "middle_initial": "D",
            "other_names": "N/A",
            "address": "350 5th Ave",
            "apt": "Floor 44",
            "city": "New York",
            "state": "NY",
            "zip": "10118",
            "dob": "12/04/1990",
            "ssn": "678-90-1234",
            "email": "alexey.petrov@email.com",
            "phone": "212-555-0166",
            "status": "[X] 4. An alien authorized to work until 09/30/2027",
            "status_details": "Form I-94 Admission #: 98765432101",
            "sig_date": "10/01/2026"
        },
        "section_2": {
            "mode": "List A Combination (Foreign Passport + Form I-94)",
            "doc_title_1": "Doc 1: Foreign Passport",
            "issuing_auth_1": "Russian Federation",
            "doc_num_1": "758921004",
            "exp_date_1": "12/04/2029",
            "doc_title_2": "Doc 2: Form I-94 Arrival/Departure Record",
            "issuing_auth_2": "DHS / CBP",
            "doc_num_2": "98765432101",
            "exp_date_2": "09/30/2027",
            "hire_date": "10/01/2026",
            "employer_rep": "Sterling, Jonathan, HR Director",
            "employer_biz": "FinTech Capital Partners LLC",
            "employer_addr": "1 Wall St, Floor 22, New York, NY 10005",
            "employer_sig_date": "10/02/2026"
        }
    },
    {
        "id": "scenario_6",
        "file_name": "i9_template_6_noncitizen_national_state_id_and_birth_cert.pdf",
        "title": "FORM I-9 TEMPLATE 6: NONCITIZEN NATIONAL (LIST B STATE ID + LIST C BIRTH CERT)",
        "subtitle": "Scenario 6: Noncitizen U.S. National presenting State ID + Certification of Birth (Form FS-545)",
        "badge_color": "#0e7490",
        "table_bg": "#ecfeff",
        "border_color": "#06b6d4",
        "section_1": {
            "last_name": "Taufetee",
            "first_name": "Tui",
            "middle_initial": "J",
            "other_names": "N/A",
            "address": "4500 Kalihi St",
            "apt": "Unit 3",
            "city": "Honolulu",
            "state": "HI",
            "zip": "96819",
            "dob": "06/15/1998",
            "ssn": "789-01-2345",
            "email": "tui.taufetee@email.com",
            "phone": "808-555-0155",
            "status": "[X] 2. A noncitizen national of the United States",
            "status_details": "N/A (Born in American Samoa)",
            "sig_date": "10/05/2026"
        },
        "section_2": {
            "mode": "List B (State ID) AND List C (Certification of Birth)",
            "doc_title_1": "List B: State Identification Card",
            "issuing_auth_1": "Hawaii DOT",
            "doc_num_1": "H9812401",
            "exp_date_1": "06/15/2028",
            "doc_title_2": "List C: Certification of Birth Abroad (Form FS-545)",
            "issuing_auth_2": "U.S. Department of State",
            "doc_num_2": "FS545-99812",
            "exp_date_2": "N/A (Does not expire)",
            "hire_date": "10/05/2026",
            "employer_rep": "Silva, Keanu, Staffing Director",
            "employer_biz": "Pacific Horizon Ventures",
            "employer_addr": "1000 Bishop St, Suite 400, Honolulu, HI 96813",
            "employer_sig_date": "10/06/2026"
        }
    }
]

def generate_pdf_scenario(data):
    pdf_path = os.path.join(OUT_DIR, data["file_name"])
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=32, bottomMargin=32)
    story = []

    # Title Banner
    story.append(Paragraph(data["title"], title_style))
    story.append(Paragraph(data["subtitle"], subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor(data["badge_color"]), spaceAfter=10))

    # Section 1
    story.append(Paragraph("Section 1: Employee Information &amp; Attestation (Pre-Filled Data)", section_heading))
    s1 = data["section_1"]
    s1_rows = [
        [
            Paragraph(f"Last Name:<br/><b>{s1['last_name']}</b>", cell_value),
            Paragraph(f"First Name:<br/><b>{s1['first_name']}</b>", cell_value),
            Paragraph(f"M.I.:<br/><b>{s1['middle_initial']}</b>", cell_value),
            Paragraph(f"Other Last Names:<br/><b>{s1['other_names']}</b>", cell_value)
        ],
        [
            Paragraph(f"Address:<br/><b>{s1['address']}</b>", cell_value),
            Paragraph(f"Apt / Suite:<br/><b>{s1['apt']}</b>", cell_value),
            Paragraph(f"City:<br/><b>{s1['city']}</b>", cell_value),
            Paragraph(f"State / ZIP:<br/><b>{s1['state']} {s1['zip']}</b>", cell_value)
        ],
        [
            Paragraph(f"Date of Birth:<br/><b>{s1['dob']}</b>", cell_value),
            Paragraph(f"SSN:<br/><b>{s1['ssn']}</b>", cell_value),
            Paragraph(f"Email Address:<br/><b>{s1['email']}</b>", cell_value),
            Paragraph(f"Telephone:<br/><b>{s1['phone']}</b>", cell_value)
        ],
        [
            Paragraph(f"Citizenship Status Checkbox:<br/><b>{s1['status']}</b>", cell_value),
            Paragraph(f"Immigration / Doc Identifier:<br/><b>{s1['status_details']}</b>", cell_value),
            Paragraph(f"Employee Signature:<br/><b>[Signed: {s1['first_name']} {s1['last_name']}]</b>", cell_value),
            Paragraph(f"Signature Date:<br/><b>{s1['sig_date']}</b>", cell_value)
        ]
    ]

    t1 = Table(s1_rows, colWidths=[135, 135, 135, 135])
    t1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(data["border_color"])),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(data["table_bg"])),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    # Section 2
    story.append(Paragraph(f"Section 2: Employer Review &amp; Verification — {data['section_2']['mode']}", section_heading))
    s2 = data["section_2"]
    s2_rows = [
        [Paragraph("Document Title 1", cell_label), Paragraph(f"<b>{s2['doc_title_1']}</b>", cell_value)],
        [Paragraph("Issuing Authority 1", cell_label), Paragraph(f"<b>{s2['issuing_auth_1']}</b>", cell_value)],
        [Paragraph("Document Number 1", cell_label), Paragraph(f"<b>{s2['doc_num_1']}</b>", cell_value)],
        [Paragraph("Expiration Date 1", cell_label), Paragraph(f"<b>{s2['exp_date_1']}</b>", cell_value)],
        [Paragraph("Document Title 2 (if applicable)", cell_label), Paragraph(f"<b>{s2['doc_title_2']}</b>", cell_value)],
        [Paragraph("Issuing Authority 2", cell_label), Paragraph(f"<b>{s2['issuing_auth_2']}</b>", cell_value)],
        [Paragraph("Document Number 2", cell_label), Paragraph(f"<b>{s2['doc_num_2']}</b>", cell_value)],
        [Paragraph("Expiration Date 2", cell_label), Paragraph(f"<b>{s2['exp_date_2']}</b>", cell_value)],
        [Paragraph("First Day of Employment (Hire Date)", cell_label), Paragraph(f"<b>{s2['hire_date']}</b>", cell_value)],
        [Paragraph("Employer Representative Name &amp; Title", cell_label), Paragraph(f"<b>{s2['employer_rep']}</b>", cell_value)],
        [Paragraph("Employer Business Name &amp; Address", cell_label), Paragraph(f"<b>{s2['employer_biz']}<br/>{s2['employer_addr']}</b>", cell_value)],
        [Paragraph("Employer Signature Date", cell_label), Paragraph(f"<b>{s2['employer_sig_date']}</b>", cell_value)],
    ]

    t2 = Table(s2_rows, colWidths=[190, 350])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(data["border_color"])),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(data["table_bg"])),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t2)

    doc.build(story)
    print(f"[+] Generated: {data['file_name']}")

# Run all 6 generations and export master JSON
if __name__ == "__main__":
    for item in SAMPLES:
        generate_pdf_scenario(item)

    json_path = os.path.join(OUT_DIR, "all_i9_dummy_samples.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(SAMPLES, f, indent=2)
    print(f"\n[+] Generated master JSON dataset: {json_path}")
