import sqlalchemy as sa
from sqlalchemy.orm import relationship
from .base import Base


class DimUsers(Base):

    # primary key
    user_id = sa.Column(sa.Integer, primary_key=True)

    # other columns
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    gender = sa.Column(sa.String)
    level = sa.Column(sa.String)


class DimArtists(Base):

    # primary key
    artist_id = sa.Column(sa.String, primary_key=True)

    # other columns
    artist_name = sa.Column(sa.String)
    artist_location = sa.Column(sa.String)
    artist_latitude = sa.Column(sa.String)
    artist_longitude = sa.Column(sa.String)


class DimTime(Base):

    # primary key
    start_time = sa.Column(sa.DateTime, primary_key=True)

    # other columns
    hour = sa.Column(sa.Integer)
    day = sa.Column(sa.Integer)
    week = sa.Column(sa.Integer)
    month = sa.Column(sa.Integer)
    year = sa.Column(sa.Integer)
    weekday = sa.Column(sa.Integer)


class DimSongs(Base):

    # primary key
    song_id = sa.Column(sa.String, primary_key=True)

    # foreign key and relationship
    artist_id = sa.Column(sa.String, sa.ForeignKey('dim_artists.artist_id'))
    dim_artist = relationship("DimArtists", backref='dim_songs')

    # other columns
    title = sa.Column(sa.String)
    year = sa.Column(sa.Integer)
    duration = sa.Column(sa.Float)


class FactSongPlays(Base):

    # primary key
    songplay_id = sa.Column(sa.Integer, primary_key=True)

    # foreign keys
    user_id = sa.Column(sa.Integer, sa.ForeignKey('dim_users.user_id'))
    song_id = sa.Column(sa.String, sa.ForeignKey('dim_songs.song_id'))
    artist_id = sa.Column(sa.String, sa.ForeignKey('dim_artists.artist_id'))
    start_time = sa.Column(sa.DateTime, sa.ForeignKey('dim_time.start_time'))

    # relationships
    dim_users = relationship("DimUsers", backref='fact_song_plays')
    dim_songs = relationship("DimSongs", backref='fact_song_plays')
    dim_artist = relationship("DimArtists", backref='fact_song_plays')
    dim_time = relationship("DimTime", backref='fact_song_plays')

    # other columns
    session_id = sa.Column(sa.Integer)
    level = sa.Column(sa.String)
    location = sa.Column(sa.String)
    user_agent = sa.Column(sa.String)


song_data_dimensions = [DimArtists, DimSongs]
log_data_dimensions = [DimUsers,  DimTime]
sparkify_facts = [FactSongPlays]
