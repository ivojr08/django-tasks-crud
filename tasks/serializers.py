from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # ergonomic field for the client: boolean reflecting the status
    # writeable: if client send "done": true/false, convert to status
    # readable: always return calculated done
    done = serializers.BooleanField(required=False)
    owner = serializers.IntegerField(source='owner_id', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'done', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']

    # business rules / validations
    def validate_title(self, value: str):
        value = (value or '').strip()
        if not value:
            raise serializers.ValidationError("Title can't be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Title must have max 200 characters.")
        return value
    
    def validate_status(self, value: str):
        if value not in dict (Task.STATUS_CHOICES):
            raise serializers.ValidationError(
                "Status invalid. Use 'Pending' or 'Completed'."
            )
        return value
    
    def _apply_done_to_status(self, data: dict) -> dict:
        """
        If the payload brings 'done', convert to status:
        done=True -> status='Completed'
        done=False -> status='Pending'
        """
        if 'done' in data:
            done = data.pop('done')
            data['status'] = 'Completed' if done else 'Pending'
        return data
    
    def create(self, validated_data):
        validated_data = self._apply_done_to_status(validated_data)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data = self._apply_done_to_status(validated_data)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        """
        alwaye return 'done' consistent with actual status
        """
        rep = super().to_representation(instance)
        rep['done'] = (instance.status == 'Completed')
        return rep
    