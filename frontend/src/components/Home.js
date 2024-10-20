import React,{ useState, useEffect } from "react";
import axios from 'axios';
import '../styles/home.css';


const Home = () => {
    const [levelPreviews, setLevelPreviews] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(()=>{
        const fetchLevelPreviews = async () => {
            setLoading(true);
            try {
                const levels = [1,2,3,4,5,6];
                const previews = {};

                for (const level of levels) {
                    const animeList = [];
                    //Fetch 3 anime for preview
                    for (let i = 0; i < 3; i++) {
                        const response = await axios.get(`/api/random-anime/${level}/`);
                        animeList.push(response.data);
                    }

                    previews[level] = animeList
                } 
                setLevelPreviews (previews);
         
            } catch (error) {
                console.error('Error fetching previews:', error);
                setError('Failed to load anime previews. Please try again later.');
            } finally {
                setLoading(false);
            }
        };
        
        fetchLevelPreviews();
    },[]);

    const getLevelName = (level) => {
        const names = {
            1: "Very Easy (Top 250)",
            2: "Easy (250-500)",
            3: "Medium (500-1000)",
            4: "Hard (1000-3000)",
            5: "Very Hard (3000-5000)",
            6: "God Mode (5000+)"
        };
        return names[level]
    }

    
    if (loading) {
        return (
            <div className="landing-container">
                <div className="sidebar">
                    <div className="glass-box">
                        <h1>AnimGuess</h1>
                        <p>Loading your anime adventure...</p>
                    </div>
                </div>
                <div className="main-content loading">
                    <div className="loading-spinner"></div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="landing-container">
                <div className="sidebar">
                    <div className="glass-box">
                        <h1>AnimGuess</h1>
                        <p>{error}</p>
                    </div>
                </div>
            </div>
        );
    }



    return (
        <div className="landing-container">
            <div className="sidebar">
                <div className="glass-box">
                    <h1>AnimGuess</h1>
                    <p>Just another anime guessing game? No. Well yea with a unique twist, we test how well do you know an anime's rating, yeah, you had that right, rating!</p>
                </div>
            </div>
            <div className="main-content">
                {Object.entries(levelPreviews).map(([level, animeList]) => (
                    <div key={level} className="level-section">
                        <h2 className="level-title">{getLevelName(parseInt(level))}</h2>
                        <div className="anime-cards">
                            {animeList.map((anime, index) => (
                                <div 
                                    key={anime.mal_id} 
                                    className={`anime-card ${index === 2 ? 'card-cutoff' : ''}`}
                                >
                                    <img 
                                        src={anime.images.image_url} 
                                        alt={anime.title} 
                                        className="anime-poster" 
                                    />
                                    <h3 className="anime-title">{anime.title}</h3>
                                    <div className="anime-meta">
                                        <span className="anime-year">{anime.year}</span>
                                        {index !== 2 && (
                                            <span className="anime-popularity">
                                                #{anime.popularity} in popularity
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};


export default Home;