import os
import json
import re

from batch_meta import get_batch_metadata

def parse_markdown_to_concepts(md_content, default_scan_start):
    # Split content by markdown headings
    # Look for sections like ### or ## 
    concepts = []
    
    # Try finding sub-modules or thematic blocks
    pattern = r'(?:###|####)\s+([^\n]+)\n(.*?)(?=(?:###|####|\Z))'
    matches = re.findall(pattern, md_content, re.DOTALL)
    
    current_scan = default_scan_start
    
    for title, body in matches:
        title_clean = title.strip().replace('**', '').replace('`', '')
        if any(skip in title_clean.lower() for skip in ['archival', 'pyq', 'model answer', 'upsc psir', 'table of contents', 'overview']):
            continue
            
        # Check if page scan mentioned in title or body
        page_match = re.search(r'page_(\d+)\.png', body, re.IGNORECASE)
        if page_match:
            current_scan = int(page_match.group(1))
            
        # Extract bullet points
        raw_bullets = re.findall(r'^[ \t]*[\*\-]\s+(.+)$', body, re.MULTILINE)
        details = []
        for b in raw_bullets:
            b_clean = b.strip()
            if len(b_clean) > 10 and not b_clean.startswith('|'):
                # Clean markdown bold markers if too cluttered
                details.append(b_clean[:400])
        
        # If no bullet points found, extract sentences
        if not details:
            paragraphs = [p.strip() for p in body.split('\n\n') if len(p.strip()) > 30 and not p.strip().startswith('#') and not p.strip().startswith('|')]
            for p in paragraphs[:6]:
                details.append(p[:350])
                
        if len(details) < 2:
            continue
            
        # Summary
        summary = details[0] if details else title_clean
        
        # Badge determination
        badge = "Core Concept"
        if "debate" in title_clean.lower() or "vs" in title_clean.lower():
            badge = "Theoretical Debate"
        elif "article" in title_clean.lower() or "case" in title_clean.lower() or "amendment" in title_clean.lower() or "schedule" in title_clean.lower():
            badge = "Constitutional Doctrine"
        elif "commission" in title_clean.lower() or "reforms" in title_clean.lower():
            badge = "Institutional Reforms"
        elif any(k in title_clean.lower() for k in ["kothari", "austin", "ambedkar", "gandhi", "roy", "bipin", "palshikar"]):
            badge = "Scholarly Perspective"
            
        concepts.append({
            "title": title_clean[:120],
            "scanPage": current_scan,
            "badge": badge,
            "summary": summary[:250],
            "details": details[:8]
        })
        
        if len(concepts) >= 8:
            break
            
    return concepts

def parse_flashcards(md_content, section_title, start_id):
    # Look for flashcards or generate high-yield cards from quotes/scholars
    flashcards = []
    
    # Check for quotes
    quotes = re.findall(r'"([^"]{25,200})"', md_content)
    for q in quotes[:3]:
        flashcards.append({
            "id": start_id + len(flashcards),
            "front": f"Who asserted or what does this dictum refer to: \"{q.strip()}\"?",
            "back": f"Key doctrinal quote highlighted in {section_title}. Represents core analytical framework for UPSC answer enrichment.",
            "badge": "Quote & Dictum",
            "mnemonic": "Essential Thinker Reference"
        })
        
    return flashcards

def parse_model_answers(md_content, section_title, start_id):
    answers = []
    # Look for Model Answer sections
    qa_blocks = re.findall(r'(?:###|####)\s*(?:Question|Model Answer|PYQ)[^\n]*\n(.*?)(?=(?:###|####|\Z))', md_content, re.DOTALL | re.IGNORECASE)
    for block in qa_blocks[:2]:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) >= 4:
            q_text = lines[0].replace('**', '').replace('Question:', '').strip()
            if len(q_text) < 15:
                continue
            answers.append({
                "id": f"ans-{start_id + len(answers)}",
                "question": q_text,
                "marks": "20 Marks (250 Words)",
                "topic": section_title,
                "structure": {
                    "intro": "Contextualize the theme through constitutional provisions, historical debates, and foundational scholars.",
                    "body": [
                        "Analyze primary dimensions, core contentions, and competing schools of thought.",
                        "Assess institutional mechanisms, judicial interpretations, and realpolitik dynamics.",
                        "Synthesize empirical trends from contemporary governance and committee recommendations."
                    ],
                    "scholars": ["Constitutional Bench Jurisprudence", "Leading Political Theorists", "Official Commission Reports"],
                    "conclusion": "Conclude with a balanced forward-looking vision emphasizing constitutional morality and institutional balance."
                }
            })
    return answers

print("Parser functions compiled successfully.")
