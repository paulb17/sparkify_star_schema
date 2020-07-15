from db_manager.db_transactions import DatabaseTransactionManager
from db_manager.db_model.sparkify_schema import DimSongs, DimArtists
from db_manager.session_manager import session_scope


class SparkifyDBQueries(DatabaseTransactionManager):

    def __init__(
            self,
            db_name=None,
            db_host=None
    ):

        super().__init__(

            db_name=db_name,
            db_host=db_host
        )

    def song_fact_query(self, record):
        """
        Query the song and artist dimension table to identify foreign keys for the sparkify fact table
        """

        with session_scope(self.engine) as session:

            result = session.query(
                DimSongs.artist_id,
                DimSongs.song_id,
            ).join(
                DimArtists, DimArtists.artist_id == DimSongs.artist_id
            ).filter(
                DimSongs.duration == record['length'],
                DimSongs.title == record['song'],
                DimArtists.artist_name.ilike(f"%{record['artist']}%"),
            ).first()

        if not result:
            artist_id, song_id = None, None
        else:
            artist_id, song_id = result

        return artist_id, song_id
