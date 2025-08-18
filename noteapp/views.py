from django.shortcuts import get_object_or_404
from noteapp.models import Note
from noteapp.serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


# 🔍 Search Notes
@api_view(["GET"])
@permission_classes([AllowAny])  # Anyone can search
def search_notes(request):
    query = request.query_params.get("search", "").strip()
    
    if not query:
        return Response({"detail": "Search query cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

    notes = Note.objects.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query) |
        Q(category__icontains=query)
    )
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 📌 List and Create Notes
@api_view(["GET", "POST"])
def notes(request):
    if request.method == "GET":
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required for creating notes."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Attach note to user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📍 Note Detail (GET, UPDATE, DELETE)
@api_view(["GET", "PUT", "DELETE"])
def note_detail(request, slug):
    note = get_object_or_404(Note, slug=slug)

    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required for updating notes."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = NoteSerializer(note, data=request.data, partial=True)  # ✅ allow partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required for deleting notes."}, status=status.HTTP_401_UNAUTHORIZED)

        note.delete()
        return Response({"detail": "Note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
