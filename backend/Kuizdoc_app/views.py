from django.http import HttpResponse
from django.contrib.auth.models import User as UserAuth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .models import Documents, QuizQuestions, UserAnswers
from django.contrib import messages
from .serializers import DocumentsSerializer, UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import openai
from openai import OpenAI
import os
import random
from corsheaders.middleware import CorsMiddleware
import fitz
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from io import StringIO

class uploadDoc(viewsets.ModelViewSet):
   """
   A viewset for uploading documents.

   Attributes:
       queryset (QuerySet): All documents in the database.
       serializer_class (DocumentsSerializer): The serializer for the documents.
       parser_classes (Tuple): The parsers for the viewset.
   """
   queryset = Documents.objects.all()
   serializer_class = DocumentsSerializer
   parser_classes = (MultiPartParser, FormParser,)

   def post(self, request, *args, **kwargs):
       """
       Handles POST requests for uploading documents.

       Args:
           request (HttpRequest): The HTTP request.
           *args: Variable length argument list.
           **kwargs: Arbitrary keyword arguments.

       Returns:
           HttpResponse: The HTTP response.
       """
       file_serializer = DocumentsSerializer(data=request.data)
       if file_serializer.is_valid():
           file_serializer.save()
           return Response(file_serializer.data, status=status.HTTP_201_CREATED)
       else:
           return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class summalizedoc(APIView):
   """
   A view for summarizing documents.

   Attributes:
       None
   """
   def get(self, request, id, format=None):
       """
       Handles GET requests for summarizing documents.

       Args:
           request (HttpRequest): The HTTP request.
           id (int): The ID of the document to summarize.
           format (str): The format of the response.

       Returns:
           HttpResponse: The HTTP response.
       """
       try:
           document = Documents.objects.get(Documentid=id)
           document_content = self.read_pdf(document.file)
           cleaned_text = self.clean_text(document_content)
       except Documents.DoesNotExist:
           return Response({"error": "No document found"}, status=404)

       summaries = self.summarize_text(cleaned_text, question=False, generate=False)
       return Response({"summaries": summaries})

   def clean_text(self, text):
       """
       Cleans the text by replacing special characters with spaces.

       Args:
           text (str): The text to clean.

       Returns:
           str: The cleaned text.
       """
       cleaned_text = text.replace('\n', ' ')
       cleaned_text = cleaned_text.replace('\t', ' ')
       cleaned_text = cleaned_text.replace('\r', ' ')
       cleaned_text = cleaned_text.replace('\x0c', ' ')
       cleaned_text = cleaned_text.replace('\x0b', ' ')
       cleaned_text = cleaned_text.replace('\x0e', ' ')
       cleaned_text = cleaned_text.replace('\x0f', ' ')
       cleaned_text = cleaned_text.replace('\x10', ' ')
       cleaned_text = cleaned_text.replace('\x11', ' ')
       cleaned_text = cleaned_text.replace('\x12', ' ')
       cleaned_text = cleaned_text.replace('\x13', ' ')
       cleaned_text = cleaned_text.replace('\x14', ' ')
       cleaned_text = cleaned_text.replace('\x15', ' ')
       cleaned_text = cleaned_text.replace('\x16', ' ')
       cleaned_text = cleaned_text.replace('\x17', ' ')
       cleaned_text = cleaned_text.replace('\x18', ' ')
       return cleaned_text

   def summarize_text(self, text, question, generate, chunk_size=5000):
       """
       Summarizes the text using the OpenAI GPT-3.5-turbo-1106 model.

       Args:
           text (str): The text to summarize.
           chunk_size (int): The size of the chunks to split the text into.

       Returns:
           list: The summaries of the text.
       """
       summaries = []
       openai_client = OpenAI(api_key="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")

       for chunk in self.split_text(text, chunk_size):
           GPT_MODEL = "gpt-3.5-turbo-1106"
           if question:
               messages = [
                   {"role": "system", "content": "You are a helpful assistant."},
                   {"role": "user", "content": f"{chunk}\n\nSummarize:"},
                   {"role": "user", "content": f"{question}"},
               ]
           elif generate:
                messages = [
                     {"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": f"{chunk}\n\nSummarize:"},
                     {"role": "user", "content": f"Generate {generate} sample questions:"},
                ]
           else:    
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{chunk}\n\nSummarize:"},
                ]

           response = openai_client.chat.completions.create(
               model=GPT_MODEL,
               messages=messages,
               temperature=0,
               max_tokens=150,
               stop=["\n\n"]
           )

           summaries.append(response.choices[0].message.content.strip())
       print(f"The summaries are {summaries}")
       return summaries
   def split_text(self, text, chunk_size=5000):
    print(f"Splinting text into chunks of {chunk_size} characters")
    """
        Splits the text into chunks of a specified size.

        Args:
            text (str): The text to split.
            chunk_size (int): The size of the chunks.

        Returns:
            list: The chunks of text.
    """
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:

        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                print(f"The chunk is {chunk}")
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks
   def read_pdf(self, file_path):
      
      """
      Reads the content of a PDF file.

      Args:
          file_path (str): The path of the PDF file.

      Returns:
          str: The content of the PDF file.
      """
      context = ""
      with fitz.open(file_path.path) as pdf_file:
          num_pages = pdf_file.page_count
          for page_num in range(num_pages):
              page = pdf_file[page_num]
              page_text = page.get_text()
              context += page_text
      print(f"The pdf Context is {context}")
      return context
      
