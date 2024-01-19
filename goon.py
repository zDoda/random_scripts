import subprocess
import datetime
import openai
import random

# Initialize the OpenAI client
client = openai.OpenAI()

job_titles = [
    "Software Engineer",
    "Data Scientist",
    "Graphic Designer",
    "Project Manager",
    "Product Manager",
    "Accountant",
    "Marketing Manager",
    "Sales Representative",
    "Human Resources Manager",
    "Operations Manager",
    "Customer Service Representative",
    "Web Developer",
    "Business Analyst",
    "Mechanical Engineer",
    "Electrical Engineer",
    "Civil Engineer",
    "Teacher",
    "Nurse",
    "Physician",
    "Lawyer",
    "Architect",
    "Chef",
    "Pharmacist",
    "Financial Analyst",
    "Journalist"
]


def chat_completion(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. you only write python scripts"},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content
    except:
        return "error"


def create_script():
    job_title = random.choice(job_titles)
    script = chat_completion(f'write a python script for {job_title}')
    with open(f'/Users/czook/Github/goon_cave/{datetime.datetime.now()}_{job_title}_script.py', 'w') as file:
        file.write(f'{script}')


def git_commit():
    # Change to your repository directory
    repo_dir = "/Users/czook/Github/goon_cave/"
    commit_message = f"Auto commit on {datetime.datetime.now()}"

    # Commands to execute
    commands = [
        f"git -C {repo_dir} add .",
        f"git -C {repo_dir} commit -m '{commit_message}'",
        f"git -C {repo_dir} push"
    ]

    for cmd in commands:
        subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    git_commit()
# More stuff soon to add
