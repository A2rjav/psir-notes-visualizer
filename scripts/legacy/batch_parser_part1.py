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
        
        badge = "Bilateral Dynamics"
        tl = title_clean.lower()
        if "doctrine" in tl or "policy" in tl or "strategy" in tl or "accord" in tl:
            badge = "Foreign Policy Doctrine"
        elif "security" in tl or "defense" in tl or "maritime" in tl or "nuclear" in tl:
            badge = "Strategic Security"
        elif "trade" in tl or "wto" in tl or "economic" in tl or "integration" in tl:
            badge = "Global Trade Architecture"
        elif "un" in tl or "asean" in tl or "saarc" in tl or "bimstec" in tl or "eu" in tl:
            badge = "Multilateral Institution"
            
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
                "front": f"What strategic rationale or diplomatic doctrine is defined by: \"{q.strip()}\"?",
                "back": f"Critical geopolitical doctrine highlighted in {section_title}. Key high-scoring conceptual anchor for UPSC PSIR Paper 2.",
                "badge": "Diplomatic Quote",
                "mnemonic": "Essential Strategic Reference"
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
                "id": f"ans-p2b-{start_id + len(answers)}",
                "question": q_text,
                "marks": "20 Marks (250 Words)",
                "topic": section_title,
                "structure": {
                    "intro": "Contextualize India's strategic dilemma, bilateral historical lineage, and geopolitical stakes.",
                    "body": [
                        "Analyze the core structural imperatives, bilateral agreements, and balance of power considerations.",
                        "Evaluate major points of friction, strategic vulnerability, and multilateral constraints.",
                        "Examine India's diplomatic countermeasures, strategic partnerships, and foreign policy innovations."
                    ],
                    "scholars": ["Prominent Strategic Commentators", "Diplomatic Analysts", "Foreign Policy Experts"],
                    "conclusion": "Provide a forward-looking, realistic UPSC conclusion balancing strategic autonomy with vital national security interests."
                }
            })
    return answers
