# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
)
from autonomie_base.models.types import (
    PersistentACLMixin,
)
from autonomie_base.models.base import (
    default_table_args,
)
from autonomie.models.node import Node


class Business(Node):
    """
    Permet de :

        * Collecter les fichiers

        * Regrouper devis/factures/avoirs

        * Calculer le CA d'une affaire

        * Générer les factures

        * Récupérer le HT à dépenser

        * Des choses plus complexes en fonction du type de business

    Business.estimations
    Business.invoices
    Business.invoices[0].cancelinvoices
    """
    __tablename__ = "business"
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': "business"}

    id = Column(
        Integer,
        ForeignKey('node.id'),
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )

    closed = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Cette affaire est-elle terminée ?"
            }
        },
    )

    business_type_id = Column(
        ForeignKey('business_type.id'),
        info={'colanderalchemy': {'title': u"Type d'affaires"}}
    )
    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    # Relations
    business_type = relationship(
        "BusinessType",
        info={'colanderalchemy': {'exclude': True}},
    )
    project = relationship(
        "Project",
        primaryjoin="Project.id == Business.project_id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )
    estimations = relationship(
        "Estimation",
        back_populates="businesses",
        secondary="estimation_business",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )
    invoices = relationship(
        "Invoice",
        back_populates="business",
        primaryjoin="Invoice.business_id==Business.id",
    )
    cancelinvoices = relationship(
        "CancelInvoice",
        back_populates="business",
        primaryjoin="CancelInvoice.business_id==Business.id",
    )
