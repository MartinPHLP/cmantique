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
    subjects = content.split("\n")
    return subjects


def get_sentence(subject):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f'Tu es un generateur de phrases dans la langue française uniquement. Ton français est irréprochable. Format de la réponse : "phrase".'},
            {"role": "user", "content": f'Génere une unique phrase, courte (max 15 mots) et simple en francais, sur le thème suivant : "{subject}". Le type de phrase doit être aléatoire. Format de la réponse : "phrase".'}
        ],
        temperature=1.3,
        n=10,
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
                {"role": "system", "content": f"Tu es un generateur de phrases dans la langue française uniquement. Ton français est irréprochable. Maximum 15 mots."},
                {"role": "user", "content": f"Génere une phrase courte et simple en francais (max 15 mots), dont le sens est {label} à celui de la phrase suivante : {sentence}. La structure de la phrase doit être différente."}
            ],
            temperature=1.3,
            n=1,
            max_tokens=50
        )["choices"][0]["message"]["content"]
        result.append(response)
    result = [sentence.replace('"', "") for sentence in result]

    return result


def get_sub_id(subjects, element):
    for i, subject in enumerate(subjects):
        if element == subject:
            return (i)
    print("ID ERROR")
    exit()


if __name__ == "__main__":
    subjects = get_subjects("./subjects.txt")
    subject_id_begin = int(input("Subject id to begin: "))
    subject_id_end = int(input("Subject id to end: "))

    for sub in subjects[subject_id_begin:subject_id_end]:
        have_sentences = 0
        have_triples = 0
        too_much_fail = 0
        too_munch_count = 0
        id = get_sub_id(subjects, sub)
        with io.open(f"./semFr_ds/{str(id)}.txt", "w") as f:
            while have_sentences != 1:
                if too_much_fail > 4:
                    if too_munch_count == 3:
                        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!! API PROBLEM, STOP EXECUTING !!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                        exit()
                    too_much_fail = 0
                    too_munch_count += 1
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!! TOO MUCH FAIL, WAIT !!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                    time.sleep(120)

                try:
                    sentences = []
                    responses = get_sentence(sub)
                    for response in responses:
                        if response.replace('"', "").replace("« ", "").replace("« ", "") not in sentences:
                            sentences.append(response.replace('"', "").replace("«", "").replace("»", ""))
                    have_sentences = 1

                except Exception as e:
                    too_much_fail += 1
                    print(f"\n{e}\n\nLAST ID NOT COMPLETED : {id}\n\n\n")

            finished_sentences = []
            while have_triples != 1:
                if too_much_fail > 4:
                    if too_munch_count == 3:
                        print("\n\nAPI PROBLEM, STOP EXECUTING\n\n")
                        exit()
                    too_much_fail = 0
                    too_munch_count += 1
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!! TOO MUCH FAIL, WAIT !!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                    time.sleep(120)

                try:
                    for sentence in tqdm(sentences):
                        time.sleep(0.5)
                        if sentence not in finished_sentences:
                            triple = get_associated_sentence(sentence)
                            finished_sentences.append(sentence)
                            f.write(f"{sentence}\n{triple[0]}\n{triple[1]}\n{triple[2]}\n\n")
                    have_triples = 1
                    print(f"\n\n\n ************************** ID COMPLETED : {id} **************************\n\n\n")

                except Exception as e:
                    too_much_fail += 1
                    print(f"\n{e}\n\nLAST ID NOT COMPLETED : {id}\n\n\n")
