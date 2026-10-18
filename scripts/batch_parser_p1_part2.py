import os
import json
import re

def parse_markdown_to_concepts(md_content, default_scan_start):
    concepts = []
    
    # Split content by markdown headings (### or #### or ##)
    pattern = r'(?:###|####)\s+([^\n]+)\n(.*?)(?=(?:###|####|\Z))'
    matches = re.findall(pattern, md_content, re.DOTALL)
    
    current_scan = default_scan_start
    
    for title, body in matches:
        title_clean = title.strip().replace('**', '').replace('`', '')
        if any(skip in title_clean.lower() for skip in ['archival', 'pyq', 'model answer', 'upsc psir', 'table of contents', 'overview', 'metadata']):
            continue
            
        # Check if page scan mentioned in title or body
        page_match = re.search(r'page_(\d+)\.png', body, re.IGNORECASE)
        if not page_match:
            page_match = re.search(r'Page\s+(\d+)', title_clean, re.IGNORECASE)
            
        if page_match:
            try:
                current_scan = int(page_match.group(1))
            except ValueError:
                pass
            
        # Extract bullet points
        raw_bullets = re.findall(r'^[ \t]*[\*\-]\s+(.+)$', body, re.MULTILINE)
        details = []
        for b in raw_bullets:
            b_clean = b.strip()
            if len(b_clean) > 10 and not b_clean.startswith('|'):
                details.append(b_clean[:400])
        
        # If no bullet points found, extract sentences / paragraphs
        if not details:
            paragraphs = [p.strip() for p in body.split('\n\n') if len(p.strip()) > 30 and not p.strip().startswith('#') and not p.strip().startswith('|')]
            for p in paragraphs[:6]:
                details.append(p[:350])
                
        if len(details) < 2:
            continue
            
        summary = details[0] if details else title_clean
        
        # Badge determination
        badge = "Core Concept"
        tl = title_clean.lower()
        if "debate" in tl or "vs" in tl or "critique" in tl:
            badge = "Theoretical Debate"
        elif "article" in tl or "case" in tl or "amendment" in tl or "doctrine" in tl or "act" in tl:
            badge = "Constitutional Doctrine"
        elif "commission" in tl or "reforms" in tl or "committee" in tl:
            badge = "Institutional Reforms"
        elif any(k in tl for k in ["kothari", "guha", "mehta", "baxi", "ambedkar", "gandhi", "roy", "upadhyay", "jaffrelot", "joshi"]):
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
    flashcards = []
    
    # 1. Search for explicit flashcards in the markdown
    explicit_cards = re.findall(r'(?:Card|Flashcard|\*\*Q\d+:|\*\*Question\d+:)\s*([^\n\?]+\?)\s*(?:Answer|Ans|\*\*A\d+:|\*\*Ans\d+:)?\s*([^\n]+)', md_content, re.IGNORECASE)
    for q, a in explicit_cards[:3]:
        flashcards.append({
            "id": start_id + len(flashcards),
            "front": q.strip().replace('**', ''),
            "back": a.strip().replace('**', '')[:300],
            "badge": "Active Recall",
            "mnemonic": section_title.split(':')[0]
        })
        
    # 2. Extract quotes if needed
    if len(flashcards) < 3:
        quotes = re.findall(r'"([^"]{25,220})"', md_content)
        for q in quotes:
            if len(flashcards) >= 4:
                break
            flashcards.append({
                "id": start_id + len(flashcards),
                "front": f"Who asserted or what does this dictum refer to: \"{q.strip()}\"?",
                "back": f"Key doctrinal quote highlighted in {section_title}. Essential analytical framework for UPSC PSIR answer enrichment.",
                "badge": "Quote & Dictum",
                "mnemonic": "Essential Thinker Reference"
            })
            
    return flashcards

def parse_model_answers(md_content, section_title, start_id):
    answers = []
    qa_blocks = re.findall(r'(?:###|####)\s*(?:Question|Model Answer|PYQ)[^\n]*\n(.*?)(?=(?:###|####|\Z))', md_content, re.DOTALL | re.IGNORECASE)
    for block in qa_blocks[:2]:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) >= 3:
            q_text = lines[0].replace('**', '').replace('Question:', '').replace('PYQ:', '').strip()
            if len(q_text) < 15:
                continue
            answers.append({
                "id": f"ans-p2-{start_id + len(answers)}",
                "question": q_text,
                "marks": "20 Marks (250 Words)",
                "topic": section_title,
                "structure": {
                    "intro": "Contextualize the topic through constitutional provisions, historical background, and foundational political thinkers.",
                    "body": [
                        "Analyze primary institutional dimensions, ideological positions, and competing schools of thought.",
                        "Examine landmark judicial rulings, empirical governance deficits, and realpolitik dynamics.",
                        "Synthesize empirical evidence from national commissions, committee reports, and scholarly debates."
                    ],
                    "scholars": ["Constitutional Bench Jurisprudence", "Leading Political Scientists & Sociologists", "Official Commission Reports (ARC / Punchhi / Law Commission)"],
                    "conclusion": "Synthesize a forward-looking conclusion grounded in constitutional morality, good governance, and institutional balance."
                }
            })
    return answers
