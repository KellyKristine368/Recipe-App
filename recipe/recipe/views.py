from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Category
from .forms import RecipeForm, CategoryForm

# Create your views here.
def home(request):
    featured_recipe = Recipe.objects.order_by('-created_at').first()

    # GET FULL LIST FIRST (no slicing yet!)
    latest_recipes = Recipe.objects.all().order_by('-created_at')
    popular_recipes = Recipe.objects.all().order_by('-recipe_view_count')
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        latest_recipes = latest_recipes.filter(category_id=category_id)
        popular_recipes = popular_recipes.filter(category_id=category_id)

    search_query = request.GET.get('search')
    if search_query:
        latest_recipes = latest_recipes.filter(recipe_name__icontains=search_query)
        popular_recipes = popular_recipes.filter(recipe_name__icontains=search_query)

    # NOW SLICE AFTER FILTERING
    latest_recipes = latest_recipes[:6]
    popular_recipes = popular_recipes[:6]

    context = {
        'featured_recipe': featured_recipe,
        'latest_recipes': latest_recipes,
        'popular_recipes': popular_recipes,
        'categories': categories,
        'search_query': search_query or '',
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'home.html', context)


def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('recipe_list') 
    else:
        form = RecipeForm()

    context = {
        'form': form
    }
    return render(request, 'recipe/create_recipe.html', context)



def recipe_list(request):
    # Get all recipes, newest first
    recipes = Recipe.objects.all().order_by('-id')

    # Group recipes by category (None for Uncategorized)
    categorized_recipes = {}
    for recipe in recipes:
        category = recipe.category  # can be None
        if category not in categorized_recipes:
            categorized_recipes[category] = []
        categorized_recipes[category].append(recipe)

    context = {
        'categorized_recipes': categorized_recipes
    }
    return render(request, 'recipe/recipe_list.html', context)

def recipes(request): 
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RecipeForm()
        
        queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context = {
        'recipes': queryset,
        'form': form,
    }
    return render(request, 'recipe/recipes.html', context)

def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return redirect('/')

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.recipe_view_count += 1
    recipe.save()
    related_recipes = Recipe.objects.filter(category=recipe.category).exclude(id=recipe.id)[:6]

    context = {
        'recipe': recipe,
        'recipes': related_recipes  
    }
    return render(request, 'recipe/recipe_detail.html', context)


def update_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'recipe': recipe,
        'form': form,
    }
    return render(request, 'recipe/update_recipe.html', context)
    
    
def category_list(request):
    categories = Category.objects.all().order_by('name')
    recipes = None

    # When a category is clicked — filter recipes by that category
    category_id = request.GET.get('category')
    if category_id:
        recipes = Recipe.objects.filter(category_id=category_id)

    context = {
        'categories': categories,
        'recipes': recipes,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'recipe/category.html', context)

   # make sure you created this form

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')

    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'recipe/add_category.html', context)

def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.method == "POST":
        recipe.delete()
        return redirect('recipe-list')

    return render(request, 'recipe/recipe_confirm_delete.html', {"recipe": recipe})

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'category': category}
    return render(request, 'recipe/edit_category.html', context)

def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    
    context = {'category': category}
    return render(request, 'recipe/delete_category.html', context)

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    recipes = Recipe.objects.filter(category=category)

    context = {
        'category': category,
        'recipes': recipes,
    }
    return render(request, 'recipe/category_detail.html', context)