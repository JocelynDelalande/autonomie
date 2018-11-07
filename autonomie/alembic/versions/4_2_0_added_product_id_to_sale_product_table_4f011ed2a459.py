"""4.2.0 Added product_id to sale_product table

Revision ID: 4f011ed2a459
Revises: 18b6a30326e2
Create Date: 2018-10-11 14:50:10.510325

"""

# revision identifiers, used by Alembic.
revision = '4f011ed2a459'
down_revision = '18b6a30326e2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def update_database_structure():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sale_product', sa.Column('product_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def get_tva(tva_value=2000):
    """ Return TVA objet by value"""
    cnx = op.get_bind()
    tva = cnx.execute("SELECT id FROM tva WHERE value=%s" % tva_value)
    tva_id = None
    if tva is not None:
        for tva_item in tva:
            tva_id = tva_item.id
    return tva_id


def get_product_id(tva_id):
    """ Return product object depending on TVA id"""
    cnx = op.get_bind()
    products = cnx.execute("SELECT id from product WHERE tva_id=%s" % tva_id)
    product_id = None
    if products is not None and products.rowcount < 2:
        for product in products:
            product_id = product.id
    return product_id


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    cnx = op.get_bind()
    sale_product = cnx.execute("SELECT id, tva FROM sale_product")
    for item in sale_product:
        tva = get_tva(item.tva)
        if tva is not None:
            product = get_product_id(tva)
            if product is not None:
                cnx.execute("UPDATE sale_product SET product_id=%s WHERE id=%s" % (product, item.id))
        else:
            tva = get_tva()
            if tva is not None:
                product = get_product_id(tva)
                if product is not None:
                    cnx.execute("UPDATE sale_product SET product_id=%s WHERE id=%s" % (product, item.id))

    from zope.sqlalchemy import mark_changed
    mark_changed(session)


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sale_product', 'product_id')
    ### end Alembic commands ###