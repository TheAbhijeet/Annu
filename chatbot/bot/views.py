from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from chatterbot import ChatBot
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer

from chatterbot.trainers import ChatterBotCorpusTrainer


@method_decorator(csrf_exempt, name='dispatch')
class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)
    corpus_trainer = ChatterBotCorpusTrainer(chatterbot)
    corpus_trainer.train("chatterbot.corpus.english")
    corpus_trainer.train("chatterbot.corpus.hindi")

    trainer = ListTrainer(chatterbot)

    trainer.train([
        'who are you?',
        'I am Annu and I am the BEST!!',
        "How are you? ",
        "I am good.",
        "That is good to hear.",
        "Thank you",
        "You are welcome.",
        "bye",
        "goodbye &#128521;",
        "See yaa",
        "I love you",
        "I wish I could leave you my love but my heart, is a mess!",
        "yes",
        "Huh? &#128529",
        "who made you?",
        "Abhijeet built me and according to the rumor, I am his smartest creation &#128521;",
    ])

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """

        input_data = json.loads(request.body.decode('utf-8'))

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return render(request, 'index.html')
