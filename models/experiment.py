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
    if next_number == 1:
        return f"{run}{extension}"  # First file (sample.txt)
    else:
        return f"{run}{next_number}{extension}" # (sample1.txt, sample2.txt, etc.)

def consent():
    """
    Ask user for consent and proceed if it is given.
    returns True for positive and False for negative choice
    """

    print("\n Do you want to start searching? (Yes or No)")

    userinput = input()
    if 'yes' in userinput:
        return True
    else:
        return False


def questionaire():
    """
    questionaire on system's performance and user's data
    returns a dictionary with the user's answers
    
    """
    questions= {
        'rating': 'On a scale from 1 to 10, how would you rate this system?',
        'understanding':'On a scale from 1 to 10, how understandable were the dialog agent responses?',
        'Human-like': 'On a scale from 1 to 10, how natural did the interaction with the dialog agent feel?',
        'Recommendation': 'Would you recommend this system to others? (Yes or no).',
        'Reusability': 'Would you use this system again? (Yes or no)',
        'Age': 'Please indicate your age group: (18-25), (25-40), (40-60).', 
    }
    
    answers = {}
    total =  len(questions)
    print('\n Session complete. Please answer the following questions:\n')
    i = 1
    for key, question in questions.items():
        print(f'Q{i}/{total}: {question}')
        userinput= input()
        answers[key]= userinput     
        i+= 1
    
    return answers       
