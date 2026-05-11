"""Generate Claude-Campus-Fellows-Plan.pdf from the program design markdown.

Uses fpdf2 with macOS TrueType fonts (Arial + Georgia) so smart quotes
and em-dashes render natively.
"""

from fpdf import FPDF

FONT_DIR = "/System/Library/Fonts/Supplemental"


class Plan(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("sans", size=8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 6, f"Claude Campus Fellows  ·  {self.page_no()}", align="C")


COLOR_INK = (20, 20, 19)
COLOR_MUTED = (95, 95, 95)
COLOR_RULE = (220, 218, 210)
COLOR_CRAIL = (193, 95, 60)
COLOR_PAMPAS = (244, 243, 238)


pdf = Plan(format="letter")
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(left=22, top=22, right=22)

# Sans (Arial) — used as Helvetica Neue approximation
pdf.add_font("sans", "", f"{FONT_DIR}/Arial.ttf")
pdf.add_font("sans", "B", f"{FONT_DIR}/Arial Bold.ttf")
pdf.add_font("sans", "I", f"{FONT_DIR}/Arial Italic.ttf")
pdf.add_font("sans", "BI", f"{FONT_DIR}/Arial Bold Italic.ttf")
# Serif (Georgia)
pdf.add_font("serif", "", f"{FONT_DIR}/Georgia.ttf")
pdf.add_font("serif", "B", f"{FONT_DIR}/Georgia Bold.ttf")
pdf.add_font("serif", "I", f"{FONT_DIR}/Georgia Italic.ttf")
pdf.add_font("serif", "BI", f"{FONT_DIR}/Georgia Bold Italic.ttf")

pdf.add_page()


def text_w():
    return pdf.w - pdf.l_margin - pdf.r_margin


def write_paragraph(text, size=11, style="", color=COLOR_INK, family="serif", leading=5.3, gap=2.5):
    pdf.set_font(family, style=style, size=size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, leading, text)
    pdf.ln(gap)


def write_h1(text):
    pdf.set_font("sans", style="B", size=24)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(0, 9, text)
    pdf.ln(1)


def write_byline(text):
    pdf.set_font("sans", style="", size=12)
    pdf.set_text_color(*COLOR_MUTED)
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)


def write_h2(text):
    if pdf.get_y() > 30:
        pdf.ln(4)
    pdf.set_draw_color(*COLOR_RULE)
    pdf.set_line_width(0.2)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(4)
    pdf.set_font("sans", style="B", size=15)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(0, 7, text)
    pdf.ln(2)


def write_h3(text):
    pdf.ln(2)
    pdf.set_font("sans", style="B", size=12)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(0, 6, text)
    pdf.ln(1)


def write_h4(text):
    pdf.ln(1)
    pdf.set_font("sans", style="B", size=10.5)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(0, 5.5, text)
    pdf.ln(0.5)


def write_bullet(text, level=0):
    indent = 4 + level * 5
    bullet = "•" if level == 0 else "–"
    pdf.set_x(pdf.l_margin + indent)
    pdf.set_font("serif", style="", size=11)
    pdf.set_text_color(*COLOR_INK)
    bw = pdf.get_string_width(bullet + "  ")
    pdf.cell(bw, 5.3, bullet + "  ")
    pdf.multi_cell(text_w() - indent - bw, 5.3, text)
    pdf.ln(0.5)


def write_numbered(num, text, level=0):
    indent = 4 + level * 5
    pdf.set_x(pdf.l_margin + indent)
    pdf.set_font("sans", style="B", size=10.5)
    pdf.set_text_color(*COLOR_CRAIL)
    label = f"{num}."
    lw = pdf.get_string_width(label + "  ")
    pdf.cell(lw, 5.3, label + "  ")
    pdf.set_font("serif", style="", size=11)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(text_w() - indent - lw, 5.3, text)
    pdf.ln(0.5)


