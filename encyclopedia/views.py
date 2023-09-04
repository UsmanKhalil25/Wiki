from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import choice

from . import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request,TITLE):
    content = util.get_entry(TITLE)
    if content:
        return render(request,"encyclopedia/content.html",{
            "title":TITLE,
            "content": markdown2.markdown(content)
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"This page does not exist"
        })


def search(request):
    query = request.GET["q"]
    content = util.get_entry(query)

    if content:
        return HttpResponseRedirect(reverse("title",args=[query]))
    else:
        entries = util.list_entries()
        possibleResults = []
        for entry in entries:
            if query.lower() in entry.lower():
                possibleResults.append(entry)
        empty = False
        if len(possibleResults) == 0:
            empty = True
        return render(request,"encyclopedia/search.html",{
            "title": query,
            "entries":possibleResults,
            "empty" :empty
        })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={"class": "form-control w-75"}))
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={"class":"form-control w-75 mt-2 h-75"}))

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            if(util.get_entry(title)):
                return render(request,"encyclopedia/error.html",{
                    "message":"Page already exists"
                })
            else:
                util.save_entry(title,description)
                return HttpResponseRedirect(reverse("title",args=[title]))
    else:
        form = NewPageForm()
        return render(request,"encyclopedia/newpage.html",{
            "form":form
        })



class EditPageForm(forms.Form):
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={"class":"form-control w-75 mt-2 h-75"}))
    

def editpage(request, TITLE):
    form = EditPageForm(initial={'description': util.get_entry(TITLE)})

    if request.method == "POST":
        update = EditPageForm(request.POST)
        if update.is_valid():
            newcontent = update.cleaned_data["description"]
            util.save_entry(TITLE, newcontent)
            return HttpResponseRedirect(reverse("title", args=[TITLE]))
    
    else:
    
        return render(request, "encyclopedia/editpage.html", {
            "title": TITLE,
            "form": form
        })


    
def random(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse("title",args=[entry]))
    
