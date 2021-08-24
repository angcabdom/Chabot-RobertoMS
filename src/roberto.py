from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance, JaccardSimilarity
from chatterbot.response_selection import get_first_response

bot_roberto = ChatBot(
    'Roberto',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            'default_response': 'Por favor, reformule su peticion',
            'maximum_similarity_threshold': 0.90
        }
        
    ],
    database_uri='sqlite:///src/db/database.db'
)