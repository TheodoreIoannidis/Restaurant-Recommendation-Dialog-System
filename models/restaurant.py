import pyttsx3
from .system_info_retriever import SystemInfoRetriever
from .system_message_generator import SystemMessageGenerator
from .intent_predictor import IntentPredictor



class Restaurant:

    """
    restaurant recommendation dialog system. Call method 'run_system()' to start dialog.
    """
    def __init__(self, restaurant_info_df, allow_restart=False, tts= False, caps=False, filename=None):
        self.info_dict = {"food": None, "pricerange": None, "area": None}
        self.additional_dict = {"touristic": None, "romantic": None, "children": None, "assigned seats": None}
        self.restaurant_info_df = restaurant_info_df
        self.user_input = None
        self.curr_state= 1
        self.caps = caps
        self.tts= tts
        self.filename= filename
        self.allow_restart = allow_restart
        self.system_message_generator = SystemMessageGenerator(info_dict= self.info_dict, additional_dict= self.additional_dict,
                                                                restaurant_info_df=self.restaurant_info_df,
                                                                tts=self.tts, caps=self.caps, filename= self.filename)
        self.system_info_retriever = SystemInfoRetriever(self.info_dict, self.restaurant_info_df, caps=self.caps)
        self.intent_predictor = IntentPredictor().prepare_for_exercise()
        
    def run_system(self):

        while True:

            if self.curr_state==1:
                self.system_message_generator.make_greeting()
                self.info_dict.update({"pricerange": None, "area": None, "food": None})
                self.additional_dict.update({"touristic": None, "romantic": None, "children": None, "assigned seats": None})
                self.curr_state = 2  # move to asking preferences

            # if user says bye, end conversation
            if self.curr_state==5:
                break

            # get user input and predict intent
            self.user_input= input('user: ')
            restart = False

            predicted_intent = self.intent_predictor.predict([self.user_input])
            # print(f"speach act: {predicted_intent[0]}" if not self.caps else f"speach act: {predicted_intent[0]}".upper())

            # handle thanks
            if predicted_intent[0] == "thankyou":
                self.system_message_generator._give_response("You're welcome!")
                continue            

            # allow dialog restarts (configurability)
            if self.allow_restart and ("restart" in self.user_input):
                # empty dictionaries and restart
                self.info_dict.update({"pricerange": None, "area":None, "food": None})
                self.additional_dict.update({"touristic": None, "romantic": None, "children": None, "assigned seats": None})
                self.curr_state = 1
                restart = True
                continue

            self.system_info_retriever.get_info_from_input(self.user_input)
            # move to next state
            self.system_message_generator.generate_next_step(predicted_intent=predicted_intent, user_input=self.user_input,
                                                             state=self.curr_state, restart=restart)
            
            self.curr_state = self.system_message_generator.curr_state

        return
