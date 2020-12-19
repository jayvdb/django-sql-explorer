# -*- coding: utf-8 -*-
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404
from django.views import View

from explorer.models import Query
from explorer.utils import url_get_query_id
from explorer.views.auth import PermissionRequiredMixin
from explorer.views.export import _export


class StreamQueryView(PermissionRequiredMixin, View):

    permission_required = 'view_permission'

    def get(self, request, query_id, *args, **kwargs):
        if not url_get_query_id(request, query_id):
            raise SuspiciousOperation
        query = get_object_or_404(Query, pk=query_id)
        return _export(request, query, download=False)
