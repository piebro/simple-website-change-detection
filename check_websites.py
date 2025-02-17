import hashlib
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def save_changes(changes):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_entry = f"\n## {timestamp}\n"
    if changes:
        log_entry += "\n".join(f"- {change}" for change in changes) + "\n"
        
    with open("log.md") as f:
        existing_content = f.read()
    
    with open("log.md", "w") as f:
        f.write(log_entry + existing_content)

def check_by_search_text(changes, query):
    response = requests.get(query["URL"])
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
        
    # Get visible text
    visible_text = soup.get_text()
    # Clean up whitespace
    visible_text = " ".join(visible_text.split())
    
    expected_count = query.get("ExpectedCount", 1)
    actual_count = visible_text.count(query["SearchText"])
    has_changed = actual_count != expected_count
    if has_changed:
        changes.append(f"{query['Name']}: Content changed! Expected `{expected_count}` occurrence(s) of `{query['SearchText']}`, found `{actual_count}`")
        query["ExpectedCount"] = actual_count
    return has_changed

def check_by_hash(changes, query):
    response = requests.get(query["URL"])
    content_hash = hashlib.md5(response.text.encode()).hexdigest()
    has_changed = content_hash != query["Hash"]
    if has_changed:
        changes.append(f"{query['Name']}: Content changed! New hash: `{content_hash}`")
        query["Hash"] = content_hash
    return has_changed

def check_by_search_html(changes, query):
    response = requests.get(query["URL"])
    html_content = response.text
    
    expected_count = query.get("ExpectedCount", 1)
    actual_count = html_content.count(query["SearchHTML"])
    has_changed = actual_count != expected_count
    if has_changed:
        changes.append(f"{query['Name']}: HTML content changed! Expected `{expected_count}` occurrence(s) of `{query['SearchHTML']}`, found `{actual_count}`")
        query["ExpectedCount"] = actual_count
    return has_changed

def check_websites():
    # Read queries from JSON file instead of importing
    with open("queries.json") as f:
        queries = json.load(f)
    
    changes = []
    queries_to_keep = []
    
    for query in queries:
        try:
            if "Hash" in query:
                has_changed = check_by_hash(changes, query)
            elif "SearchHTML" in query:
                has_changed = check_by_search_html(changes, query)
            elif "SearchText" in query:
                has_changed = check_by_search_text(changes, query)
            else:
                print(f"No check method found for {query['Name']}")
                has_changed = False
                
            if has_changed and query.get("DeleteOnChange", False):
                changes.append(f"{query['Name']}: Query removed after change detected")
            else:
                queries_to_keep.append(query)

        except Exception as e:
            changes.append(f"Error checking {query['Name']}: {e}")
            queries_to_keep.append(query)

    # Update queries.json with the new values
    with open("queries.json", "w") as f:
        json.dump(queries_to_keep, f, indent=4)
            
    save_changes(changes)

if __name__ == "__main__":
    check_websites()
