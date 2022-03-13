import webbrowser
import datetime
import pyjokes
import wikipedia
import pywhatkit

from transformers import AutoTokenizer
from transformers import pipeline
from transformers import AutoModelForQuestionAnswering



class bot:
    def __init__(self):
        self.model = AutoModelForQuestionAnswering.from_pretrained("./roberta_ver3/")
        self.tokenizer = AutoTokenizer.from_pretrained("./roberta_ver3")
        self.nlp = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer)

    def query(self, input):
        q = input.lower()
        if ('open' in q or 'start' in q):
            q = input.lower().replace(" ","")
            q = q.replace("\"","")
            web = q[4:]
            webbrowser.open('https://www.{}.com'.format(web))
            return 'Starting ' + web[0].upper() + web[1:]
        elif ('what time' in q):
            return self.query_time()
        elif ('what day' in q):
            return self.query_day()
        elif ('who are you' in q):
            return 'I\m Hannah, your super cute assistant'
        elif ('i am' in q or 'am i' in q):
            return 'Interesting question, why you don\'t know who you are?'
        elif ('what is' in q or 'who is' in q):
            ans = self.get_answer(q)
            return ans
        elif ('a joke' in q):
            return self.joke()
        elif ('remember' in q):
            data = q[9:]
            remember = open('/home/notta/Study/Coding/Projects/introduction-to-ai-hust/back_end/data.txt', 'w')
            remember.write(data)
            return "Okay, you said me to remember that" + data
        elif ('do you know anything' in q):
            data = open('/home/notta/Study/Coding/Projects/introduction-to-ai-hust/back_end/data.txt', 'r')
            return "Okay, you said me to remember that" + data.read()
        elif ('play song' in q):
            song = q[11:]
            pywhatkit.playonyt(song)
            return "Playing " + song
        elif ('hi' in q or 'hello' in q):
            return self.whatsup()
        elif ('bye' in q):
            return 'Bye, see you again!'
        elif (q == ''):
            return ''
        else:
            return self.get_answer(q)

    def query_day(self):
        day = datetime.date.today()
        print(day)
        weekday = day.weekday()
        print(weekday)
        map = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
            }
        try:
            return  f'Today is {map[weekday]}'
        except:
            pass


    def query_time(self):
        time = datetime.datetime.now().strftime("%I:%M:%S")
        return f"It's {time[0:2]} o'clock and {time[3:5]} minutes"

    def whatsup(self):
        return '''Hola, I am Hannah. I am your personal assistant.
        How may i help you?
        '''
    def joke(self):
        joke = pyjokes.get_joke(language="en", category="neutral")
        return joke

    def get_answer(self, question):
        question = question.lower()
        keyword = question
        if "what is" in question:
            keyword = question[8:]
        elif "who is" in question:
            keyword = question[7:]
        elif "where is" in question:
            keyword = question[9:]
        if "birthday" in keyword:
            keyword = keyword[:-9]
        # print(keyword)
        context = self.get_context(keyword)
        # print(context)
        return self.getanswer(question, context)["answer"]

    def getanswer(self, input, context):
        QA_input = {
            'question': input,
            'context': context
        }
        res = self.nlp(QA_input)
        return res

    def get_context(self, input):
        searched = wikipedia.search(input, results=2, suggestion=False)
        # print(searched)
        context = ""
        for temp in searched:
            context =context + wikipedia.summary(temp, auto_suggest=False)
        # print(context)
        return context