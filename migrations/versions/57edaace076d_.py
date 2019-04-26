"""empty message

Revision ID: 57edaace076d
Revises: 
Create Date: 2019-04-19 08:25:43.692974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57edaace076d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('image_url', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_image_url'), 'categories', ['image_url'], unique=False)
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)
    op.create_index(op.f('ix_categories_status'), 'categories', ['status'], unique=False)
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('image_url', sa.String(length=64), nullable=True),
    sa.Column('overview', sa.String(length=10000), nullable=True),
    sa.Column('description', sa.String(length=10000), nullable=True),
    sa.Column('climate', sa.String(length=500), nullable=True),
    sa.Column('best_time_to_visit', sa.String(length=500), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_countries_climate'), 'countries', ['climate'], unique=False)
    op.create_index(op.f('ix_countries_image_url'), 'countries', ['image_url'], unique=False)
    op.create_index(op.f('ix_countries_name'), 'countries', ['name'], unique=False)
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avator', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_features_avator'), 'features', ['avator'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('index', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('nickname', sa.String(length=100), nullable=True),
    sa.Column('display_name', sa.String(length=100), nullable=True),
    sa.Column('photo', sa.String(length=100), nullable=True),
    sa.Column('social_id', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('dob', sa.DateTime(), nullable=True),
    sa.Column('phone_number_personal', sa.String(length=100), nullable=True),
    sa.Column('phone_number_company', sa.String(length=100), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('company_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.Column('last_booking_read_time', sa.DateTime(), nullable=True),
    sa.Column('last_offer_read_time', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_company_name'), 'users', ['company_name'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_token'), 'users', ['token'], unique=True)
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=120), nullable=True),
    sa.Column('overview', sa.String(length=2000), nullable=True),
    sa.Column('paypal', sa.String(length=120), nullable=True),
    sa.Column('logo', sa.String(length=120), nullable=True),
    sa.Column('banner', sa.String(length=120), nullable=True),
    sa.Column('facebook', sa.String(length=120), nullable=True),
    sa.Column('twitter', sa.String(length=120), nullable=True),
    sa.Column('instagram', sa.String(length=120), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_body'), 'messages', ['body'], unique=False)
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('payload_json', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_payload_json'), 'notifications', ['payload_json'], unique=False)
    op.create_table('prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('location', sa.String(length=120), nullable=True),
    sa.Column('total_price_adults', sa.Numeric(), nullable=True),
    sa.Column('total_price_children', sa.Numeric(), nullable=True),
    sa.Column('price_per_day_children', sa.Numeric(), nullable=True),
    sa.Column('price_per_day_adults', sa.Numeric(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publishers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=120), nullable=True),
    sa.Column('overview', sa.String(length=2000), nullable=True),
    sa.Column('paypal', sa.String(length=120), nullable=True),
    sa.Column('logo', sa.String(length=120), nullable=True),
    sa.Column('banner', sa.String(length=120), nullable=True),
    sa.Column('facebook', sa.String(length=120), nullable=True),
    sa.Column('twitter', sa.String(length=120), nullable=True),
    sa.Column('instagram', sa.String(length=120), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('overal_ratings', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Publocations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('country', sa.String(length=120), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('includes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('include', sa.String(length=120), nullable=True),
    sa.Column('price_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['price_id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('listings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('short_description', sa.String(length=320), nullable=True),
    sa.Column('long_description', sa.String(length=2000), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=80), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('package', sa.String(length=64), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('overal_ratings', sa.Integer(), nullable=True),
    sa.Column('connectivity', sa.String(length=120), nullable=True),
    sa.Column('physical_condition', sa.String(length=64), nullable=True),
    sa.Column('price_type_id', sa.Integer(), nullable=True),
    sa.Column('availability_from', sa.DateTime(), nullable=True),
    sa.Column('availability_to', sa.DateTime(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('add_ons', sa.String(length=2000), nullable=True),
    sa.Column('policy', sa.String(length=2000), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=True),
    sa.Column('space', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['features.id'], ),
    sa.ForeignKeyConstraint(['price_type_id'], ['prices.id'], ),
    sa.ForeignKeyConstraint(['publisher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_listings_availability_from'), 'listings', ['availability_from'], unique=False)
    op.create_index(op.f('ix_listings_availability_to'), 'listings', ['availability_to'], unique=False)
    op.create_index(op.f('ix_listings_location'), 'listings', ['location'], unique=False)
    op.create_index(op.f('ix_listings_package'), 'listings', ['package'], unique=False)
    op.create_index(op.f('ix_listings_published'), 'listings', ['published'], unique=False)
    op.create_index(op.f('ix_listings_status'), 'listings', ['status'], unique=False)
    op.create_table('parks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=10000), nullable=True),
    sa.Column('image_url', sa.String(length=64), nullable=True),
    sa.Column('climate', sa.String(length=500), nullable=True),
    sa.Column('best_time_to_visit', sa.String(length=500), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('price_type_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['price_type_id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parks_climate'), 'parks', ['climate'], unique=False)
    op.create_index(op.f('ix_parks_country_id'), 'parks', ['country_id'], unique=False)
    op.create_index(op.f('ix_parks_image_url'), 'parks', ['image_url'], unique=False)
    op.create_index(op.f('ix_parks_name'), 'parks', ['name'], unique=False)
    op.create_table('pubemails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pubphones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=120), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity', sa.String(length=120), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('birds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('image_url', sa.String(length=64), nullable=True),
    sa.Column('park_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['park_id'], ['parks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_birds_description'), 'birds', ['description'], unique=False)
    op.create_index(op.f('ix_birds_image_url'), 'birds', ['image_url'], unique=False)
    op.create_index(op.f('ix_birds_name'), 'birds', ['name'], unique=False)
    op.create_index(op.f('ix_birds_park_id'), 'birds', ['park_id'], unique=False)
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('reason', sa.String(length=300), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookings_status'), 'bookings', ['status'], unique=False)
    op.create_table('days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('day_by_day', sa.String(length=2000), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('image_url', sa.String(length=64), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_image_url'), 'images', ['image_url'], unique=False)
    op.create_index(op.f('ix_images_name'), 'images', ['name'], unique=False)
    op.create_table('listing_tags',
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], )
    )
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place', sa.String(length=120), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=64), nullable=True),
    sa.Column('listing_id', sa.Integer(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.ForeignKeyConstraint(['publisher_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reviews_comment'), 'reviews', ['comment'], unique=False)
    op.create_table('wildlife',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('image_url', sa.String(length=64), nullable=True),
    sa.Column('frequency', sa.String(length=80), nullable=True),
    sa.Column('park_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['park_id'], ['parks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wildlife_description'), 'wildlife', ['description'], unique=False)
    op.create_index(op.f('ix_wildlife_frequency'), 'wildlife', ['frequency'], unique=False)
    op.create_index(op.f('ix_wildlife_image_url'), 'wildlife', ['image_url'], unique=False)
    op.create_index(op.f('ix_wildlife_name'), 'wildlife', ['name'], unique=False)
    op.create_index(op.f('ix_wildlife_park_id'), 'wildlife', ['park_id'], unique=False)
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price_id', sa.Integer(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], ),
    sa.ForeignKeyConstraint(['price_id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_offers_description'), 'offers', ['description'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.Column('children', sa.Integer(), nullable=True),
    sa.Column('adults', sa.Integer(), nullable=True),
    sa.Column('grand_total', sa.Numeric(), nullable=True),
    sa.Column('departure_date', sa.DateTime(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_holder_name', sa.String(length=64), nullable=True),
    sa.Column('card_number', sa.String(length=64), nullable=True),
    sa.Column('select_card', sa.String(length=64), nullable=True),
    sa.Column('month', sa.String(length=64), nullable=True),
    sa.Column('years', sa.String(length=64), nullable=True),
    sa.Column('card_identification_number', sa.String(length=64), nullable=True),
    sa.Column('billing_zip_code', sa.String(length=64), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_billing_zip_code'), 'payments', ['billing_zip_code'], unique=False)
    op.create_index(op.f('ix_payments_card_holder_name'), 'payments', ['card_holder_name'], unique=False)
    op.create_index(op.f('ix_payments_card_identification_number'), 'payments', ['card_identification_number'], unique=False)
    op.create_index(op.f('ix_payments_card_number'), 'payments', ['card_number'], unique=False)
    op.create_index(op.f('ix_payments_month'), 'payments', ['month'], unique=False)
    op.create_index(op.f('ix_payments_select_card'), 'payments', ['select_card'], unique=False)
    op.create_index(op.f('ix_payments_status'), 'payments', ['status'], unique=False)
    op.create_index(op.f('ix_payments_years'), 'payments', ['years'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payments_years'), table_name='payments')
    op.drop_index(op.f('ix_payments_status'), table_name='payments')
    op.drop_index(op.f('ix_payments_select_card'), table_name='payments')
    op.drop_index(op.f('ix_payments_month'), table_name='payments')
    op.drop_index(op.f('ix_payments_card_number'), table_name='payments')
    op.drop_index(op.f('ix_payments_card_identification_number'), table_name='payments')
    op.drop_index(op.f('ix_payments_card_holder_name'), table_name='payments')
    op.drop_index(op.f('ix_payments_billing_zip_code'), table_name='payments')
    op.drop_table('payments')
    op.drop_table('orders')
    op.drop_index(op.f('ix_offers_description'), table_name='offers')
    op.drop_table('offers')
    op.drop_index(op.f('ix_wildlife_park_id'), table_name='wildlife')
    op.drop_index(op.f('ix_wildlife_name'), table_name='wildlife')
    op.drop_index(op.f('ix_wildlife_image_url'), table_name='wildlife')
    op.drop_index(op.f('ix_wildlife_frequency'), table_name='wildlife')
    op.drop_index(op.f('ix_wildlife_description'), table_name='wildlife')
    op.drop_table('wildlife')
    op.drop_index(op.f('ix_reviews_comment'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_table('places')
    op.drop_table('listing_tags')
    op.drop_index(op.f('ix_images_name'), table_name='images')
    op.drop_index(op.f('ix_images_image_url'), table_name='images')
    op.drop_table('images')
    op.drop_table('days')
    op.drop_index(op.f('ix_bookings_status'), table_name='bookings')
    op.drop_table('bookings')
    op.drop_index(op.f('ix_birds_park_id'), table_name='birds')
    op.drop_index(op.f('ix_birds_name'), table_name='birds')
    op.drop_index(op.f('ix_birds_image_url'), table_name='birds')
    op.drop_index(op.f('ix_birds_description'), table_name='birds')
    op.drop_table('birds')
    op.drop_table('activities')
    op.drop_table('pubphones')
    op.drop_table('pubemails')
    op.drop_index(op.f('ix_parks_name'), table_name='parks')
    op.drop_index(op.f('ix_parks_image_url'), table_name='parks')
    op.drop_index(op.f('ix_parks_country_id'), table_name='parks')
    op.drop_index(op.f('ix_parks_climate'), table_name='parks')
    op.drop_table('parks')
    op.drop_index(op.f('ix_listings_status'), table_name='listings')
    op.drop_index(op.f('ix_listings_published'), table_name='listings')
    op.drop_index(op.f('ix_listings_package'), table_name='listings')
    op.drop_index(op.f('ix_listings_location'), table_name='listings')
    op.drop_index(op.f('ix_listings_availability_to'), table_name='listings')
    op.drop_index(op.f('ix_listings_availability_from'), table_name='listings')
    op.drop_table('listings')
    op.drop_table('includes')
    op.drop_table('Publocations')
    op.drop_table('publishers')
    op.drop_table('prices')
    op.drop_index(op.f('ix_notifications_payload_json'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_messages_body'), table_name='messages')
    op.drop_table('messages')
    op.drop_table('customers')
    op.drop_index(op.f('ix_users_token'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_company_name'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_features_avator'), table_name='features')
    op.drop_table('features')
    op.drop_index(op.f('ix_countries_name'), table_name='countries')
    op.drop_index(op.f('ix_countries_image_url'), table_name='countries')
    op.drop_index(op.f('ix_countries_climate'), table_name='countries')
    op.drop_table('countries')
    op.drop_index(op.f('ix_categories_status'), table_name='categories')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_index(op.f('ix_categories_image_url'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
