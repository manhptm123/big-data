# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import numpy as np
# from scipy.special import softmax
# tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")

# model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")

# # print(model(**tokenizer('cool',return_tensors='pt')))

# def sentimentAnylasis(model,tokenizer,text):
#     scores = model(**tokenizer(text,return_tensors='pt'))
#     scores = scores[0][0].detach().numpy()
#     scores = softmax(scores)
#     ranking = np.argsort(scores)
#     print(scores)
#     print(ranking)
#     if ranking[-1] == 0: 
#         return "NEG"
#     if ranking[-1] == 1:
#         return "NEU"
#     return 'POS'

# # print(sentimentAnylasis(model,tokenizer,'very good'))