class GenerateQuiz(summalizedoc):


    def post(self, request, *args, **kwargs):
        """
        return HttpResponse('This is a POST request')
        """
        id = kwargs.get('id')
        try:
              document = Documents.objects.get(Documentid=id)
              document_content = self.read_pdf(document.file)
              cleaned_text = self.clean_text(document_content)
        except Documents.DoesNotExist:
              return Response({"error": "No document found"}, status=404)
        questions = self.summarize_text(cleaned_text, generate=5, question=False)
        return Response({"questions": questions})


    # def generate_questions(self, text, num_questions=5):
    #     """
    #     Generates questions from the text using the OpenAI GPT-3.5-turbo-1106 model.

    #     Args:
    #         text (str): The text to generate questions from.
    #         num_questions (int): The number of questions to generate.

    #     Returns:
    #         list: The generated questions.
    #     """
    #     questions = []

    #     # Replace "your_openai_api_key" with your actual OpenAI API key
    #     openai_client = OpenAI(api_key="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")

    #     GPT_MODEL = "gpt-3.5-turbo-1106"
        
    #     # Prepare messages for the OpenAI GPT-3.5-turbo model
    #     messages = [
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": f"{text}\n\nGenerate {num_questions} questions:"},
    #     ]

    #     # Request question generation from OpenAI GPT-3.5-turbo
    #     response = openai_client.chat.completions.create(
    #         model=GPT_MODEL,
    #         messages=messages,
    #         temperature=0,
    #         max_tokens=100,
    #         stop=["\n\n"]
    #     )

    #     # Extract and split the generated questions
    #     generated_questions = response.choices[0].message.content.strip().split("\n")

    #     # Define a basic question structure
    #     question_template = {
    #         "QuestionText": "",
    #         "OptionA": "Option A",
    #         "OptionB": "Option B",
    #         "OptionC": "Option C",
    #         "OptionD": "Option D",
    #         "Answer": "Answer"
    #     }

    #     # Iterate over the generated questions
    #     for generated_question in generated_questions:
    #         # Update the question text in the template
    #         question_template["QuestionText"] = generated_question.strip()
            
    #         # Add the modified question to the list of questions
    #         questions.append(question_template.copy())

    #     return questions
class AnswerQuiz(summalizedoc):


    def post(self, request, *args, **kwargs):
        """
        return HttpResponse('This is a POST request')
        """
        question = kwargs.get('question')
        id = kwargs.get('id')
        try:
              document = Documents.objects.get(Documentid=id)
              document_content = self.read_pdf(document.file)
              cleaned_text = self.clean_text(document_content)
        except Documents.DoesNotExist:
              return Response({"error": "No document found"}, status=404)
        answer = self.summarize_text(cleaned_text, generate=False, question=question)
        return Response({"answer": answer})

class UserSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # Create a new user based on the serializer data
            # user = .objects.create_user(
            #     username=serializer.validated_data['username'],
            #     email=serializer.validated_data['email'],
            #     password=serializer.validated_data['password']
            # )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(f"/user/{request.user.email}")
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        file_serializer = UserLoginSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if user:
            login(request, user)
            first_name = user.first_name
            print(f"Welcome to Kuizdoc!{first_name}")
            return redirect("upload/")
        else:
            return render(request, self.template_name, {'error_message': 'Wrong email or password. Try again'})

class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')