def write_rationale(text, level=1):
    indent = 4 + level * 5 + 6
    pdf.set_x(pdf.l_margin + indent)
    pdf.set_font("serif", style="I", size=10)
    pdf.set_text_color(*COLOR_MUTED)
    pdf.multi_cell(text_w() - indent, 5, "Rationale: " + text)
    pdf.ln(0.5)


def write_blockquote(text, attribution):
    pdf.ln(2)
    start_y = pdf.get_y()
    pdf.set_font("serif", style="I", size=14)
    pdf.set_text_color(*COLOR_INK)
    pdf.set_x(pdf.l_margin + 6)
    pdf.multi_cell(text_w() - 8, 7, text)
    end_y = pdf.get_y()
    pdf.set_draw_color(*COLOR_CRAIL)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, start_y, pdf.l_margin, end_y)
    pdf.ln(1)
    pdf.set_font("sans", style="", size=10.5)
    pdf.set_text_color(*COLOR_MUTED)
    pdf.set_x(pdf.l_margin + 6)
    pdf.cell(0, 5, "— " + attribution, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)


def write_thesis(text):
    pdf.ln(2)
    start_x = pdf.l_margin
    pdf.set_font("serif", style="I", size=11)
    pdf.set_text_color(*COLOR_INK)
    y0 = pdf.get_y()
    pdf.set_x(start_x + 6)
    pdf.multi_cell(text_w() - 12, 5.5, text)
    y1 = pdf.get_y()
    pdf.set_fill_color(*COLOR_PAMPAS)
    pdf.rect(start_x, y0 - 2, text_w(), (y1 - y0) + 4, style="F")
    pdf.set_draw_color(*COLOR_CRAIL)
    pdf.set_line_width(1.0)
    pdf.line(start_x, y0 - 2, start_x, y1 + 2)
    pdf.set_y(y0)
    pdf.set_x(start_x + 6)
    pdf.set_font("serif", style="I", size=11)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(text_w() - 12, 5.5, text)
    pdf.ln(5)


def write_mitigation(text):
    pdf.ln(1)
    pdf.set_x(pdf.l_margin + 8)
    pdf.set_font("serif", style="", size=10)
    pdf.set_text_color(*COLOR_INK)
    pdf.multi_cell(text_w() - 10, 5, "Mitigation: " + text)
    pdf.ln(2)


# ============ CONTENT ============

write_h1("Claude Campus Fellows")
write_byline("by Arinze Obiezue")

write_blockquote(
    "“Never doubt that a small group of thoughtful, committed citizens can change the world. Indeed it’s the only thing that ever has.”",
    "Margaret Mead",
)

write_paragraph(
    "This quote, printed on the walls of the African Leadership University, changed my life in 2016. It made me believe in the power of collective thought and action, no matter how small. It sits at the center of my belief in startups like Anthropic as the most potent vehicles for systems-level change, with passionate people as its vectors. My approach to designing this program is rooted in this belief."
)

# About
write_h2("About Claude Campus Fellows")
write_paragraph(
    "The Claude Campus Fellows program is a community of graduate students, primarily from the humanities, who convene and guide campus-wide conversations on AI and society for both graduate and undergraduate students. While the Campus Ambassadors lead the Claude Builder Clubs as technical product evangelists, the Campus Fellows lead the Claude Thinker Salons as non-technical thought curators. The objectives of the program are to:"
)
write_bullet("give non-technical students a voice in steering AI development and its impact on society")
write_bullet("help Anthropic’s education team understand how Claude helps thinking/learning for students")
write_bullet("increase Claude usage among students from humanities, arts, and culture disciplines")

write_h3("Program & Thinker Salon Structure")
structure = [
    ("1 Campus Fellow per campus", "solving the bystander effect of multiple fellows with unequal engagement"),
    ("7–10 students per salon", "to ensure depth of engagement per participant"),
    ("3–4 disciplines represented per salon", "to capture a wider surface area of student insights"),
    ("1:1 ratio of grad and undergrad participants per salon", "giving equal voice to students across educational levels"),
    ("10 weeks long", "mapped onto the same timeline as the sister Campus Ambassador program"),
    ("Pilot program beginning with 5–10 schools with existing Claude for Education presence or deep involvement in AI ethics (eg: The Schwarzman Center for Humanities at Oxford University that houses the Institute for AI Ethics)", "to give the program team a learning window before scaling"),
    ("Faculty sponsor required", "to provide an institutional accountability partner for aligning salon topics with school priorities and ensuring published artifacts align with school policies"),
]
for i, (item, rationale) in enumerate(structure, 1):
    write_numbered(i, item)
    write_rationale(rationale)

