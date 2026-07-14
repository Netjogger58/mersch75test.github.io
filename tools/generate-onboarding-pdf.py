#!/usr/bin/env python3
"""Generéiert docs/website-arbeiten-fuer-dummies.pdf aus dem Markdown-Fichier."""

import os
import re
import html
import argparse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem,
    Preformatted, HRFlowable, Table, TableStyle
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT = os.path.join(BASE_DIR, 'docs', 'website-arbeiten-fuer-dummies.md')
DEFAULT_OUTPUT = os.path.join(BASE_DIR, 'docs', 'website-arbeiten-fuer-dummies.pdf')

def parse_args():
    parser = argparse.ArgumentParser(description='Markdown → PDF fir Mersch75-Dokumenter.')
    parser.add_argument('--input', default=DEFAULT_INPUT, help='Markdown-Fichier (default: docs/website-arbeiten-fuer-dummies.md)')
    parser.add_argument('--output', default=DEFAULT_OUTPUT, help='Ziel-PDF (default: docs/website-arbeiten-fuer-dummies.pdf)')
    parser.add_argument('--title', default='Mersch75.lu', help='Titel op der Éischter Säit')
    parser.add_argument('--subtitle', default='Websäit – Dummies Guide', help='Ënnertitel op der Éischter Säit')
    return parser.parse_args()

styles = getSampleStyleSheet()

def make_style(name, parent, **kw):
    base = styles[parent] if parent else None
    return ParagraphStyle(name, parent=base, **kw)

TITLE = make_style('CustomTitle', 'Title', fontSize=22, leading=26, spaceAfter=24, textColor=colors.HexColor('#0d2f8f'))
H1 = make_style('CustomH1', 'Heading1', fontSize=16, leading=20, spaceBefore=18, spaceAfter=10, textColor=colors.HexColor('#0d2f8f'))
H2 = make_style('CustomH2', 'Heading2', fontSize=13, leading=17, spaceBefore=14, spaceAfter=8)
H3 = make_style('CustomH3', 'Heading3', fontSize=11, leading=15, spaceBefore=12, spaceAfter=6)
BODY = make_style('CustomBody', 'BodyText', fontSize=10, leading=14, spaceAfter=6)
QUOTE = make_style('CustomQuote', 'BodyText', fontSize=10, leading=14, leftIndent=20, rightIndent=10, textColor=colors.HexColor('#555555'), spaceAfter=8)
BULLET = make_style('CustomBullet', 'BodyText', fontSize=10, leading=14, leftIndent=10, spaceAfter=4)
CODE = make_style('CustomCode', 'Code', fontName='Courier', fontSize=8, leading=11, leftIndent=20, rightIndent=10, spaceAfter=8)
TABLE_HEADER = make_style('TableHeader', 'BodyText', fontSize=9, leading=12, textColor=colors.white)
TABLE_CELL = make_style('TableCell', 'BodyText', fontSize=8, leading=11)

def md_to_html(line):
    """Wandel Markdown-Inline-Markup a ReportLab-kompatibel HTML."""
    if not line:
        return line
    # XML-Sonderzeechen escapen (awer keng Quotes, well Text net an Attributer steet).
    s = html.escape(line, quote=False)
    # Fett
    s = re.sub(r'\*\*(.+?)\*\*', lambda m: '<b>' + m.group(1) + '</b>', s)
    # Kursiv
    s = re.sub(r'\*(.+?)\*', lambda m: '<i>' + m.group(1) + '</i>', s)
    # Inline-Code
    s = re.sub(r'`([^`]+)`', lambda m: '<font name="Courier" size="9">' + m.group(1) + '</font>', s)
    # Links [text](url)
    def link_repl(m):
        text = m.group(1)
        url = m.group(2).replace('"', '&quot;')
        return f'<a href="{url}" color="#0d2f8f">{text}</a>'
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, s)
    return s

def flush_list(story, items, list_type):
    if not items:
        return
    list_items = [ListItem(Paragraph(it, BULLET)) for it in items]
    if list_type == 'numbered':
        flow = ListFlowable(list_items, bulletType='1', leftIndent=25, bulletIndent=10, spaceBefore=4, spaceAfter=6)
    else:
        flow = ListFlowable(list_items, bulletType='bullet', leftIndent=25, bulletIndent=10, spaceBefore=4, spaceAfter=6)
    story.append(flow)

