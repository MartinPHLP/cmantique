import openai
import os
import io
import time
from tqdm import tqdm

openai.organization = str(os.getenv("OAI_PERSONNAL_ID"))
openai.api_key = str(os.getenv("OAI_SECRET_KEY_ACCESS"))




def get_subjects(path):
    with io.open(path, "r") as f:
        content = f.read()
    content = content.split("\n")
    subjects = [element.replace("...", "") for element in content]
    return subjects


def get_sentence(subject):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f'Tu es un generateur de phrases dans la langue française. Ton français est irréprochable. Format de la réponse : "phrase".'},
            {"role": "user", "content": f'Génere une unique phrase, courte (max 15 mots) et simple en francais, sur le thème suivant : "{subject}". Le type de phrase doit être aléatoire. Format de la réponse : "phrase".'}
        ],
        temperature=1.3,
        n=1,
        max_tokens=50
    )["choices"]

    result = [element["message"]["content"] for element in response]
    return result


def get_associated_sentence(sentence):
    labels = ["opposé", "neutre comparé", "similaire"]
    result = []

    for label in labels:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Tu es un generateur de phrases dans la langue française. Ton français est irréprochable. Maximum 15 mots."},
                {"role": "user", "content": f"Génere une phrase courte et simple en francais (max 15 mots), dont le sens est {label} à celui de la phrase suivante : {sentence}. La structure de la phrase doit être différente."}
            ],
            temperature=1.3,
            n=1,
            max_tokens=50
        )["choices"][0]["message"]["content"]
        result.append(response)

    return result


# liste = get_sentence(get_subjects("/Users/martinphilip/Documents/personal_projects/cmantique/subjects.txt")[3])
liste = get_sentence("Le chef prépare un délicieux repas dans la cuisine.")
test = get_associated_sentence(liste[0])

print(f"{liste[0]}\n{test[0]}\n{test[1]}\n{test[2]}\n")
