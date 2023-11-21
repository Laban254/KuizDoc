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
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import PyPDF2


class uploadDoc(viewsets.ModelViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = DocumentsSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class summalizedoc will handle the get summalize request, the user will send the document id and the function will return the summalized content, 
# the function will use the openai api to summalize the document
# the function will return the summalized content
# the function will take the document id as a parameter

class summalizedoc(APIView):
    def get(self, request, id, format=None):
        """
        get the document id
        read the document content
        split the document content into chunks of 2048 characters
        send each chunk to the openai api to summalize it
        return the summalized content

        args:
            id: document id

        return:
            summalized content
        """
        #openai.api_key = os.environ.get('OPENAI_API_KEY')
       
        client = OpenAI(api_key="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")


        # try:
        #     document = Documents.objects.get(Documentid=id)

        #     document_content = self.read_pdf(document.file)
        # except Documents.DoesNotExist:
        #     return Response({"error": "No document found"}, status=404)

        # summaries = []

        # for chunk in self.split_text(document_content):
        #     response = openai.Completion.create(
        #         engine="text-davinci-002",
        #         prompt=f"{chunk}\n\nSummarize:",
        #         max_tokens=150
        #     )
        #     summaries.append(response.choices[0].text.strip())

        # return Response({"summaries": summaries})

        try:
            document = Documents.objects.get(Documentid=id)
            document_content = self.read_pdf(document.file)
        except Documents.DoesNotExist:
            return Response({"error": "No document found"}, status=404)

        summaries = []

        for chunk in self.split_text(document_content):
            client = OpenAI(api_key="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")
            GPT_MODEL = "gpt-3.5-turbo-1106"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{chunk}\n\nSummarize:"},
            ],
            response = client.chat.completions.create(
                model=GPT_MODEL,
                messages=messages,
                temperature=0,
                max_tokens=150,
                stop=["\n\n"]
            )
            response_message = response.choices[0].message.content
            summaries.append(response['choices'][0]['message']['content'].strip())
            print(summaries)
            #summaries.append(response_message.strip())

        return Response({"summaries": summaries})


    def split_text(self, text):
        """
        Split the text into chunks of 2048 characters.
        """
        max_chunk_size = 2048
        chunks = []
        current_chunk = ""

        for sentence in text.split("."):
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += sentence + "."
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + "."

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
    
    def read_pdf(self, file_path):
        pdf_file_obj = open(file_path.path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        text = ""
        for page_obj in pdf_reader.pages:
            text += page_obj.extract_text()

        pdf_file_obj.close()
        return text
