from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "body", "slug", "category", "owner", "created", "updated"]
        read_only_fields = ["slug", "created", "updated", "owner"]  # owner should be read-only

    def create(self, validated_data):
        # ✅ Attach owner from context
        owner = self.context["request"].user
        return Note.objects.create(owner=owner, **validated_data)
