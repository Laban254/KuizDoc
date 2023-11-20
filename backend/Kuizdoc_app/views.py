from django.http import HttpResponse
from .models import Documents
from .serializers import DocumentsSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import openai
import os

class DocumentUpload(APIView):
    def post(self, request):
        """
        Upload a document to the database.
        """
        serializer = DocumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        """
        Read the content of the uploaded document, split it into chunks,
        and send the chunks to OpenAI API to get a summary.
        """
        openai.api_key = os.environ.get('OPENAI_API_KEY')

        try:
            document = Documents.objects.latest('uploaded_at')
            document_content = document.content
        except Documents.DoesNotExist:
            return Response({"error": "No document found"}, status=404)

        summaries = []

        for chunk in self.split_text(document_content):
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"{chunk}\n\nSummarize:",
                max_tokens=150
            )
            summaries.append(response.choices[0].text.strip())

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
