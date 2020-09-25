from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import util
import random
from markdown2 import Markdown

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    encyclopediaEntry = util.get_entry(entry)
    if encyclopediaEntry is None:
        return render(request, "encyclopedia/entrynotfound.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(encyclopediaEntry),
            "entryTitle": entry
        })


def search(request):
    entryStr = request.GET.get('q', '')
    if(util.get_entry(entryStr) is not None):
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': entryStr}))
    else:
        entryList = []
        for entry in util.list_entries():
            if entryStr.lower() in entry.lower():
                entryList.append(entry)
        if len(entryList) == 0:
            entryList = util.list_entries()
            return render(request, "encyclopedia/index.html", {
                "entries": entryList,
                "value": entryStr,
                "search": True,
                "isSearchStrAvailable": False
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entryList,
                "value": entryStr,
                "search": True,
                "isSearchStrAvailable": True
            })


def newEntry(request):
    if 'title' in request.POST and request.POST['title']:
        entryTitle = request.POST['title']
        entryDescription = request.POST['description']
        entryExists = util.get_entry(entryTitle)
        if entryExists:
            return render(request, 'encyclopedia/newEntry.html', {
                'error': 'Entry already exists. Please try with a new title'
            })
        else:
            util.save_entry(entryTitle, entryDescription)
            return render(request, "encyclopedia/entry.html", {
                "entry": markdowner.convert(util.get_entry(entryTitle)),
                "entryTitle": entryTitle
            })
    else:
        return render(request, 'encyclopedia/newEntry.html')


def randomEntry(request):
    randomTitle = random.choice(util.list_entries())
    return render(request, 'encyclopedia/entry.html', {
        "entry": markdowner.convert(util.get_entry(randomTitle)),
        "entryTitle": randomTitle
    })


def editEntry(request, title):
    return render(request, 'encyclopedia/editEntry.html', {
        'title': title,
        'editDesc': markdowner.convert(util.get_entry(title))
    })


def saveEntry(request):
    titleEntry = request.POST['title']
    descEntry = request.POST['editDesc']
    util.save_entry(titleEntry, descEntry)
    return render(request, 'encyclopedia/entry.html', {
        "entry": markdowner.convert(util.get_entry(titleEntry)),
        "entryTitle": titleEntry
    })
