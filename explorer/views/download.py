# -*- coding: utf-8 -*-
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from explorer.models import Query
from explorer.utils import url_get_query_id
from explorer.views.auth import PermissionRequiredMixin
from explorer.views.export import _export


class DownloadQueryView(PermissionRequiredMixin, View):

    permission_required = 'view_permission'

    def get(self, request, query_id, *args, **kwargs):
        if not url_get_query_id(request, query_id):
            raise SuspiciousOperation
        query = get_object_or_404(Query, pk=query_id)
        return _export(request, query)


class DownloadFromSqlView(PermissionRequiredMixin, View):

    permission_required = 'view_permission'

    def post(self, request, *args, **kwargs):
        sql = request.POST.get('sql', '')
        connection = request.POST.get('connection', '')
        query = Query(sql=sql, connection=connection, title='')
        if not sql:
            raise SuspiciousOperation
        ql = query.log(request.user)
        query.title = f'Playground-{ql.id}'
        return _export(request, query)
