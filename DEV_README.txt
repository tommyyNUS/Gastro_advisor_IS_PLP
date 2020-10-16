Developers Readme:

app.py - flask file with main routine
chatbot folder - all chatbot related scripts and functions
    config.py - can configure confidence level before saying "i dont know what you are saying", now at 90%
    intent.py - all intent logics are housed here
    train_corpus.py - add any new knowledge to chatterbot here! (Append question/answer pair into list side by side)
    db.sqlite3 - All trained data are stored in this sqlite file. The chatbot will not reply anything if this is deleted

to run chatbot, run "python app.py"
to run chatbot in debug mode, run "python app.py -debug"
to train chatterbot corpus, run "python app.py -train"