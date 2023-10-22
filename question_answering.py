from transformers import pipeline

model_name = "distilbert-base-cased-distilled-squad"  # Specify the model name
qa_pipeline = pipeline("question-answering", model=model_name)

# Now you can use qa_pipeline for question-answering with the specified model.

def answer_question(context, question):
    qa_pipeline = pipeline("question-answering")
    result = qa_pipeline(question=question, context=context)
    return result['answer']