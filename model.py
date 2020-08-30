from config import Config
import sqlalchemy as sa

connection = 'postgres://{0}:{1}@{2}/{3}'.format(Config.DATABASE_USER,
                                                 Config.DATABASE_PASSWORD,
                                                 Config.DATABASE_HOST,
                                                 Config.DATBASE_NAME)

milk_produce = sa.Table('tb_raw_milk', sa.MetaData(),
               sa.Column('raw_milk_id', sa.String, primary_key=True),
               sa.Column('raw_milk_farm_id', sa.String, nullable=False),
               sa.Column('raw_milk_product_id', sa.String, nullable=False),
               sa.Column('raw_milk_product_quantity', sa.Integer, nullable=False),
               sa.Column('raw_milk_product_price', sa.Float, nullable=False),
               sa.Column('raw_milk_product_units', sa.VARCHAR(10), nullable=False),
               sa.Column('raw_milk_timestamp', sa.TIMESTAMP, nullable=False))

milk_price = sa.Table('tb_raw_milk_price', sa.MetaData(),
                     sa.Column('rmp_id', sa.String, primary_key=True),
                     sa.Column('rmp_farm_id', sa.String, nullable=False),
                     sa.Column('rmp_product_id', sa.String, nullable=False),
                     sa.Column('rmp_total_product_quantity', sa.Integer, nullable=False),
                     sa.Column('rmp_avg_price', sa.Float, nullable=False),
                     sa.Column('rmp_units', sa.VARCHAR(10), nullable=False),
                     sa.Column('rmp_date', sa.Date, nullable=False),
                     sa.Column('rmp_current_price', sa.Float, nullable=False),
                     sa.Column('rmp_current_quantity', sa.Integer, nullable=False))

p_goods = sa.Table('tb_processed_goods', sa.MetaData(),
               sa.Column('pg_id', sa.String, primary_key=True),
               sa.Column('pg_timestamp', sa.TIMESTAMP, nullable=False),
               sa.Column('pg_product_id', sa.String, nullable=False),
               sa.Column('pg_quantity_produced', sa.Integer, nullable=False),
               sa.Column('pg_quantity_used', sa.Integer, nullable=False),
               sa.Column('pg_farm_id', sa.String, nullable=False),
               sa.Column('pg_units', sa.VARCHAR(10), nullable=False),
               sa.Column('pg_milk_id', sa.String, nullable=False),
               sa.Column('pg_price', sa.Float, nullable=False))

p_goods_price = sa.Table('tb_processed_goods_price', sa.MetaData(),
                        sa.Column('pgp_id', sa.String, primary_key=True),
                        sa.Column('pgp_farm_id', sa.String, nullable=False),
                        sa.Column('pgp_product_id', sa.String, nullable=False),
                        sa.Column('pgp_total_quantity', sa.Integer, nullable=False),
                        sa.Column('pgp_avg_price', sa.Float, nullable=False),
                        sa.Column('pgp_units', sa.VARCHAR(10), nullable=False),
                        sa.Column('pgp_date', sa.Date, nullable=False),
                        sa.Column('pgp_current_quantity', sa.Integer, nullable=False),
                        sa.Column('pgp_current_price', sa.Float, nullable=False),
                        sa.Column('pgp_quantity_used', sa.Integer, nullable=False),
                        sa.Column('pgp_milk_id', sa.String, nullable=False))

net_stock = sa.Table('tb_net_stock', sa.MetaData(),
                    sa.Column('net_stock_id', sa.String, primary_key=True),
                    sa.Column('net_stock_product_id', sa.String, nullable=False),
                    sa.Column('net_stock_product_quantity', sa.Integer, nullable=False),
                    sa.Column('net_stock_product_units', sa.VARCHAR(50), nullable=False),
                    sa.Column('net_stock_last_updated', sa.TIMESTAMP, nullable=False),
                    sa.Column('net_stock_vendor_id', sa.String, nullable=False),
                    sa.Column('net_stock_avg_price', sa.Float, nullable=False))