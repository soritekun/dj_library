import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function SongResults({ songs }) {
  return (
    <div>
      {songs.map((song, index) => (
        <Card key={index} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h5" component="div">
              {song.name}
            </Typography>
            <Typography variant="body2">
              {(song.artistsn || []).map(artist => artist.name).join(', ')}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default SongResults;