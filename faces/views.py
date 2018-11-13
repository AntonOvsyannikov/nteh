# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .services import *
from .forms import *


def misc(request):
    error = ''
    gl = ''
    try:
        gl = get_gallery_list()
    except Exception as e:
        error = unicode(e)

    return render(
        request,
        'faces/misc.html',
        {
            'response': unicode(gl),
            'error': error,
        }
    )


def face_add(request):
    if request.method == 'POST':

        form = AddFaceForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                face = create_face(request.FILES['photo'], json.dumps({'name':form.cleaned_data['name']}))
                return redirect('faces:face_detail', face['id'])
            except ServiceException as e:
                form.add_error(None, unicode(e))

    else:
        form = AddFaceForm()

    return render(request, 'faces/face_add.html', {'form': form})


def _json_meta(f):
    try:
        f['meta'] = json.loads(f['meta'])
    except ValueError:
        pass

    return f

def _digforname(f):

    f =_json_meta(f)

    m = f['meta']

    if isinstance(m, (str, unicode)):
        f['name'] = m
    else:
        try:
            f['name'] = m['name']
        except (KeyError, TypeError):
            f['name'] = 'Неизвестный'
    return f

def _digfornames(faces):
    return map(_digforname, faces)

def face_list(request):
    return render(request, 'faces/face_list.html',
                  {'face_list': _digfornames(list_faces()), 'delete': True})

def face_detail(request, _id):
    return render(request, 'faces/face_detail.html', {'face': _digforname(get_face(_id))})


def face_delete(request, _id):
    delete_face(_id)
    return redirect('faces:face_list')


def find(request):
    if request.method == 'POST':
        form = FindFaceForm(request.POST, request.FILES)

        if form.is_valid():


            try:
                faces = _digfornames(
                    identify_face(
                        form.cleaned_data['url'] or request.FILES['photo'],
                        form.cleaned_data['n'],
                        form.cleaned_data['threshold']
                    )
                )

                for f in faces:
                    try:
                        if float(f['confidence']) < 0.9:
                            f['lowconfidence'] = '1'
                    except KeyError:
                        pass

                return render(request, 'faces/face_list.html', {'face_list': faces })
            except ServiceException as e:
                form.add_error(None, unicode(e))

    else:
        form = FindFaceForm()

    return render(request, 'faces/find.html', {'form': form})


def home(request):
    return redirect('faces:face_add')

def clean(request):

    for f in list_faces():
        delete_face(f['id'])

    delete_gallery()

    return redirect('faces:face_add')