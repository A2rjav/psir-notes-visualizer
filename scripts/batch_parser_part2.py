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
            
        page_match = re.search(r'page_(\d+)\.png', body, re.IGNORECASE)
        if not page_match:
            page_match = re.search(r'Page\s+(\d+)', title_clean, re.IGNORECASE)
            
        if page_match:
            try:
                current_scan = int(page_match.group(1))
            except ValueError:
                pass
            
        raw_bullets = re.findall(r'^[ \t]*[\*\-]\s+(.+)$', body, re.MULTILINE)
        details = []
        for b in raw_bullets:
            b_clean = b.strip()
            if len(b_clean) > 10 and not b_clean.startswith('|'):
                details.append(b_clean[:400])
        
        if not details:
            paragraphs = [p.strip() for p in body.split('\n\n') if len(p.strip()) > 30 and not p.strip().startswith('#') and not p.strip().startswith('|')]
            for p in paragraphs[:6]:
                details.append(p[:350])
                
        if len(details) < 2:
            continue
            
        summary = details[0] if details else title_clean
        
        badge = "Theoretical Model"
        tl = title_clean.lower()
        if "realism" in tl or "liberalism" in tl or "marxism" in tl or "constructivism" in tl or "feminism" in tl:
            badge = "IR Theory"
        elif "comparative" in tl or "approach" in tl or "systems" in tl or "structural" in tl:
            badge = "Comparative Approach"
        elif "power" in tl or "security" in tl or "balance" in tl or "nuclear" in tl:
            badge = "Strategic Concept"
        elif "cold war" in tl or "soviet" in tl or "détente" in tl:
            badge = "Geopolitical History"
            
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
    explicit_cards = re.findall(r'(?:Card|Flashcard|\*\*Q\d+:|\*\*Question\d+:)\s*([^\n\?]+\?)\s*(?:Answer|Ans|\*\*A\d+:|\*\*Ans\d+:)?\s*([^\n]+)', md_content, re.IGNORECASE)
    for q, a in explicit_cards[:3]:
        flashcards.append({
            "id": start_id + len(flashcards),
            "front": q.strip().replace('**', ''),
            "back": a.strip().replace('**', '')[:300],
            "badge": "Active Recall",
            "mnemonic": section_title.split(':')[0]
        })
        
    if len(flashcards) < 3:
        quotes = re.findall(r'"([^"]{25,220})"', md_content)
        for q in quotes:
            if len(flashcards) >= 4:
                break
            flashcards.append({
                "id": start_id + len(flashcards),
                "front": f"What theoretical framework or IR paradigm is captured by: \"{q.strip()}\"?",
                "back": f"Essential theoretical concept highlighted in {section_title}. Foundational for conceptual clarity in UPSC PSIR Paper 2 Section A.",
                "badge": "Theoretical Dictum",
                "mnemonic": "Essential IR Reference"
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
                "id": f"ans-p2a-{start_id + len(answers)}",
                "question": q_text,
                "marks": "20 Marks (250 Words)",
                "topic": section_title,
                "structure": {
                    "intro": "Define the core analytical concept, its historical emergence, and theoretical lineage.",
                    "body": [
                        "Deconstruct the principal theoretical arguments, structural assumptions, and key scholarly debates.",
                        "Evaluate major critiques from rival theoretical paradigms (Realist, Liberal, Marxist, Constructivist, Feminist).",
                        "Synthesize contemporary practical relevance to 21st-century global governance, state sovereignty, and international security."
                    ],
                    "scholars": ["Foundational Theorists", "Contemporary Political Scientists", "Critical Scholars"],
                    "conclusion": "Deliver an elegant, balanced UPSC conclusion synthesizing the enduring analytical utility of the concept."
                }
            })
    return answers