def parse_table(rows):
    """Markdown-Tabellereien a ReportLab Tabell."""
    data = []
    is_header = True
    for raw in rows:
        if raw.strip().startswith('|'):
            cells = [c.strip() for c in raw.strip().split('|')]
            cells = cells[1:-1]  # éischt a lescht leer Zell ewech
            if all(re.match(r'^[-:]+$', c.strip()) for c in cells):
                continue
            data.append([Paragraph(md_to_html(c), TABLE_HEADER if is_header else TABLE_CELL) for c in cells])
            is_header = False
    if not data:
        return None
    table = Table(data, colWidths=[4.5*cm, 5.5*cm, 5.5*cm], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d2f8f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
    ]))
    return table

def main(input_file=DEFAULT_INPUT, output_file=DEFAULT_OUTPUT, title='Mersch75.lu', subtitle='Websäit – Dummies Guide'):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    story = [Paragraph(title, TITLE), Paragraph(subtitle, H1), Spacer(1, 12)]

    i = 0
    n = len(lines)
    in_code = False
    code_lines = []
    list_buffer = []
    list_type = None

    while i < n:
        line = lines[i].rstrip('\n')

        if in_code:
            if line.strip().startswith('```'):
                story.append(Preformatted('\n'.join(code_lines), CODE, maxLineLength=100))
                story.append(Spacer(1, 6))
                in_code = False
                code_lines = []
            else:
                code_lines.append(line)
            i += 1
            continue

        if line.strip().startswith('```'):
            # Allfälleg Lëscht ofschléissen, ier de Codeblock ufänkt
            if list_buffer:
                flush_list(story, list_buffer, list_type)
                list_buffer = []
                list_type = None
            in_code = True
            i += 1
            continue

        # Tabell erkennen
        if line.strip().startswith('|'):
            table_rows = []
            while i < n and lines[i].strip().startswith('|'):
                table_rows.append(lines[i].rstrip('\n'))
                i += 1
            table = parse_table(table_rows)
            if table:
                story.append(table)
                story.append(Spacer(1, 8))
            continue

        if line.strip() == '---':
            if list_buffer:
                flush_list(story, list_buffer, list_type)
                list_buffer = []
                list_type = None
            story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceBefore=10, spaceAfter=10))
            i += 1
            continue

        # Lëschten
        if line.startswith('- ') or line.startswith('* '):
            item = md_to_html(line[2:])
            if list_type != 'bullet':
                if list_buffer:
                    flush_list(story, list_buffer, list_type)
                list_buffer = []
                list_type = 'bullet'
            list_buffer.append(item)
            i += 1
            continue

        num_match = re.match(r'^(\d+)\.\s+', line)
        if num_match:
            item = md_to_html(line[num_match.end():])
            if list_type != 'numbered':
                if list_buffer:
                    flush_list(story, list_buffer, list_type)
                list_buffer = []
                list_type = 'numbered'
            list_buffer.append(item)
            i += 1
            continue

        # Wann keng Lëscht méi, ofschléissen
        if list_buffer:
            flush_list(story, list_buffer, list_type)
            list_buffer = []
            list_type = None

        # Iwwerschreften
        if line.startswith('# '):
            story.append(Paragraph(md_to_html(line[2:]), H1))
            i += 1
            continue
        if line.startswith('## '):
            story.append(Paragraph(md_to_html(line[3:]), H2))
            i += 1
            continue
        if line.startswith('### '):
            story.append(Paragraph(md_to_html(line[4:]), H3))
            i += 1
            continue

        # Zitat
        if line.startswith('> '):
            story.append(Paragraph(md_to_html(line[2:]), QUOTE))
            i += 1
            continue

        # Eidel Linnen
        if not line.strip():
            i += 1
            continue

        # Normalen Absaz
        story.append(Paragraph(md_to_html(line), BODY))
        i += 1

    flush_list(story, list_buffer, list_type)

    doc = SimpleDocTemplate(output_file, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    doc.build(story)
    print(f'PDF geschriwen: {output_file}')

if __name__ == '__main__':
    args = parse_args()
    main(args.input, args.output, args.title, args.subtitle)
