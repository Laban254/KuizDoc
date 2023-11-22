from django.http import HttpResponse
from .models import Documents
from .serializers import DocumentsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
import openai
from openai import OpenAI
import os
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

       summaries = self.summarize_text(cleaned_text)
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

   def summarize_text(self, text, chunk_size=5000):
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
