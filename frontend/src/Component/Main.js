import React, { useState } from 'react';
import { Typography, Container, TextField, IconButton, Button, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import MenuIcon from '@mui/icons-material/Menu';
import "./Main.css";

function Main() {
  const [songList, setSongList] = useState([]);
  const [newSong, setNewSong] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const addSong = () => {
    if (newSong.trim() !== '') {
      setSongList([...songList, newSong]);
      setNewSong('');
    }
  };

  const filteredSongs = songList.filter(song => song.includes(searchTerm));

  return (
    <div className='main'>
      <Container maxWidth="sm" className='container'>
        <div className='Music_Search'>
          <TextField 
            fullWidth
            variant="outlined"
            placeholder="曲を検索..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <SearchIcon sx={{ mr: 1 }} />
              ),
            }}
          />
        </div>

        <div className='input-SongList'>
          <div className='input-Box'>
            {filteredSongs.map((song, index) => (
              <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <TextField
                  fullWidth
                  variant="outlined"
                  value={song}
                  style={{backgroundColor: '#444'}}
                  InputProps={{
                    readOnly: true,
                  }}
                />
              </Box>
            ))}
          </div>
        </div>

        <div>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="新しい曲を追加..."
            value={newSong}
            onChange={(e) => setNewSong(e.target.value)}
          />
          <Button onClick={addSong} variant="contained" style={{backgroundColor: 'green'}} startIcon={<AddIcon />} sx = {{mb:2}}>
            曲を追加
          </Button>
        </div>
      </Container>
    </div>
  );
}

export default Main;
