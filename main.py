import nltk
import pandas as pd
import random
from models.restaurant import Restaurant
from models.experiment import consent, questionaire, get_next_filename


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stopwords = nltk.corpus.stopwords.words("english")

restaurant_info_df = pd.read_csv('./data/restaurant_info.csv')
# read restaurant data
rest_data = pd.read_csv('./data/restaurant_info.csv', sep=',')
# create additional columns with random values
num_rows = rest_data.shape[0]
rest_data.insert(4, "food quality", random.choices(['bad', 'good'], k =num_rows), )
rest_data.insert(4, "crowdedness", random.choices(['quiet', 'busy'], k=num_rows), )
rest_data.insert(4, "length of stay", random.choices(['short', 'long'], k=num_rows))
# save to new csv file
rest_data.to_csv('./data/restaurant_info_mod.csv', sep=',')
# use modified data
restaurant_info_df = pd.read_csv('./data/restaurant_info_mod.csv', sep=',')
# filename = get_next_filename()

def get_user_data(version, file):
    
    if version== 'tts':
        choice = True
    else:
        choice = False

    restaurant = Restaurant(allow_restart=True, caps=False, restaurant_info_df= restaurant_info_df, tts=choice, filename= file)
    restaurant.run_system()
    answers = questionaire()
    
    with open(file, 'a') as results:
        results.write(f"\n{version} \n {str(answers)}\n")


choices= ['tts', 'simple']

if consent():
    filename = get_next_filename()
    # randomize order of the 2 versions
    choice= random.choice(choices)
    get_user_data(choice, filename)

    choices.remove(choice)
    get_user_data(choices[0], filename)
    