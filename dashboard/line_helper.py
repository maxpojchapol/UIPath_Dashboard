from django.views.decorators.csrf import csrf_exempt
from Config.LineConfig import *
from django.http.response import JsonResponse
@csrf_exempt
def linewebhook(request):
    if request.method == "POST":
        print(request.body.decode())
        # message = "test"
        # NotifyMessage(message)
        return JsonResponse(200, safe=False)
    if request.method == "GET":
        return JsonResponse("Get method", safe=False)


@csrf_exempt
def NotifyMessage(message):
    LINE_API = "https://api.line.me/v2/bot/message/push"

    Authorization = "Bearer {}".format(Line_accesstoken)
    print(Authorization)
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": Authorization,
    }

    data = {"to": Group_id, "messages": [{"type": "text", "text": message}]}

    data = json.dumps(data)  ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200