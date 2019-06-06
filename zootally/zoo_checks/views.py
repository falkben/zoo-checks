from datetime import date
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import (
    AnimalCountForm,
    BaseAnimalCountFormset,
    BaseSpeciesCountFormset,
    SpeciesCountForm,
)
from .models import Animal, AnimalCount, Exhibit, Species, SpeciesCount


@login_required
# TODO: logins may not be sufficient - they need to be a part of a group
def home(request):
    exhibits = Exhibit.objects.filter(user=request.user)

    return render(request, "home.html", {"exhibits": exhibits})


def get_formset_order(
    exhibit_species, exhibit_animals, species_formset, animals_formset
):
    """
    Creates an order to display the formsets that we can call in the template
    """

    # to set the order
    formset_dict = {}
    anim_total = 0
    for ind, spec in enumerate(exhibit_species):
        spec_anim_list = exhibit_animals.filter(species=spec).order_by("name")
        spec_anim_index = list(range(anim_total, spec_anim_list.count() + anim_total))
        anim_total += spec_anim_list.count()

        # store in dictionary, using id because that's known unique
        formset_dict[spec.id] = {}
        formset_dict[spec.id]["species"] = spec
        formset_dict[spec.id]["formset"] = species_formset[ind]
        formset_dict[spec.id]["animalformset_index"] = zip(
            spec_anim_list, [animals_formset[i] for i in spec_anim_index]
        )

    return formset_dict


@login_required
def count(request, exhibit_id):
    # TODO: counts should default to maximum (across users) for the day
    # TODO: condition should default to median? condition (across users) for the day

    exhibit = get_object_or_404(Exhibit, pk=exhibit_id)
    exhibit_species = exhibit.species.all()
    exhibit_animals = exhibit.animals.all().order_by("species", "name")
    species_counts_today = (
        SpeciesCount.objects.filter(species__in=exhibit_species)
        .filter(datecounted__gte=date.today())
        .order_by("species")
    )

    SpeciesCountFormset = inlineformset_factory(
        Exhibit,
        SpeciesCount,
        form=SpeciesCountForm,
        can_delete=False,
        can_order=False,
        extra=len(exhibit_species),  # exhibit.species.count(),
        formset=BaseSpeciesCountFormset,
        max_num=len(exhibit_species),
    )
    AnimalCountFormset = inlineformset_factory(
        Exhibit,
        AnimalCount,
        form=AnimalCountForm,
        can_delete=False,
        can_order=False,
        extra=len(exhibit_animals),  # exhibit.animals.count(),
        formset=BaseAnimalCountFormset,
        max_num=len(exhibit_animals),
    )

    init_sp_counts = [0] * exhibit_species.count()
    for i, sp in enumerate(exhibit_species):
        sp_count = species_counts_today.filter(species=sp)
        if sp_count.count() > 0:
            init_sp_counts[i] = sp_count.aggregate(Max("count"))["count__max"]

    init_spec = [
        {"species": obj, "datecounted": date.today()} for obj in exhibit_species
    ]
    [init.update({"count": c}) for init, c in zip(init_spec, init_sp_counts)]
    init_anim = [
        {"animal": obj, "datecounted": date.today()} for obj in exhibit_animals
    ]

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        species_formset = SpeciesCountFormset(
            request.POST, request.FILES, instance=exhibit, initial=init_spec
        )
        # TODO: Need to test to make sure we are editing the right animal counts
        animals_formset = AnimalCountFormset(
            request.POST, request.FILES, instance=exhibit, initial=init_anim
        )

        # needed in the case the form wasn't submitted properly and we have to re-render the form
        formset_order = get_formset_order(
            exhibit_species, exhibit_animals, species_formset, animals_formset
        )

        # check whether it's valid:
        if species_formset.is_valid() and animals_formset.is_valid():
            # process the data in form.cleaned_data as required
            for form in species_formset.save():
                form.users.add(request.user)

            for form in animals_formset.save():
                form.users.add(request.user)

            # redirect to a new URL:
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        species_formset = SpeciesCountFormset(instance=exhibit, initial=init_spec)
        animals_formset = AnimalCountFormset(instance=exhibit, initial=init_anim)
        formset_order = get_formset_order(
            exhibit_species, exhibit_animals, species_formset, animals_formset
        )
        # TODO: figure out why we have more forms than we need in species formset

    return render(
        request,
        "tally.html",
        {
            "exhibit": exhibit,
            "exhibit_animals": list(exhibit_animals),
            "exhibit_species": list(exhibit_species),
            "species_formset": species_formset,
            "animals_formset": animals_formset,
            "formset_order": formset_order,
        },
    )
