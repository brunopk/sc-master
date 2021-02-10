from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from app.models import scrpi_client
from app.serializers.commands.scrpi_status_resp import CmdScRpiStatusResp
from app.serializers.generic.resp_error import RespError
from app.models import ApiError as ScRpiError, NotConnected
from app.decorators import catch_errors


# TODO: get led_number with scrpi_client (same response fields as scrpi_status)

class CmdScRpiStatus(APIView):

    permission_classes = [TokenHasReadWriteScope]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CmdScRpiStatusResp(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: RespError()
        }
    )
    @catch_errors()
    def patch(self, _):
        # No puede ser un scrpi error
        if scrpi_client.last_error is not None:
            serialized_response = CmdScRpiStatusResp(data={
                'led_number': 300,
                'is_error': True,
                'last_exception': scrpi_client.last_error.__class__.__name__
            })
        else:
            try:
                scrpi_client.ping()
            except ScRpiError:
                serialized_response = CmdScRpiStatusResp(data={
                    'led_number': 300,
                    'is_error': False
                })
            except Exception as e:
                if isinstance(e, NotConnected) or isinstance(e, BrokenPipeError) or isinstance(e, ConnectionResetError):
                    serialized_response = CmdScRpiStatusResp(data={
                        'led_number': 300,
                        'is_error': True,
                        'last_exception': e.__class__.__name__
                    })
                # Other exceptions are cached by
                else:
                    raise e

        # Masks exception (like exceptions serializing response) to avoid being cached by
        # catch_errors decorators (for instance NotConnected -> Exception)
        try:
            serialized_response.is_valid(raise_exception=True)
        except Exception:
            raise Exception()
        return Response(serialized_response.data, status=status.HTTP_200_OK)

