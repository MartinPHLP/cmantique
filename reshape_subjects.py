import io

def get_subjects(path):
    with io.open(path, "r") as f:
        content = f.read()
    content = content.split("\n")
    return content

def reshape_subjects(path):
    with io.open(path, "r") as f:
        content = f.read()
    content = content.replace("\n\n", "\n").replace('"', '').replace("...", "")
    with io.open(path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    reshape_subjects("/Users/martinphilip/Documents/personal_projects/cmantique/subjects.txt")
    subjects = get_subjects("/Users/martinphilip/Documents/personal_projects/cmantique/subjects.txt")
    sub_without_duplicates = []
    for subject in subjects:
        if subject not in sub_without_duplicates:
            sub_without_duplicates.append(subject)
    with io.open("/Users/martinphilip/Documents/personal_projects/cmantique/subjects.txt", "w") as f:
        for subject in sub_without_duplicates:
            f.write(f"{subject}\n")
    print(f"nb of subjects : {len(sub_without_duplicates)}")
