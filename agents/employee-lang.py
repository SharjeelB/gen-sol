#pip install langchain openai python-dotenv


import json
import re
import os
import openai

from dotenv import load_dotenv

load_dotenv("env.local")

# try to fetch employee records from OpenAI; fall back to local file
def fetch_employees_via_openai():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    
    openai.api_key = api_key
    print(f"OPENAI_API_KEY: {openai.api_key}")
    prompt = (
        "You are given no context. Return the full employee dataset as a JSON array of objects. "
        "Each object should have fields like name, department, title, salary if available. "
        "Respond ONLY with valid JSON array and no extra text."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1500,
    )
    text = resp.choices[0].message.content
    return json.loads(text)

try:
    data = fetch_employees_via_openai()
except Exception:
    with open("data/employee.json") as f:
        data = json.load(f)

def find_employees_by_name(query, employees):
    matches = []
    q = query.lower()
    for emp in employees:
        name = emp.get("name", "").lower()
        if name and name in q:
            matches.append(emp)
    # try matching first or last name tokens
    if not matches:
        tokens = re.findall(r"[A-Za-z]+", query)
        for t in tokens:
            for emp in employees:
                parts = emp.get("name", "").lower().split()
                if parts and (parts[0] == t.lower() or (len(parts) > 1 and parts[1] == t.lower())):
                    if emp not in matches:
                        matches.append(emp)
    return matches

def list_employees_in_department(dept, employees):
    return [e for e in employees if e.get("department", "").lower() == dept.lower()]

question = input("Ask a question: ")

q = question.lower()
employees = data if isinstance(data, list) else data.get("employees", [])

emps = find_employees_by_name(question, employees)

if "salary" in q or "pay" in q or "compensation" in q:
    if emps:
        if len(emps) == 1:
            sal = emps[0].get("salary") or emps[0].get("pay")
            print(sal if sal is not None else "Salary not found in data.")
        else:
            out = [{"name": e.get("name"), "salary": e.get("salary") or e.get("pay")} for e in emps]
            print(json.dumps(out, indent=2))
    else:
        print("Employee not found in data.")
elif "department" in q or "dept" in q:
    if emps:
        if len(emps) == 1:
            print(emps[0].get("department", "Department not found in data."))
        else:
            out = [{"name": e.get("name"), "department": e.get("department")} for e in emps]
            print(json.dumps(out, indent=2))
    else:
        # ask for employees in a department
        m = re.search(r"in (the )?([A-Za-z &]+) department", question, re.IGNORECASE)
        if m:
            dept = m.group(2)
            emps = list_employees_in_department(dept, employees)
            if emps:
                print(json.dumps(emps, indent=2))
            else:
                print("No employees found in that department.")
        else:
            print("Employee not found in data.")
elif "title" in q or "position" in q or "job" in q:
    if emps:
        if len(emps) == 1:
            print(emps[0].get("title", emps[0].get("position", "Title not found in data.")))
        else:
            out = [{"name": e.get("name"), "title": e.get("title", e.get("position"))} for e in emps]
            print(json.dumps(out, indent=2))
    else:
        print("Employee not found in data.")
elif "list" in q and "department" in q:
    # e.g., list departments
    depts = sorted({e.get("department") for e in employees if e.get("department")})
    print(json.dumps(depts, indent=2))
else:
    # fallback: try to return full employee record if name present
    if emps:
        if len(emps) == 1:
            print(json.dumps(emps[0], indent=2))
        else:
            print(json.dumps(emps, indent=2))
    else:
        print(json.dumps(data, indent=2))