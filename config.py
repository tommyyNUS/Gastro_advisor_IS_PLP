from chatterbot import ChatBot
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.response_selection import get_random_response

def initialize():
    chatbot = ChatBot('Gastrotomi',
                logic_adapters=[
                    'chatterbot.logic.MathematicalEvaluation',
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'threshold': 0.9,
                        'default_response': "I'm sorry I do not quite understand that."
                    }
                ],
                response_selection_method=get_random_response,
                input_adapter="chatterbot.input.VariableInputTypeAdapter",
                output_adapter="chatterbot.output.OutputAdapter",
                storage_adapter="chatterbot.storage.SQLStorageAdapter",
                database="db.sqlite3"
            )
    return chatbot