# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Project model
"""
import datetime
import colander
import deform

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Boolean,
    Date,
)
from sqlalchemy.orm import (
    deferred,
    relationship,
    backref,
)

from autonomie import forms
from autonomie_base.models.types import (
    PersistentACLMixin,
)
from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
)
from autonomie.models.node import Node
from autonomie.models.services.project import ProjectService


ProjectCustomer = Table(
    'project_customer',
    DBBASE.metadata,
    Column("project_id", Integer, ForeignKey('project.id')),
    Column("customer_id", Integer, ForeignKey('customer.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine']
)


def check_begin_end_date(form, value):
    """
    Check the project beginning date preceeds the end date
    """
    ending = value.get('ending_date')
    starting = value.get('starting_date')

    if ending is not None and starting is not None:
        if not ending >= starting:
            exc = colander.Invalid(
                form,
                u"La date de début doit précéder la date de fin du projet"
            )
            exc['starting_date'] = u"Doit précéder la date de fin"
            raise exc


def get_projects_from_request(request):
    """
    Return the projects of the current company (we fetch the company from the
    request context)
    """
    if request.context.__name__ == 'project':
        # Edition (we don't want the current project)
        projects = [project for project in request.context.company.projects
                    if project.id != request.context.id]
    elif request.context.__name__ == 'company':
        projects = request.context.projects
    else:
        raise Exception("We can't retrieve the projects from something that's \
not a a project itself or a company")

    return projects


class Project(Node):
    """
        The project model
    """
    __tablename__ = 'project'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'project'}

    __colanderalchemy_config__ = {'validator': check_begin_end_date}

    id = Column(
        ForeignKey('node.id'),
        primary_key=True,
        info={'colanderalchemy': forms.EXCLUDED}
    )

    code = Column(
        String(4),
        info={'colanderalchemy': {'title': u"Code"}},
    )

    type = deferred(
        Column(
            String(150),
            info={'colanderalchemy': {'title': u"Type de projet"}},
        ),
        group='edit'
    )

    company_id = Column(
        Integer,
        ForeignKey('company.id'),
        info={
            'options': {'csv_exclude': True},
            'colanderalchemy': forms.EXCLUDED,
        }
    )

    starting_date = deferred(
        Column(
            Date(),
            info={
                "colanderalchemy": {
                    "title": u"Date de début",
                }
            },
            default=datetime.date.today,
        ),
        group='edit',
    )

    ending_date = deferred(
        Column(
            Date(),
            info={
                "colanderalchemy": {
                    "title": u"Date de fin",
                }
            },
            default=datetime.date.today,
        ),
        group='edit',
    )

    definition = deferred(
        Column(
            Text,
            info={
                'label': u"Définition",
                'colanderalchemy': {
                    'title': u"Définition",
                    'widget': deform.widget.TextAreaWidget(
                        css_class="col-md-10"
                    ),
                }
            },

        ),
        group='edit',
    )

    archived = Column(
        Boolean(),
        default=False,
        info={'colanderalchemy': forms.EXCLUDED},
    )

    customers = relationship(
        "Customer",
        secondary=ProjectCustomer,
        backref=backref(
            'projects',
            info={'colanderalchemy': forms.EXCLUDED},
        ),
        info={
            'colanderalchemy': {
                "title": u"Client",
                "exclude": True,
            },
            'export': {'exclude': True},
        }
    )

    tasks = relationship(
        "Task",
        primaryjoin="Task.project_id==Project.id",
        back_populates="project",
        order_by='Task.date',
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        }
    )
    estimations = relationship(
        "Estimation",
        primaryjoin="Estimation.project_id==Project.id",
        order_by='Estimation.date',
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        }
    )
    invoices = relationship(
        "Invoice",
        primaryjoin="Invoice.project_id==Project.id",
        order_by='Invoice.date',
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        }
    )
    cancelinvoices = relationship(
        "CancelInvoice",
        primaryjoin="CancelInvoice.project_id==Project.id",
        order_by='Invoice.date',
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        }
    )

    _autonomie_service = ProjectService

    def has_tasks(self):
        return self._autonomie_service.count_tasks(self) > 0

    def is_deletable(self):
        """
            Return True if this project could be deleted
        """
        return self.archived and not self.has_tasks()

    def get_company_id(self):
        return self.company.id

    def get_next_estimation_index(self):
        return self._autonomie_service.get_next_estimation_index(self)

    def get_next_invoice_index(self):
        return self._autonomie_service.get_next_invoice_index(self)

    def get_next_cancelinvoice_index(self):
        return self._autonomie_service.get_next_cancelinvoice_index(self)

    def todict(self):
        """
            Return a dict view of this object
        """
        phases = [phase.todict() for phase in self.phases]
        return dict(
            id=self.id,
            name=self.name,
            code=self.code,
            definition=self.definition,
            type=self.type,
            archived=self.archived,
            phases=phases,
        )

    def __json__(self, request):
        return self.todict()

    @classmethod
    def check_phase_id(cls, project_id, phase_id):
        return cls._autonomie_service.check_phase_id(project_id, phase_id)

    @classmethod
    def label_query(cls):
        return cls._autonomie_service.label_query(cls)