from roberto import bot_roberto
from chatterbot.trainers import ChatterBotCorpusTrainer

trainer = ChatterBotCorpusTrainer(bot_roberto)

trainer.train(
    "./src/train/spanish/greetings.yml",
    "./src/train/spanish/despedidas.yml",
    "./src/train/spanish/emociones.yml",
    "./src/train/spanish/IA.yml",
    "./src/train/spanish/perfilbot.yml",
    "./src/train/spanish/psicologia.yml",
    "./src/train/spanish/localizacionesHosp.yml",
    "./src/train/spanish/COVID19.yml",
    "./src/train/spanish/horariosHosp.yml",
    "./src/train/spanish/infoHosp.yml"
)