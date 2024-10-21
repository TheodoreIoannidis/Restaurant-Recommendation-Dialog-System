# Restaurant-Recommendation-Dialog-System
Dialog system which recommends restaurants in Cambridge, based on the user's preferences.

The user can specify the food type, pricerange and area of the restaurant he is looking for in any order. If the user does not specify all the information, the system will proceed to ask for the remaining preferences. After all info is specified, the system will ask the user for any additional requirements he may have (e.g. suitable for children, assigned seats, touristic, romantic). The user can restart the procedure by typing 'restart'.

The system then filters all Cambridge restaurants, finds the ones which satisfy the user's requirements and gives a recommendation if there are any. The user can then ask for the recommended restaurant's adress, phone number or postal code.

The system has some configurability: 
  a) Text to speech.
  
  b) Capitalized output (turn on/off caps).
  
  c) Restarting (enable/disable restart).

Because the system was used in an experiment, after each session, the user is required to answer to some questions regarding the use of the system with and without text to speech. 
The dialog and answers to the questionnaire are saved in a text file.
