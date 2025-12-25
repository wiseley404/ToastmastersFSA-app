from django.shortcuts import render, get_object_or_404, redirect
from .models import Form, Response, Submission, Option
from .forms import make_form, FormForm, FieldForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def show_form(request, form_id):
    formulaire = get_object_or_404(Form, id=form_id)
    FormClass = make_form(formulaire)

    submitted = False
    if request.user.is_authenticated:
        submitted = Submission.objects.filter(user=request.user,form=formulaire).exists()
    form_instance = FormClass()


    for field in FormClass().fields.values():
            field.widget.attrs['disabled'] = 'disabled'
    context = {
        'form':form_instance, 
        'is_active': True,
        'is_published': formulaire.is_published,
        'submitted': submitted,
        'formulaire': formulaire
        }
    return render(request, 'forms/show_form.html', context)


@staff_member_required
def edit_form(request, form_id):
    formulaire = get_object_or_404(Form, id=form_id)
    FormClass = make_form(formulaire)
    context = {
        'form': FormClass(),
        'in_creation_mode': True,
        'is_published': formulaire.is_published,
        'formulaire': formulaire
    }
    return render(request, 'forms/show_form.html', context)


@staff_member_required
def confirm_form_deletion(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, 'forms/delete_form.html', {'form': form})


@staff_member_required
def delete_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if form:
        form.delete()
    return redirect('forms_list')


@login_required
def submit_form(request, form_id):
    formulaire = get_object_or_404(Form, id=form_id)
    FormClass = make_form(formulaire)

    if request.method == 'POST':
        form = FormClass(request.POST)

        if form.is_valid():
            submission = Submission.objects.create(
            user=request.user if request.user.is_authenticated else None,
            form=formulaire
        )
            for field in form.fields.all():
                value = form.cleaned_data.get(field.description)
                if isinstance(value, list):
                    for val in value:
                        Response.objects.create(
                            submission=submission,
                            field=field,
                            value=val
                        )
                else:
                    Response.objects.create(
                        submission=submission,
                        field=field,
                        value=value
                    )
            return render(request, "forms/show_form.html", {"submitted_successfully": True})


@staff_member_required
def create_form(request):
    if request.method == "POST":
        form = FormForm(request.POST)
        if form.is_valid():
            formulaire= form.save()
            return HttpResponseRedirect(reverse('edit_form', args=[formulaire.id]))
    else:
        form = FormForm()
    return render(request, 'forms/create_form.html', {'form': form})
    


@staff_member_required
def add_fields(request, form_id):
    formulaire = get_object_or_404(Form, id=form_id)
    formulaire.in_creation_mode = True
    formulaire.save()
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.form = formulaire
            field.save()
            
            if field.type in ['select', 'radio', 'checkbox']:
                options = request.POST.getlist('options')
                for option in options:
                    Option.objects.create(field=field, value=option.strip())
                return HttpResponseRedirect(reverse('edit_form', args=[formulaire.id]))
            else:
                return HttpResponseRedirect(reverse('modifier_formulaire', args=[formulaire.id]))
    else:
        form = FieldForm()
    return render(request, 'forms/add_field.html', {'form': form, 'formulaire': formulaire})


@staff_member_required
def confirm_form_publication(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, 'forms/publish_form.html', {'form': form})


@staff_member_required
def publish_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    form.is_published = True
    form.is_active = True
    form.in_creation_mode = False
    form.save()
    return HttpResponseRedirect(reverse('forms_list'))


@staff_member_required
def confirm_form_closure(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, 'forms/close_form.html', {'form': form})


@staff_member_required
def close_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    form.is_active = False
    form.save()
    return HttpResponseRedirect(reverse('historique_forms'))


@login_required
def show_published_forms_list(request):
    active_published_forms = Form.objects.filter(is_published=True, is_active=True).order_by('-date')
    not_published_forms = Form.objects.filter(is_published=False).order_by('-date')
    return render(request, 'forms/forms_list.html', {
        'active_published_forms': active_published_forms,
        'not_published_forms': not_published_forms,
        'section_active':'votes'
        }
    )


@staff_member_required
def show_historique_forms_list(request):
    inactive_published_forms = Form.objects.filter(is_published=True, is_active=False).order_by('-date')
    return render(request, 'forms/historique_forms.html', {
        'inactive_published_forms': inactive_published_forms
    })


@staff_member_required
def show_results(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, 'forms/show_results.html', {'form':form})




    
