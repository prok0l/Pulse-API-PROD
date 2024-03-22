from rest_framework import serializers


class FriendsSerializer(serializers.Serializer):
    login = serializers.CharField(source="to_user.login")
    addedAt = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['addedAt'] = instance.addedAt.strftime('%Y-%m-%dT%H:%M:%SZ')
        return data
