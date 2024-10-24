from .preprocessor import Preprocessor
import pandas as pd
import pyttsx3


def infer_columns(row):
    """
    Rules to infer new columns of restaurant dataframe
    """
    touristic, children, romantic, assigned_seats = None, None, None, None

    if row["pricerange"] == "cheap" and row["food quality"] == "good":
        touristic = True
    elif row["food"] == "romanian":
        touristic = False

    if row["length of stay"] == "long":
        children = False
        romantic = True
    else:
        children = True

    if row["crowdedness"] == "busy":
        assigned_seats = True
        romantic = False  # busy overrules long stay
    else:
        assigned_seats = False
    result = pd.Series([touristic, children, romantic, assigned_seats],
                       index=["touristic", "children", "romantic", "assigned seats"])

    return result


def all_info_retrieved(dictionary):
    """
    check if all ditionary values are not None
    """
    return all(value is not None for value in dictionary.values())

class SystemMessageGenerator:
    """
    generates system responses and implements transitions between states
    """

    def __init__(self, info_dict, additional_dict, restaurant_info_df, tts=True, state=0, caps=False, filename=None):
        self.preprocessor = Preprocessor()
        self.info_dict = info_dict
        self.additional_dict = additional_dict
        self.restaurant_info_df = restaurant_info_df
        self.propositions = restaurant_info_df.copy(deep=True)
        self.recommendation = None
        self.filename = filename
        self.curr_state = state
        self.caps = caps
        self.tts = tts
        self.question_dict = {
            "greeting": "Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?",
            "pricerange": "What is the price range?",
            "area": "What part of town do you have in mind?",
            "food": "What kind of food would you like?",
            "additional": "Do you have additional requirements?",
        }
        self.requests_keywords = {
            "address": "addr",
            "phone number": "phone",
            "phone": "phone",
            "postcode": "postcode",
            "code": "postcode",
        }
        self.rulebase = {
            "assigned seats": "it is busy",
            "romantic": "it is not busy and you can stay for a long time",
            "touristic": "the food quality is good and the prices are cheap",
            "children": "the length of stay is short",
        }

    def _give_response(self, response):
        response_pr = f"system: {response}"
        print(response_pr if not self.caps else response_pr.upper())

        with open(self.filename, 'a') as d:
            d.write(f"\n{response_pr}")

        if self.tts:
            speaker = pyttsx3.init()
            speaker.say(response)
            speaker.runAndWait()

    def _get_propositions(self):
        """
        get propositions based on current info dict
        """
        # Check what the user cares about and build query
        # Check what the user cares about and build query
        query = pd.Series([True] * len(self.propositions))

        if self.info_dict["food"] != "dontcare":
            query &= (self.propositions['food'] == self.info_dict['food'])
        if self.info_dict["pricerange"] != "dontcare":
            query &= (self.propositions['pricerange'] == self.info_dict['pricerange'])
        if self.info_dict["area"] != "dontcare":
            query &= (self.propositions['area'] == self.info_dict['area'])

        # if any restaurants satisfy all preferences
        if query.any():
            self.propositions = self.propositions[query]
        else:
            self._give_response("No restaurants found.")
            self.propositions = self.restaurant_info_df
            self.curr_state = 1

    def _print_proposition(self):
        """
        get recommendation from current propositions
        """
        if self.propositions.empty:
            self._give_response("No propositions found.")
            self.info_dict.update({"pricerange": None, "area": None, "food": None})
            self.additional_dict.update({"touristic": None, "romantic": None, "children": None, "assigned seats": None})
            self.curr_state = 1
            self.recommendation = None
            self.propositions = self.restaurant_info_df
            return

        # if user doesn't have additional preferences return first row
        self.recommendation = self.propositions.iloc[0]
        self.candidates = self.propositions

        note = ""
        add = False
        # check additional info dict for specified preferences
        for key, value in self.additional_dict.items():
            if value == "care":
                # get propositions that satisfy preference
                self.candidates = self.propositions[self.propositions[key]]
                add = True
                break

        if not self.candidates.empty:
            # recommend first candidate
            self.recommendation = self.candidates.iloc[0]
        else:
            self._give_response("I didn't find any restaurant with these additional requirements.")
            self.info_dict.update({"pricerange": None, "area": None, "food": None})
            self.additional_dict.update({"touristic": None, "romantic": None, "children": None, "assigned seats": None})
            self.curr_state = 1
            self.recommendation = None
            self.propositions = self.restaurant_info_df
            self.candidates = None
            return

        if add:
            # add extra preference sentence to system output
            if key == "touristic" and self.recommendation[key]:
                contradiction = f" even though the food is romanian," if self.recommendation[
                                                                             "food"] == "romanian" else ""
                note = f"It is also {key}, as you requested, because {contradiction} {self.rulebase[key]}."
            elif key == "romantic" and self.recommendation[key]:
                note = f"It is also {key}, as you requested, because {self.rulebase[key]}."
            elif key == "assigned seats" and self.recommendation[key]:
                note = f"It also has assigned seats, as you requested, because{self.rulebase[key]}."
            elif key == "children" and self.recommendation[key]:
                note = f"It is also suitable for children, as you requested, because {self.rulebase[key]}."
                # if no such restaurants
            else:
                no_match = "I didn't find any restaurant with these additional requirements."
                self._give_response(no_match)
                self.info_dict.update({"pricerange": None, "area": None, "food": None})
                self.additional_dict.update(
                    {"touristic": None, "romantic": None, "children": None, "assigned seats": None})
                self.curr_state = 1
                self.recommendation = None
                self.propositions = self.restaurant_info_df
                self.candidates = None
                return

        foodtype_str = self.recommendation['food'] if 'food' in self.recommendation[
            'food'] else f"{self.recommendation['food']} food"
        # system's response
        recommendation_str = f"{(self.recommendation['restaurantname']).capitalize()} is a nice restaurant in the {self.recommendation['area']} of town serving {foodtype_str} and the prices are {self.recommendation['pricerange']}. {note}"
        self._give_response(recommendation_str)
        self.curr_state = 4

    def _make_confirmation_question(self):

        extra1, extra2 = "", ""
        for key, value in self.additional_dict.items():
            if value == "care":
                if key in ["touristic", "romantic"]:
                    extra1 = f" and {key}"
                elif key in ["assigned seats"]:
                    extra2 = f" with {key}"
                elif key in ["children"]:
                    extra2 = " where you can bring your children,"
                break
        conf_question = f"You are looking for a {self.info_dict['food']}{extra1} restaurant{extra2} in {self.info_dict['area']} part of town where the prices are {self.info_dict['pricerange']}?"
        self._give_response(conf_question)

    def _fit_propositions(self):
        """
        Apply rules to the system's propositions and infer values for the 4 new columns
        """
        self.propositions.loc[:, ["touristic", "children", "romantic", "assigned seats"]] = self.propositions.apply(
            infer_columns, axis=1)

    def _additional(self, user_input):
        """
        Method to fill in the additional dictionary
        """
        for key, value in self.additional_dict.items():
            if key in user_input:
                self.additional_dict[key] = "care"
                break

    def make_greeting(self):
        self._give_response(self.question_dict["greeting"])

    def generate_next_step(self, predicted_intent, user_input, state=0, restart=False):
        """
        State transition function.
        """
        with open(self.filename, "a") as d:
            d.write(f"\n user: {user_input}")

        if "turn on caps" in user_input.lower():
            self.caps = True
            self._give_response("CAPS LOCK IS NOW ON.")
        elif "turn off caps" in user_input.lower():
            self.caps = False
            self._give_response("Caps lock is off.")
        elif "enable restart" in user_input.lower():
            self.allow_restart = True
            self._give_response("Restarts enabled.")
        elif "disable restart" in user_input.lower():
            self.allow_restart = False
            self._give_response("Restarts disabled.")

        self.curr_state = state

        # if user wants to restart, or state 1, empty both dictionaries and greet
        if restart or self.curr_state == 1:
            self.make_greeting()
            self.info_dict.update({"pricerange": None, "area": None, "food": None})
            self.additional_dict.update({"touristic": None, "romantic": None, "children": None, "assigned seats": None})
            self.recommendation = None
            self.propositions = self.restaurant_info_df
            self.curr_state = 2
            return

        if self.curr_state == 2:
            if not all_info_retrieved(self.info_dict):
                # else ask for missing information
                for key, value in self.info_dict.items():
                    if value is None:
                        self._give_response(self.question_dict[key])
                        break
            else:
                self.curr_state = 3

        if self.curr_state == 3:

            if not all_info_retrieved(self.additional_dict):
                self._give_response(self.question_dict["additional"])

                # use info dict to get initial propositions
                self._get_propositions()
                # apply rules and create new columns for additional requirements
                self._fit_propositions()
                # initialize additional dict and  ask if user has additional requirements
                self.additional_dict.update({"touristic": "dontcare", "romantic": "dontcare", "children": "dontcare",
                                             "assigned seats": "dontcare"})
            else:
                # fill additional dictionary
                self._additional(user_input)
                # if both dictionaries are filled print recommendation
                self.curr_state = 4
                self._print_proposition()
            return

        if self.curr_state == 4:

            # if user asks for other info
            if predicted_intent == "request":
                for key, value in self.requests_keywords.items():
                    if key in user_input or value in user_input:
                        if self.recommendation[value] is not None:
                            str_req = f"The {key} of {self.recommendation['restaurantname']} is {self.recommendation[value]}."
                            self._give_response(str_req)
                            break
                        else:
                            self._give_response("I do not have this information.")
                            break

            elif predicted_intent == "bye":
                self.curr_state = 5

                # if they ask for alternatives
            elif predicted_intent in ["reqmore", "reqalts"]:
                if self.candidates is not None and self.candidates.shape[0] > 1:
                    self._give_response("Other options are:\n")
                    for i, row in self.candidates.iloc[1:].iterrows():
                        string = f"{row['restaurantname']} is in the {row['area']} part of town, it serves {row['food']} food and the prices are {row['pricerange']}."
                        self._give_response(string)
                    self.candidates = None
                    self.curr_state = 4
                else:
                    self._give_response("No more options available.")
            return