write_thesis("Structure thesis: For Ambassadors, the work is distribution. For Fellows, the work is curation. This way, both programs can be symbiotic on one campus.")

write_h3("Program Requirements for Campus Fellows")
write_bullet("Minimum of 4 salons per semester/quarter")
write_bullet("A shareable Claude artifact summarizing each salon")
write_bullet("A capstone piece of content summarizing the insights from all salons per semester/quarter (eg: video, zine, essay, song, poem, etc.)")
write_bullet("Mandatory attendance of at least 1 Campus Fellow Seminar with members of Anthropic’s education, research, beneficial deployments, and/or policy teams to share live insights")

write_h3("Target Disciplines")
write_bullet("Philosophy")
write_bullet("English & Literature")
write_bullet("History")
write_bullet("Education")
write_bullet("Anthropology")
write_bullet("Design / Arts / Media / Entertainment")

# Positioning
write_h2("Program Positioning")
write_numbered(1, "Alignment with Anthropic’s DNA: Anthropic’s work building frontier AI systems while stewarding thoughtful conversations on AI and human flourishing springs naturally from the company’s founding DNA.")
write_bullet("Founder alignment: As a company built and run by both builder and thinker archetypes, reflected in Dario’s engineering background and Daniela’s humanities background, it’s critical for its Campus Program to mirror that duality.", level=1)
write_bullet("Org + mission alignment: As one of the few AI labs structured as a Public Benefit Corporation instead of the typical C-Corp, Anthropic’s legal mandate demands a balance between frontier development and thoughtful deployment of AI. While the Campus Ambassador program caters to the former, the Campus Fellowship program caters to the latter.", level=1)

write_numbered(2, "Program Differentiation: Every other AI campus program, from Perplexity’s Campus Partner program to Lovable’s Campus Leaders program, focuses primarily on growing product usage. OpenAI’s 100 Chats for College Students was a step towards more thoughtful student engagement but fell short on reach, global inclusion, and societal impact by focusing on producing a single artifact, a book on ChatGPT prompts, rather than a stream of artifacts on ongoing conversations with student communities around the world rather than just the US. Additionally, its ChatGPT Lab initiatives are still centrally organized by OpenAI’s education team rather than empowering students to organize it themselves.")
write_bullet("Also, most AI campus programs lean heavily on undergraduates (especially CS undergrads), even though graduate students often have deeper disciplinary expertise and facilitation experience. The Campus Fellows program creates a pathway to thoughtfully engage the expertise, maturity, and advanced experience of graduate students to create communities for both graduate and undergraduate students.", level=1)

write_numbered(3, "Core Insight: Because most AI campus programs focus on ‘builders’, they inadvertently exclude students from the humanities and other non-technical disciplines. However, most of the answers to the ‘big questions’ have come from a collaboration between the sciences and the arts. Also, focusing on just technical student communities cuts the total addressable student market in half. The Campus Fellows program unlocks the other half.")

# Resources
write_h2("Resources & Dependencies")
write_h4("Resources")
write_bullet("Conversation Guides: instructionals with prompts and tips for how to guide the conversation and ideas on how to leverage AI to synthesize insights from the salon.")
write_bullet("Employee Time: As the insights from the salons will likely be most relevant for the education, beneficial deployments, research, and policy teams, the program will require 1 hour of their time each month for Campus Fellow Seminars where they get to share some of their ‘big questions’ with fellows, some of whom will also be selected in advance to share insights from their campuses.")
write_bullet("Fellow Compensation: equal compensation as the Campus Ambassador program to convey the equal standing of both reps on campus as co-leaders of the Claude community on campus.")
write_bullet("Salon Reimbursement: reimbursement for salon-related expenses capped at $500 per semester/quarter; mirroring the same budget the Builder Clubs have.")
write_bullet("Content Distribution Channels: an owned channel for showcasing and distributing high-quality artifacts and insights from student salons (eg: a YouTube channel or a Substack publication).")
write_bullet("Recruitment Pipelines (value for new grads): Feeder into more research-oriented roles at Anthropic such as the Fellows Program, Research Engineer/Scientist, etc.")

