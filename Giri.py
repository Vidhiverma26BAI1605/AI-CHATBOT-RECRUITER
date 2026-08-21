
import tkinter as tk
import json
import spacy
import re
nlp=spacy.load("en_core_web_sm")



with open("giri.json","r") as file:
    questions=json.load(file)["questions"]
answers={}
current=0
SKILLS = [
    "python", "java", "c++", "sql",
    "machine learning", "deep learning",
    "artificial intelligence", "html",
    "css", "javascript", "excel",
    "data analysis", "tensorflow",
    "pandas", "numpy",
]
EXPERIENCE=["Interned","created prject","worked at infosys","build project on deep learning"]
 
EDUCATION_WORDS = [
    "b.tech", "btech", "m.tech", "mtech",
    "bca", "mca", "b.sc", "m.sc",
    "computer science", "engineering",
    "mba", "bba",
]
 
PROJECT_WORDS = [
    " chatbot project", "computer vision projects",
    "developed an ai", "developing a voice weaver",
    "built a ai", "created an AI",
    "worked on hackathons",
]
 
INTERNSHIP_WORDS = [
    "internship for 2 month", "intern at infosys",
    "AIML engineer job", "trainee",
    "industrial training",
]
 
LANGUAGES = [
    "english", "hindi", 
    "c#", "c++", "c",
    "java", "javascript", "python",
    "ruby", "go",
]


def extract_nlp_details(answers):

    text = " ".join(str(value) for value in answers.values())
    text_lower=text.lower()
    doc = nlp(text)

    details = {}

    # Extract name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            details["Name"] = ent.text
            break

    found_skills = [s for s in SKILLS if s in text_lower]
    if found_skills:
        details["Skills"] = found_skills
 
    # Education
    found_education = [w for w in EDUCATION_WORDS if w in text_lower]
    if found_education:
        details["Education"] = found_education
 
    # Experience
    experience = re.search(r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)', text_lower)
    if experience:
        details["Experience"] = experience.group() + " experience"
 
    # Projects (now checked independently of Experience)
    found_projects = [w for w in PROJECT_WORDS if w in text_lower]
    if found_projects:
        details["Projects"] = "Candidate has project experience"
 
    # Internship (now checked independently of Experience)
    found_internship = [w for w in INTERNSHIP_WORDS if w in text_lower]
    if found_internship:
        details["Internship"] = "Candidate has internship experience"
 
    # Languages
    found_languages = [lang for lang in LANGUAGES if lang in text_lower]
    if found_languages:
        details["Languages"] = found_languages
 
    return details
    
def send():
    
    global current
    answer=entry.get().strip()
    if answer=="":
        return
    chat.insert(tk.END,"You:"+ answer +"\n\n")
    key=questions[current]["key"]
    answers[key]=answer
    entry.delete(0,tk.END)
    current+=1
    if current<len(questions):
        chat.insert(
            tk.END,
            "AI Recruiter:"+ questions[current]["question"]+"\n\n"
        )
    else:
        details = extract_nlp_details(answers)

        chat.insert(
            tk.END,
            "AI Recruiter: Thank you! Your information has been collected.\n\n"
        )

        chat.insert(
            tk.END,
            "EXTRACTED CANDIDATE DETAILS:\n"
        )
        
        
        chat.insert(
            tk.END,
            json.dumps(details,indent=4)
        )
        with open("candidate.json","w") as file:
             json.dump(details,file,indent=4)
        entry.config(state="disabled")
        button.config(state="disabled")
root=tk.Tk()
root.title("AI Recruiter Chatbot")
root.geometry("600x650")
title=tk.Label(
     root,text="AI RECRUITER",font=("Arial",22,"bold")

)
title.pack(pady=15)
chat=tk.Text(root,width=70,height=30)
chat.pack(padx=10)
entry=tk.Entry(root,width=50)
entry.pack(side=tk.LEFT,padx=10,pady=10)
button=tk.Button(
     root,
     text="ENTER",
     command=send
)
button.pack(side=tk.LEFT)
if questions: 
     chat.insert(
     tk.END,
     "AI RECRUITER:" + questions[0]["question"]+"\n\n"
)
root.mainloop()
             