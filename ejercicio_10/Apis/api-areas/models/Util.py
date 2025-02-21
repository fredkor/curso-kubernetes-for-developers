from sqlalchemy import text

def get_sort_condition(cls, sort, order):
    if '.' not in sort:
        sort = '{}.{}'.format(cls.__tablename__, sort)
    else:
        arr = sort.split('.')
        sort = '{}.{}'.format(arr[len(arr) - 2], arr[len(arr) - 1])

    return text('{} {}'.format(sort, order))

def get_filter_from_request(request):
    filter_data = {
        key: value for (key, value) in request.args.items() if value and key not in ['q', 'page', 'per_page', 'sort', 'order', 'mode', 'strict']
    }

    for key, value in filter_data.items():
        if filter_data[key] == 'undefined':
            filter_data[key] = None

    return filter_data

def get_filter_table_map(filters):
    map_table = {}
    principal_filters = {}

    for filter, value in filters.items():
        filter_split = filter.split('.')
        if len(filter_split) != 1:
            if map_table.get(filter_split[0]) is not None:
                table_filter = map_table.get(filter_split[0])
            else:
                table_filter = {}

            table_filter[filter_split[1]] = value
            map_table[filter_split[0]] = table_filter
        else:
            principal_filters[filter] = value

    return principal_filters, map_table


def remove_special_filters(filters):
    special_filters = {}
    for filter, value in filters.items():
        if filters[filter] == 'is_not_null':
            special_filters[filter] = filters.get(filter)

    for filter, value in special_filters.items():
        filters.pop(filter)

    return filters, special_filters
