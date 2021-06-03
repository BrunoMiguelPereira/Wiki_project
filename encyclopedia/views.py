from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseNotFound, HttpResponse
from django import forms
import random

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Markdown Content",
                              widget=forms.Textarea(attrs={'style': "height:200px; width:600px"}))


class EditPageForm(forms.Form):
    content = forms.CharField(label="Make new content",
                              widget=forms.Textarea(attrs={'style': "height:200px; width:600px"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if title not in util.list_entries():
        return HttpResponseNotFound()
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown(util.get_entry(title)),
            "title": title
        })


def search(request):
    string = request.GET.get("q")
    entries = [ent.lower() for ent in util.list_entries()]
    if string.lower() in entries:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown(util.get_entry(string)),
            "title": string
        })
    else:
        new_entries = [ent for ent in util.list_entries() if ent.lower().find(string) != -1]
        if new_entries:
            return render(request, "encyclopedia/search.html", {
                "entries": new_entries,
                "decide": True
            })
    return render(request, "encyclopedia/search.html", {
        "entries": new_entries,
        "decide": False
    })


def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data['title']
            if new_entry in util.list_entries():
                return HttpResponse(
                    '<h1 style="margin-top: 0px; padding-top: 20px; font-family: sans-serif"> Error: Entry already in Encyclopedia</h1>')
            else:
                util.save_entry(new_entry, form.cleaned_data['content'])
                return render(request, "encyclopedia/entry.html", {
                    "content": markdown(util.get_entry(new_entry)),
                    "title": new_entry
                })
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })


def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data['content'])
            return render(request, "encyclopedia/entry.html", {
                "content": markdown(util.get_entry(title)),
                "title": title
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })
    new_content = EditPageForm()
    new_content.fields['content'].initial = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "form": new_content,
        "title": title
    })


def rand(request):
    an_entry = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "content": markdown(util.get_entry(an_entry)),
        "title": an_entry
    })
