import os
import json
import pandas as pd


def getQAGDataframe():  # Create empty lists to store extracted data
    date_list = []
    asking_group_list = []
    asking_person_id_list = []
    responding_ministry_list = []
    discussion_content_list = []
    question_file_list = []

    # Directory containing the JSON files
    current_directory = os.getcwd()
    json_dir = os.path.join(current_directory, '..', 'json')
    print(json_dir)

    # Iterate through JSON files in the directory
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(json_dir, filename)

            # Load JSON data from the file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Extract the required information from the JSON data
            date_list.append(data['question']['cloture']['dateCloture'])
            asking_group_list.append(
                data['question']['auteur']['groupe']['abrege'])
            author_id = data['question']['auteur']['identite']['acteurRef']
            asking_person_id_list.append(
                getAuthorName(author_id, current_directory))
            responding_ministry_list.append(
                data['question']['minInt']['abrege'])
            try:
                discussion_content_list.append(
                    data['question']['textesReponse']['texteReponse']['texte'])
            except TypeError:
                discussion_content_list.append("NONE")
            question_file_list.append(filename)

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'Date': date_list,
        'Asking_Group': asking_group_list,
        'Asking_Person_ID': asking_person_id_list,
        'Responding_Ministry': responding_ministry_list,
        'Discussion_Content': discussion_content_list,
        'Question_File': question_file_list
    })

    # Optionally, you can convert the 'Date' column to a datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # Display the DataFrame
    # print(df)

    return df


def getAuthorName(person_id: str, cur_dir: str):
    info_dir = os.path.join(cur_dir, '..', 'json_deputes')
    file_path = os.path.join(info_dir, 'acteur', person_id + '.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            author_data = json.load(file)
        author_name = author_data['acteur']['etatCivil']['ident']['civ'] + ' ' + \
            author_data['acteur']['etatCivil']['ident']['prenom'] + ' ' +\
            author_data['acteur']['etatCivil']['ident']['nom']
    except FileNotFoundError:
        author_name = person_id

    return author_name
