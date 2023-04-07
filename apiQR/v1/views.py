from rest_framework.decorators import api_view
from django.http import HttpResponse
import datetime
import uuid
from v1.createQR import create_qr


@api_view(['GET'])
def get_qr(request):
    data = dict(request.query_params)
    token = data.pop('token', None)
    folder = data.pop('folder', None)

    if not folder is None:
        folder = folder[0]

    if token is None:
        return HttpResponse('error: token error')

    if 'Name' not in data:
        return HttpResponse('error: Name error')

    if 'PersonalAcc' not in data:
        return HttpResponse('error: PersonalAcc error')

    if 'BankName' not in data:
        return HttpResponse('error: BankName error')

    if 'BIC' not in data:
        return HttpResponse('error: BIC error')

    if 'CorrespAcc' not in data:
        return HttpResponse('error: CorrespAcc error')

    try:
        tmp_uuid = uuid.UUID(token[0])
    except ValueError:
        return HttpResponse('error: token error')

    try:
        size = data.pop('size', None)
        if size == None:
            size = 800
        else:
            if not size[0].isdigit():
                return HttpResponse('error: invalid value size')
            else:
                size = int(size[0])

        tmp_data = [f'{el}={data.get(el)[0]}' for el in data]
        qr_str = 'ST00012|' + '|'.join(tmp_data)
        UID = uuid.uuid1()
        date = datetime.datetime.now()
        responce_qr = create_qr(qr_str, token[0], date, UID, size, folder)

        return HttpResponse(responce_qr)
    except:
        return HttpResponse('error: qr generate error')
