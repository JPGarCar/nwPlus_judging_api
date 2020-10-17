"""empty message

Revision ID: 3b3d7315647c
Revises: 21f4e65ee8b9
Create Date: 2020-10-17 12:36:25.749676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b3d7315647c'
down_revision = '21f4e65ee8b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hackers', sa.Column('grading_complete', sa.Boolean(), nullable=True))
    op.drop_column('hackers', 'judgingComplete')
    op.add_column('submissions', sa.Column('devpost_link', sa.String(), nullable=True))
    op.add_column('submissions', sa.Column('youtube_link', sa.String(), nullable=True))
    op.drop_column('submissions', 'youtubeLink')
    op.drop_column('submissions', 'devpostLink')
    op.add_column('teams', sa.Column('team_name', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'teams', ['team_name'])
    op.drop_column('teams', 'teamName')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('teamName', sa.VARCHAR(), nullable=True))
    op.drop_constraint(None, 'teams', type_='unique')
    op.drop_column('teams', 'team_name')
    op.add_column('submissions', sa.Column('devpostLink', sa.VARCHAR(), nullable=True))
    op.add_column('submissions', sa.Column('youtubeLink', sa.VARCHAR(), nullable=True))
    op.drop_column('submissions', 'youtube_link')
    op.drop_column('submissions', 'devpost_link')
    op.add_column('hackers', sa.Column('judgingComplete', sa.BOOLEAN(), nullable=True))
    op.drop_column('hackers', 'grading_complete')
    # ### end Alembic commands ###