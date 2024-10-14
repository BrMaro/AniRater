import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './GameSession.css';


const GameSession = () => {
    const [anime, setAnime] = useState(null);
    const [clueIndex, setClueIndex] = useState(0); // Track which clue to show

    useEffect(() => {
        const fetchAnime = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/random-anime/1/');
                setAnime(response.data);
            } catch (error) {
                console.error('Error fetching anime:', error);
            }
        }
        
        fetchAnime();
    }, [])

    const revealNextClue = () => {
        if (clueIndex < 9) { // There are 10 clues (0 to 9)
            setClueIndex(clueIndex + 1);
        }
    };

    // Ordering clues based on least telling to most telling
    const clues = anime ? [
        anime.images.image_url,      // 1. Poster (least telling)
        `${anime.title} (${anime.year})`, // 2. Title and Year
        anime.genres.join(', '),     // 3. Genres
        anime.synopsis,              // 4. Synopsis
        anime.youtube_url,           // 5. YouTube video (trailer)
        anime.popularity,            // 6. Popularity
        anime.favorites,             // 7. Favorites
        anime.members,               // 8. Members
        anime.rank,                  // 9. Rank
        anime.scored_by              // 10. Scored By (most telling)
    ] : [];

    return (
        <div className="game-container">
            {anime ? (
                <div className="anime-card">
                    <h2>Guess the Anime Rating!</h2>
                    
                    <div className="anime-image-wrapper">
                        {clueIndex >= 0 && <img className="anime-poster" src={anime.images.image_url} alt="Anime Poster" />}
                    </div>

                    <div className="anime-details">
                        {clueIndex >= 1 && <p><strong>Title & Year:</strong> {anime.title} ({anime.year})</p>}
                        {clueIndex >= 2 && <p><strong>Genres:</strong> {anime.genres.join(', ')}</p>}
                        {clueIndex >= 3 && <p><strong>Synopsis:</strong> {anime.synopsis}</p>}
                        {clueIndex >= 4 && (
                            <div className="youtube-trailer">
                                <iframe 
                                    src={`https://www.youtube.com/embed/${new URL(anime.youtube_url).searchParams.get('v')}`} 
                                    frameBorder="0" 
                                    allowFullScreen 
                                    title="Anime Trailer"
                                />
                            </div>
                        )}
                        {clueIndex >= 5 && <p><strong>Popularity:</strong> {clues[5]}</p>}
                        {clueIndex >= 6 && <p><strong>Favorites:</strong> {clues[6]}</p>}
                        {clueIndex >= 7 && <p><strong>Members:</strong> {clues[7]}</p>}
                        {clueIndex >= 8 && <p><strong>Rank:</strong> {clues[8]}</p>}
                        {clueIndex >= 9 && <p><strong>Scored By:</strong> {clues[9]}</p>}
                    </div>
                    <button onClick={revealNextClue} className="reveal-btn" disabled={clueIndex >= 9}>
                        {clueIndex >= 9 ? "No More Clues" : "Reveal Next Clue"}
                    </button>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default GameSession;
