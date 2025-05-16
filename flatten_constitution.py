import json

# Load the file
with open('COI.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles_raw = data[0]
parts_index = data[1]

# Create a mapping from article number to part info
article_to_part = {}
for part in parts_index:
    name = f"Part {part['PartNo']} - {part['Name']}"
    for art_no in part["Articles"]:
        article_to_part[art_no] = name

# Function to create unique IDs
def make_id(article, clause=None, subclause=None, explanation=None):
    id_str = f"Art{article}"
    if clause: id_str += f"_{clause}"
    if subclause: id_str += f"_{subclause}"
    if explanation: id_str += f"_Exp{explanation}"
    return id_str

# Flatten logic
flattened = []

for article in articles_raw:
    art_no = article.get("ArtNo")
    title = article.get("Name", "")
    part = article_to_part.get(art_no, "Unknown Part")
    subheading = article.get("SubHeading", "")
    tags = [subheading] if subheading else []

    # Handle articles with ArtDesc only (no clauses)
    if "ArtDesc" in article:
        flattened.append({
            "id": make_id(art_no),
            "article_number": art_no,
            "title": title,
            "part": part,
            "content": article["ArtDesc"],
            "tags": tags
        })

    # Handle clauses
    if "Clauses" in article:
        for clause in article["Clauses"]:
            clause_no = clause.get("ClauseNo")
            clause_desc = clause.get("ClauseDesc")
            flattened.append({
                "id": make_id(art_no, clause_no),
                "article_number": f"{art_no}({clause_no})",
                "title": title,
                "part": part,
                "content": clause_desc,
                "tags": tags
            })

            # Sub-clauses
            if "SubClauses" in clause:
                for sub in clause["SubClauses"]:
                    sub_no = sub.get("SubClauseNo")
                    sub_desc = sub.get("SubClauseDesc")
                    flattened.append({
                        "id": make_id(art_no, clause_no, sub_no),
                        "article_number": f"{art_no}({clause_no})({sub_no})",
                        "title": title,
                        "part": part,
                        "content": sub_desc,
                        "tags": tags
                    })

    # Handle explanations
    if "Explanations" in article:
        for exp in article["Explanations"]:
            exp_no = exp.get("ExplanationNo")
            exp_desc = exp.get("Explanation")
            flattened.append({
                "id": make_id(art_no, explanation=exp_no),
                "article_number": f"{art_no} - Explanation {exp_no}",
                "title": title,
                "part": part,
                "content": exp_desc,
                "tags": tags + ["Explanation"]
            })

# Save to a .jsonl file
with open('flattened_constitution.jsonl', 'w', encoding='utf-8') as f:
    for entry in flattened:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

print(f"✅ Flattened {len(flattened)} entries to 'flattened_constitution.jsonl'")
