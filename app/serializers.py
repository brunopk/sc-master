from rest_framework import serializers


class CmdSetColor(serializers.Serializer):

    section_id = serializers.UUIDField(required=False)
    color = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RespOk(serializers.Serializer):

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()


class RespError(serializers.Serializer):

    code = serializers.IntegerField()
    message = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()


class ReqToken(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplemented()

    def create(self, validated_data):
        raise NotImplemented()


class RespToken(serializers.Serializer):

    token = serializers.CharField()
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
