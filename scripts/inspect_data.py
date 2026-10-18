import json
import re

content = open('app/src/data/paper1IptData.js', encoding='utf-8').read()
# Extract sections
match = re.search(r'export const paper1IptData = (\{.*?\});\s*$', content, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print("Meta topic:", data['meta']['topicTitle'])
    print("Sections count:", len(data['sections']))
    for s in data['sections']:
        print(f"Section {s['number']}: {s['id']} - {s['title']} (Scans: {s.get('scanPages', [])})")
    print("Flashcards count:", len(data.get('flashcards', [])))
    print("Answers count:", len(data.get('answers', [])))
    print("Catalog count:", len(data.get('scansCatalog', [])))
else:
    print("Could not match json")
