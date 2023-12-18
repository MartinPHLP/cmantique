import io
import csv


def get_txt_content(file_id):
    with io.open(f"./semFr_ds/{file_id}.txt", "r") as f:
        content = f.read()
    return content


def clean_and_shape_content(content):
    id_to_pop = []

    splitted_content = content.split("\n\n")
    splitted_content = [element for element in splitted_content if len(element) > 2]
    for i, element in enumerate(splitted_content):
        splitted_element = element.split("\n")
        splitted_element = [element for element in splitted_element if len(element) > 2]
        if len(splitted_element) != 4 and i not in id_to_pop:
            id_to_pop.append(i)
        for sentence in splitted_element:
            if ('"' in sentence or '(' in sentence or ')' in sentence or '+' in sentence or 'Interrogati' in sentence or 'Impérati' in sentence or 'Exclamati' in sentence or 'Affirmati' in sentence or 'interrogati' in sentence or 'impérati' in sentence or 'exclamati' in sentence or 'affirmati' in sentence or 'Interjecti' in sentence or 'interjecti' in sentence or 'Verbe' in sentence or 'verbe' in sentence or 'phrase' in sentence or 'Phrase' in sentence) and i not in id_to_pop:
                id_to_pop.append(i)
    for id in reversed(id_to_pop):
        splitted_content.pop(id)

    return splitted_content


if __name__ == "__main__":

    max_id = int(input("Max id : "))
    with open("./semFr.csv", "w") as f:
        headers = ["sentence1", "sentence2", "label"]
        data = []

        for id in range(max_id + 1):
            content = get_txt_content(id)
            clean_content = clean_and_shape_content(content)
            for element in clean_content:
                sentences = element.split("\n")
                data.append([sentences[0], sentences[1], '-1'])
                data.append([sentences[0], sentences[2], '0'])
                data.append([sentences[0], sentences[3], '1'])

        csv_content = csv.writer(f)
        csv_content.writerow(headers)
        csv_content.writerows(data)

