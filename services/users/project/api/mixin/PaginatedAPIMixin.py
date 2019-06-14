# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/5/3 10:10 PM'

from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_paged_dict(query, page, per_page, include_fields=True, endpoint=None, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'list': [item.to_dict(include_fields) for item in resources.items],
            'pagination': {
                'current': page,
                'pageSize': per_page,
                'total_pages': resources.pages,
                'total': resources.total
            }
        }
        if endpoint:
            data['_links'] = {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        return data