write_h4("Dependencies")
write_bullet("Reputation risk: Content produced by Fellows could be misinterpreted as Anthropic-approved.")
write_mitigation("All content published by fellows must include a disclaimer along the lines of “This content, curated by a Claude Campus Fellow, represents the personal views of the students in the salon, not Anthropic’s views or that of any of its employees.” Without this, the respective Fellow will be removed from the program. Due to the severity of the reputation risk, this will be the most strictly enforced rule in the program.")
write_bullet("Program & title conflation: Lay people could confuse the Campus Fellowship for the more official FTE fellowship programs at Anthropic, although that risk also exists with the Campus Ambassador vs. Community Ambassador programs.")
write_mitigation("There will be clear and strict guidelines on how Fellows should indicate their role title on LinkedIn as well as on other social platforms. This will be monitored very closely by the Campus program team and violating fellows will be removed from the program.")
write_bullet("Research depth: Some laypeople may confuse artifacts produced from salons to be fully researched opinions that are worth parroting as market-shaping insights due to the Claude/Anthropic halo.")
write_mitigation("Content published by fellows must include a disclaimer that the insights from the artifact represent insights from guided conversations with students rather than in-depth empirical research.")

# Success Metrics
write_h2("Success Metrics")
write_paragraph("I’d know the program is working based on:")

write_h4("Primary Goals")
primary = [
    ("# of salons organized on campus", "ensuring an active presence of Claude/Anthropic on campus"),
    ("Interdisciplinary diversity per salon", "ensuring Claude’s penetration across multiple non-technical disciplines"),
    ("Number of Claude artifacts created per salon (a program requirement)", "ensuring students are actively using Claude products"),
    ("Reach of artifacts and salon content (podcasts, essays, articles, zines, etc.)", "expand how society thinks about use cases for Claude artifacts and creative tools like Claude Design"),
    ("# of product/program/policy decisions that are influenced by student insights (eg: employees quoting student insights in presentations, or Claude for Education resources building on artifacts from the thinking salons)", "gives students real, measurable agency at Anthropic"),
]
for i, (item, rationale) in enumerate(primary, 1):
    write_numbered(i, item)
    write_rationale(rationale)

write_h4("Aspirational Goals")
write_numbered(6, "# of FTE hires from the Fellowship program")
write_rationale("signals the high quality bar of the Fellowship program")

# Experience
write_h2("My Experience with Thinking Salons")
write_bullet("As an undergrad in Mauritius, I founded and ran a weekly thinking salon called Think & Chill where friends and I met every Sunday at 8pm to discuss a range of topics we had to complete some pre-readings for.")
write_bullet("Post-undergrad, when I moved to Nairobi to launch my Gen Z culture magazine, I also co-founded the ‘Sunday High Table (SHiT)’ in parallel as a biweekly intellectual community for my creative and non-creative friends to discuss philosophical topics.")
write_bullet("At Stanford, I’m part of a think club with PhDs in the medical school where we read and discuss essays from James Baldwin to Paul Graham that inspire us to think more broadly about society and our place in it.")
write_bullet("I’m also a Thinking About Thinking Fellow, part of a global community of academics, scientists, researchers, designers, and philosophers, working on the open problems at the intersection of intelligence, society, and governance.")
write_paragraph("These experiences give me a tested playbook for recruiting, facilitating, and sustaining small, high-trust thinking salons across very different contexts and markets.")


pdf.output("Claude-Campus-Fellows-Plan.pdf")
print("PDF generated")
