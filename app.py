from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap 


# NLP Packages
from textblob import TextBlob,Word 
import random 
import time

app = Flask(__name__)
# Using bootstrap to initialize all the stylings 

Bootstrap(app)


# This will be our home page and it will call the index.html file

@app.route('/')
def index():
	return render_template('index.html')

# This is the route we call to perform our analysis and showing the result

@app.route('/analyse',methods=['POST'])
def analyse():
    # Initializing time to check how much time was elapsed

    start = time.time()
    
    # Initializing the summary words to an empty string

    summary = ''
    if request.method == 'POST':
        
        # Recieving the text from the front end

        rawtext = request.form['rawtext']

        #NLP using TextBlob

        blob = TextBlob(rawtext)
        received_text2 = blob
        
        '''

        Finding out the sentiment and subjectivity of the text.

        Subjectivity (ranges from 0 to 1) : 0 is objective 1 is subjective
        Sentiment (ranges from -1 to 1): -1 is very negative, 0 is neutral and 1 is positive sentiment

        '''
        blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity

        # Finding out the number of words without punctuation and white spaces

        number_of_tokens = len(list(blob.words))

        # Extracting the main points by finding the nouns from the text

        nouns = list()        
        for word, tag in blob.tags:
            if tag == 'NN':
                
                '''
                
                Lemmatize method in TextBlob is used to find the rootword given a single word.

                Example: Word('radii').lemmatize() will return 'radius'
                         Word('went').lemmatize() will return 'go'                
                
                '''
                nouns.append(word.lemmatize())
                rand_words = random.sample(nouns,len(nouns))
                final_word = list()
                for item in rand_words:
                    final_word.append(word)
                    summary = final_word
    end = time.time()
    final_time = end-start


    return render_template('index.html',received_text = received_text2,number_of_tokens=number_of_tokens,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity,summary=summary,final_time=final_time)






if __name__ == '__main__':
	app.run(debug=True)