from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination(request, queryset, results=6):
    page = request.GET.get('page')
    paginator = Paginator(queryset, results)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    left_index = int(page) - 2
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 3
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return objects, custom_range, paginator
