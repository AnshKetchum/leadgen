# https://github.com/IvanIsCoding/ResuLLMe/blob/main/src/templates/__init__.py#L10

import jinja2
import os
import shutil
import tempfile
import subprocess
from .doc_utils import escape_for_latex

template_commands = {
    "Simple": ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
    "Awesome": ["xelatex", "-interaction=nonstopmode", "resume.tex"],
    "BGJC": ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
    "Deedy": ["xelatex", "-interaction=nonstopmode", "resume.tex"],
    "Modern": ["pdflatex", "-interaction=nonstopmode", "resume.tex"],
    "Plush": ["xelatex", "-interaction=nonstopmode", "resume.tex"],
    "Alta": ["xelatex", "-interaction=nonstopmode", "resume.tex"],
}

def generate_latex(template_name, json_resume, prelim_section_ordering):
    dir_path = os.path.abspath('leadgen/templates/resume')
    print(dir_path)

    latex_jinja_env = jinja2.Environment(
        block_start_string="\BLOCK{",
        block_end_string="}",
        variable_start_string="\VAR{",
        variable_end_string="}",
        comment_start_string="\#{",
        comment_end_string="}",
        line_statement_prefix="%-",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(dir_path),
    )

    escaped_json_resume = escape_for_latex(json_resume)

    return use_template(
        template_name, latex_jinja_env, escaped_json_resume, prelim_section_ordering
    )


def use_template(template_name, jinja_env, json_resume, prelim_section_ordering):
    PREFIX = f"{template_name}"
    EXTENSION = "tex.jinja"

    print(os.path.abspath(os.path.join("leadgen", "templates", "resume", PREFIX, f"resume.{EXTENSION}")))
    resume_template = jinja_env.get_template(os.path.join(PREFIX, f'resume.{EXTENSION}'))
    basics_template = jinja_env.get_template(os.path.join(PREFIX, f'basics.{EXTENSION}'))
    education_template = jinja_env.get_template(os.path.join(PREFIX, f'education.{EXTENSION}'))
    work_template = jinja_env.get_template(os.path.join(PREFIX, f'work.{EXTENSION}'))
    skills_template = jinja_env.get_template(os.path.join(PREFIX, f'skills.{EXTENSION}'))
    projects_template = jinja_env.get_template(os.path.join(PREFIX, f'projects.{EXTENSION}'))
    awards_template = jinja_env.get_template(os.path.join(PREFIX, f'awards.{EXTENSION}'))

    sections = {}
    section_ordering = get_final_section_ordering(prelim_section_ordering)

    if "basics" in json_resume:
        firstName = json_resume["basics"]["name"].split(" ")[0]
        lastName = " ".join(json_resume["basics"]["name"].split(" ")[1:])
        sections["basics"] = basics_template.render(
            firstName=firstName, lastName=lastName, **json_resume["basics"]
        )
    if "education" in json_resume and len(json_resume["education"]) > 0:
        sections["education"] = education_template.render(
            schools=json_resume["education"], heading="Education"
        )
    if "work" in json_resume and len(json_resume["work"]) > 0:
        sections["work"] = work_template.render(
            works=json_resume["work"], heading="Work Experience"
        )

    if "skills" in json_resume and len(json_resume["skills"]) > 0:
        sections["skills"] = skills_template.render(
            skills=json_resume["skills"], heading="Skills"
        )
    if "projects" in json_resume and len(json_resume["projects"]) > 0:
        sections["projects"] = projects_template.render(
            projects=json_resume["projects"], heading="Projects"
        )

    if "awards" in json_resume and len(json_resume["awards"]) > 0:
        sections["awards"] = awards_template.render(
            awards=json_resume["awards"], heading="Awards"
        )

    resume = resume_template.render(
        sections=sections, section_ordering=section_ordering
    )
    return resume


def get_final_section_ordering(section_ordering):
    final_ordering = ["basics"]
    additional_ordering = section_ordering + [
        "education",
        "work",
        "skills",
        "projects",
        "awards",
    ]
    for section in additional_ordering:
        if section not in final_ordering:
            final_ordering.append(section)

    return final_ordering


def render_latex(latex_command, latex_data):
    src_path = os.path.dirname(os.path.realpath(__file__)) + "/inputs"

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Copy auxiliary files to temporary directory
        shutil.copytree(src_path, tmpdirname, dirs_exist_ok=True)

        print("LATEX", latex_data, latex_command)

        with open("temp.tex", 'w') as f:
            f.write(latex_data)

        # write latex data to a file
        with open(f"{tmpdirname}/resume.tex", "w") as f:
            f.write(latex_data)

        # run latex command
        latex_process = subprocess.Popen(latex_command, cwd=tmpdirname)
        latex_process.wait()

        # read pdf data
        with open(f"{tmpdirname}/resume.pdf", "rb") as f:
            pdf_data = f.read()

    return pdf_data