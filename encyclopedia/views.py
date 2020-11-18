from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(label="Markdown content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
    # Search for md file with provided TITLE
    content = util.get_entry(TITLE)
    
    # If found, convert to html 
    if content:
        content = Markdown().convert(content)
    
    # Else, set page content to not found
    else:
        content = "<p>Sorry, couldn't find entry.<p>"
        TITLE = "Not found"
    
    # Return page with content as parameter
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": TITLE.capitalize()
    })

def search(request):

    # Get q param (lowered) from get request from form
    q = request.GET.get('q', '').lower()
    
    # Get list of entries
    entries = util.list_entries()
    
    # Compare if q (lowered) in entries list(lowered)
    if q in [entry.lower() for entry in entries]:
        
        # If it is, there is that entry, redirect to entry path
        return HttpResponseRedirect(reverse("entry", kwargs={'TITLE': q}))
    
    else:
        # If it isn't, render a page that displays a list with 
        # entry titles that contain q as a substring (eventually
        # empty)

        matchs=[]
        for entry in entries:
            if q in entry.lower():
                matchs.append(entry)

        return render(request, "encyclopedia/search.html", {
            "q": q,
            "matchs": matchs
        })

def new(request):
    # If user is acessing through a post request
    if request.method == "POST":
        
        # Pass contents posted from form to a form object
        form = NewPageForm(request.POST)

        # Apply method to form object to check validation
        # and get params if valid
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Get list of entries
            entries = util.list_entries()
            
            # Compare if title is already taken
            if title.lower() in [entry.lower() for entry in entries]:
                return render(request, "encyclopedia/entry.html", {
                    "content": "<p>Sorry, entry already exists.<p>",
                    "title": "Already exists" 
                })

            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'TITLE': title}))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    # User acessed page through get request
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewPageForm()
        })

def edit(request, title):

    # User acessed page through get request
    if request.method == "GET":
        form = EditPageForm(initial={'content': util.get_entry(title)}, auto_id=False)
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })

    # User acessed page through post request
    else:
        form = EditPageForm(request.POST)

        # Apply method to form object to check validation
        # and get params if valid
        if form.is_valid():
            content = form.cleaned_data['content']
            
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("entry", kwargs={'TITLE': title}))
        
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })

def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={'TITLE': title}))