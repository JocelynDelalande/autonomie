"""Added product_id to sale_product table

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

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    cnx = op.get_bind()
    sale_product = cnx.execute("SELECT id, tva FROM sale_product")
    for item in sale_product:
        tvaId = cnx.execute("SELECT id FROM tva  WHERE value=%s" % item.tva)
        if tvaId is not None:
            for id in tvaId:
                products = cnx.execute("SELECT id, tva_id from product WHERE tva_id=%s" % id.id)
                if products is not None and products.rowcount < 2:
                    for product in products:
                        cnx.execute("UPDATE sale_product SET product_id=%s WHERE id=%s" % (product.id, item.id))
    from zope.sqlalchemy import mark_changed
    mark_changed(session)

def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sale_product', 'product_id')
    ### end Alembic commands ###
