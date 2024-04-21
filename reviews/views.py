from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    name = "world"
    # search = request.GET.get("search") or "</html>"
    # name = "world"
    # search = request.GET.get("search")
    # invalid_name =
    # name = HttpResponse
    # return HttpResponse("Hello, {}!".format(name))
    # , HttpResponse("{}".format(search))
    #return HttpResponse(name)
    return render(request, "base.html", {"name": name})

def searchResult(request):
    search = request.GET.get("search") or "</html>"

    return render(request, "searchResult.html", {"search": search})

