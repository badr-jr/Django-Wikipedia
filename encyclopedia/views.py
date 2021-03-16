from django.shortcuts import render
import random
from . import util
import markdown2
from markdown2 import Markdown
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.urls import reverse
entries = util.list_entries()
#create textfield for searching
class NewSearchForm(forms.Form):
    search = forms.CharField(label=False, required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))
#create form for adding new entry
class CreateNewForm(forms.Form):
    page_title = forms.CharField(label="Title",required=True,
    widget=forms.TextInput(
    attrs={'placeholder':'Page Title','class':'form-control'}))
    page_content = forms.CharField(label="Content",required=False,
    widget=forms.Textarea(
    attrs={'placeholder':'Content','class':'form-control'}))
class CreateEditForm(forms.Form):
    edit_area = forms.CharField(label=False, required= False,
    widget= forms.Textarea
    ())
form = NewSearchForm()
#this returns the home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form":form,    
    })
#this returns the entry page
def topic(request,name):
    return render(request,"encyclopedia/topic_page.html",{
        "content":get_content(name),
        "title":name,
        "form":form
    })
#this search for specific topic using the exact word of substring of it and return topic page if found 
def search_topic(request):
    if request.method == "POST":
        form=NewSearchForm(request.POST)
        if form.is_valid():
            word=form.cleaned_data["search"]
            if get_content(word) != "<h1> The request page was not found. </h1>":
                return HttpResponseRedirect(reverse("wiki:topic",kwargs={"name":word}))
            results=[]
            for entry in entries:
                if word.lower() in entry.lower():
                    results.append(entry)
            if len(results) != 0:
                return render(request,"encyclopedia/search_results.html",{
                    "results":results,
                    "title":"Search Results",
                    "form":form
                })
            return topic(request,word)
#this creates new entry if it doesn't already exist and redirect to this entry page
def create_page(request):
    create_form=CreateNewForm()
    if request.method=="GET":
        return render(request,"encyclopedia/create_page.html",{
                            "create_form":create_form
        })
    else:
        form=CreateNewForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["page_title"]
            content=form.cleaned_data["page_content"]
            global entries
            for entry in entries:
                if title==entry:
                    return render(request,"encyclopedia/create_page.html",{
                    "create_form":create_form,
                    "error_message":"This page already exists."
        })
            util.save_entry(title,content) 
            entries+=[title]
            return HttpResponseRedirect(reverse("wiki:topic",kwargs={"name":title}))
#this convert the markdown content into html to render it
def get_content(name):
    markdowner = Markdown()
    page = util.get_entry(name)
    if page != None:
        page_converted = markdowner.convert(page)
        return page_converted
    else:
        return "<h1> The request page was not found. </h1>"
#this retruns random topic of the existing entries
def random_page(request):
    global entries
    return HttpResponseRedirect(reverse("wiki:topic",kwargs={"name":random.choice(entries)}))
#
def edit_page(request,word):
    editForm=CreateEditForm()
    editForm.fields["edit_area"].initial=util.get_entry(word)
    if request.method=="GET":
        return render(request,"encyclopedia/edit_page.html",{
            "editForm":editForm,
            "title":word
        })
    else:
        edit_form=CreateEditForm(request.POST)
        if edit_form.is_valid():
            new_entry=edit_form.cleaned_data["edit_area"]
            util.save_entry(word,new_entry)
            return HttpResponseRedirect(reverse("wiki:topic",kwargs={"name":word}))