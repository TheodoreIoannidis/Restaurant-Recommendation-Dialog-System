import os


def get_next_filename(run="sample", extension=".txt"):
    """
    Find last sample*.txt file in the directory and return the next filename 
    """
    # list of all files in the directory
    files = os.listdir()

    max_number = 0  # store the highest number found

    for file in files:
        if file.startswith(run) and file.endswith(extension):
            # remove base name and extension to get the numeric part (if any)
            name_part = file[len(run):-len(extension)]  # Get the part between the base name and extension

            if name_part.isdigit():
                max_number = max(max_number, int(name_part))

    next_number = max_number + 1
    
    return f"{run}{next_number}{extension}" # (sample1.txt, sample2.txt, etc.)

def consent():
    """
    Ask user for consent and proceed if it is given.
    returns True for positive and False for negative choice
    """
    print(
        "\nBefore we begin, it is important to know that all data that we collect will be anonymous and confidential, and you will not be identifiable in any report, thesis or publication which arises from this study. If the dataset will be published as part of scientific communications this will be done in an anonymized fashion.  We will kindly ask your permission to use your data for research purposes.")
    print("\nYou are free to decline this request, of course, but you will not be able to finish the experiment.")
    print("\n By agreeing, you:")
    print(
        "\n a) understand that your participation is voluntary and that you are free to withdraw at any time, without giving a reason, without your medical care or legal rights being affected.")
    print(
        "\n b) understand that the research data will be archived in a completely anonymous way in an online database and/or data repository and/or published as supplementary material to a scientific article and may be accessed by other researchers as well as the general public.")
    print(
        "\n c) understand that the anonymized research data can be used in future projects on similar or different topics to this study and potential results can be published in other scientific publications. At all times, your personal data will be kept anonymized in accordance with data protection guidelines.")
    print("\n Do you consent? (Yes or No)")

    userinput = input().lower().strip()
    if userinput == "yes" or userinput == "y":
        return True
    if userinput == "no" or userinput == "n":
        return False



def questionaire():
    """
    questionaire on system's performance and user's data
    returns a dictionary with the user's answers

    """
    questions = {
        'rating': 'On a scale from 1 to 10, how would you rate this system?',
        'understanding': 'On a scale from 1 to 10, how understandable were the dialog agent responses?',
        'Human-like': 'On a scale from 1 to 10, how natural did the interaction with the dialog agent feel?',
        'Recommendation': 'Would you recommend this system to others? (Yes or no).',
        'Reusability': 'Would you use this system again? (Yes or no)',
        'Age': 'Please indicate your age group: (18-25), (25-40), (40-60).',
    }

    answers = {}
    total = len(questions)
    print('\n Session complete. Please answer the following questions:\n')
    i = 1
    for key, question in questions.items():
        print(f'Q{i}/{total}: {question}')
        userinput = input()
        answers[key] = userinput
        i += 1

    return answers       
