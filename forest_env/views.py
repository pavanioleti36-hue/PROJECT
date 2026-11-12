"""Forest Environment app views — complete CRUD for all models."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Forest, ForestArea, Vegetation, Wildlife, WeatherCondition
from .forms import ForestForm, ForestAreaForm, VegetationForm, WildlifeForm, WeatherConditionForm


# ── Forest ────────────────────────────────────────────────────────
@login_required
def forest_list(request):
    forests = Forest.objects.all()
    return render(request, 'forest_env/forest_list.html',
                  {'forests': forests, 'title': 'Forests'})

@login_required
def forest_detail(request, pk):
    forest = get_object_or_404(Forest, pk=pk)
    areas = forest.areas.all()
    incidents = forest.fire_incidents.order_by('-fire_start_time')[:5]
    return render(request, 'forest_env/forest_detail.html',
                  {'forest': forest, 'areas': areas, 'incidents': incidents, 'title': forest.name})

@login_required
def forest_create(request):
    form = ForestForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Forest added successfully.')
        return redirect('forest_env:forest_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Add Forest', 'action': 'Create'})

@login_required
def forest_update(request, pk):
    forest = get_object_or_404(Forest, pk=pk)
    form = ForestForm(request.POST or None, instance=forest)
    if form.is_valid():
        form.save()
        messages.success(request, 'Forest updated successfully.')
        return redirect('forest_env:forest_detail', pk=forest.pk)
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Edit Forest', 'action': 'Update', 'object': forest})

@login_required
def forest_delete(request, pk):
    forest = get_object_or_404(Forest, pk=pk)
    if request.method == 'POST':
        forest.delete()
        messages.success(request, 'Forest deleted.')
        return redirect('forest_env:forest_list')
    return render(request, 'forest_env/confirm_delete.html',
                  {'object': forest, 'title': 'Delete Forest'})


# ── Forest Area ───────────────────────────────────────────────────
@login_required
def area_list(request):
    areas = ForestArea.objects.select_related('forest').all()
    forest_filter = request.GET.get('forest')
    if forest_filter:
        areas = areas.filter(forest_id=forest_filter)
    forests = Forest.objects.all()
    return render(request, 'forest_env/area_list.html',
                  {'areas': areas, 'forests': forests, 'title': 'Forest Areas',
                   'selected_forest': forest_filter})

@login_required
def area_detail(request, pk):
    area = get_object_or_404(ForestArea, pk=pk)
    nodes = area.sensor_nodes.all()
    weather = area.weather_conditions.order_by('-recorded_at')[:5]
    return render(request, 'forest_env/area_detail.html',
                  {'area': area, 'nodes': nodes, 'weather': weather, 'title': area.name})

@login_required
def area_create(request):
    form = ForestAreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Forest area added successfully.')
        return redirect('forest_env:area_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Add Forest Area', 'action': 'Create'})

@login_required
def area_update(request, pk):
    area = get_object_or_404(ForestArea, pk=pk)
    form = ForestAreaForm(request.POST or None, instance=area)
    if form.is_valid():
        form.save()
        messages.success(request, 'Forest area updated.')
        return redirect('forest_env:area_detail', pk=area.pk)
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Edit Forest Area', 'action': 'Update', 'object': area})

@login_required
def area_delete(request, pk):
    area = get_object_or_404(ForestArea, pk=pk)
    if request.method == 'POST':
        area.delete()
        messages.success(request, 'Forest area deleted.')
        return redirect('forest_env:area_list')
    return render(request, 'forest_env/confirm_delete.html',
                  {'object': area, 'title': 'Delete Forest Area'})


# ── Vegetation ────────────────────────────────────────────────────
@login_required
def vegetation_list(request):
    items = Vegetation.objects.select_related('forest_area__forest').all()
    return render(request, 'forest_env/vegetation_list.html',
                  {'items': items, 'title': 'Vegetation'})

@login_required
def vegetation_create(request):
    form = VegetationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Vegetation record added.')
        return redirect('forest_env:vegetation_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Add Vegetation', 'action': 'Create'})

@login_required
def vegetation_update(request, pk):
    obj = get_object_or_404(Vegetation, pk=pk)
    form = VegetationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Vegetation record updated.')
        return redirect('forest_env:vegetation_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Edit Vegetation', 'action': 'Update', 'object': obj})

@login_required
def vegetation_delete(request, pk):
    obj = get_object_or_404(Vegetation, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Vegetation record deleted.')
        return redirect('forest_env:vegetation_list')
    return render(request, 'forest_env/confirm_delete.html',
                  {'object': obj, 'title': 'Delete Vegetation'})


# ── Wildlife ──────────────────────────────────────────────────────
@login_required
def wildlife_list(request):
    items = Wildlife.objects.select_related('forest_area__forest').all()
    return render(request, 'forest_env/wildlife_list.html',
                  {'items': items, 'title': 'Wildlife'})

@login_required
def wildlife_create(request):
    form = WildlifeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Wildlife record added.')
        return redirect('forest_env:wildlife_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Add Wildlife', 'action': 'Create'})

@login_required
def wildlife_update(request, pk):
    obj = get_object_or_404(Wildlife, pk=pk)
    form = WildlifeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Wildlife record updated.')
        return redirect('forest_env:wildlife_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Edit Wildlife', 'action': 'Update', 'object': obj})

@login_required
def wildlife_delete(request, pk):
    obj = get_object_or_404(Wildlife, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Wildlife record deleted.')
        return redirect('forest_env:wildlife_list')
    return render(request, 'forest_env/confirm_delete.html',
                  {'object': obj, 'title': 'Delete Wildlife'})


# ── Weather Conditions ────────────────────────────────────────────
@login_required
def weather_list(request):
    items = WeatherCondition.objects.select_related('forest_area__forest').order_by('-recorded_at')[:100]
    return render(request, 'forest_env/weather_list.html',
                  {'items': items, 'title': 'Weather Conditions'})

@login_required
def weather_create(request):
    form = WeatherConditionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Weather record added.')
        return redirect('forest_env:weather_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Add Weather Condition', 'action': 'Create'})

@login_required
def weather_update(request, pk):
    obj = get_object_or_404(WeatherCondition, pk=pk)
    form = WeatherConditionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Weather record updated.')
        return redirect('forest_env:weather_list')
    return render(request, 'forest_env/forest_form.html',
                  {'form': form, 'title': 'Edit Weather', 'action': 'Update', 'object': obj})

@login_required
def weather_delete(request, pk):
    obj = get_object_or_404(WeatherCondition, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Weather record deleted.')
        return redirect('forest_env:weather_list')
    return render(request, 'forest_env/confirm_delete.html',
                  {'object': obj, 'title': 'Delete Weather Record'})
