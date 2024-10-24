import React, { useState, useEffect } from "react";
import axios from 'axios';
import { motion, AnimatePresence } from "framer-motion";
import '../styles/home.css';

const Home = () => {
    const [levelPreviews, setLevelPreviews] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [visiblePair, setVisiblePair] = useState(0);
    
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    useEffect(() => {
        const fetchLevelPreviews = async () => {
            setLoading(true);
            try {
                const levels = [1, 2, 3, 4, 5, 6];
                const previews = {};
    
                for (let i = 0; i < levels.length; i += 3) {
                    const batch = levels.slice(i, i + 3);
                    const responses = await Promise.all(
                        batch.map(level => 
                            axios.get(`/api/level-previews/${level}/`)
                        )
                    );
                    
                    responses.forEach((response, index) => {
                        const level = batch[index];
                        previews[level] = response.data;
                    });
    
                    if (i + 3 < levels.length) {
                        await delay(1000);
                    }
                }
    
                setLevelPreviews(previews);
            } catch (error) {
                console.error('Error fetching previews:', error);
                setError(error.response?.data?.error || 'Failed to load anime previews.');
            } finally {
                setLoading(false);
            }
        };
    
        fetchLevelPreviews();
    }, []);

    // Rotate through level pairs every 5 seconds
    useEffect(() => {
        if (!loading) {
            const interval = setInterval(() => {
                setVisiblePair((prev) => (prev + 1) % 3); // 3 pairs of levels (1-2, 3-4, 5-6)
            }, 5000);

            return () => clearInterval(interval);
        }
    }, [loading]);

    const getLevelName = (level) => {
        const names = {
            1: "Very Easy ",//(Top 250)",
            2: "Easy ",//(250-500)",
            3: "Medium ",//(500-1000)",
            4: "Hard ",//(1000-3000)",
            5: "Very Hard ",//(3000-5000)",
            6: "God Mode "//(5000+)"
        };
        return names[level];
    };

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

    const visibleLevels = [1 + visiblePair * 2, 2 + visiblePair * 2];

    return (
        <div className="landing-container">
            <div className="sidebar">
                <div className="glass-box">
                    <h1>AnimGuess</h1>
                    <p>Just another anime guessing game? No. Well yea with a unique twist, we test how well do you know an anime's rating!</p>
                </div>
            </div>
            <div className="main-content">
                <AnimatePresence mode="wait">
                    {visibleLevels.map((level, levelIndex) => (
                        <motion.div
                            key={level}
                            className="level-section"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.5 }}
                        >
                            <motion.h2 
                                className="level-title"
                                initial={{ width: 0 }}
                                animate={{ width: "100%" }}
                                transition={{ 
                                    duration: 1, 
                                    delay: levelIndex * 0.5,
                                    ease: "easeOut"
                                }}
                            >
                                {getLevelName(level)}
                            </motion.h2>
                            <div className="anime-cards">
                                {levelPreviews[level]?.map((anime, index) => (
                                    <motion.div 
                                        key={anime.mal_id}
                                        className="anime-card"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ 
                                            duration: 0.5,
                                            delay: levelIndex * 0.5 + index * 0.2 + 1
                                        }}
                                        whileHover={{
                                            scale: 1.02,
                                            rotateY: 5,
                                            rotateX: -5,
                                            transition: { duration: 0.2 }
                                        }}
                                    >
                                        <div className="anime-image">
                                            <img 
                                                src={anime.images.image_url} 
                                                alt={anime.title}
                                            />
                                        </div>
                                        <div className="anime-details">
                                            <h3>{anime.title}</h3>
                                            <p className="anime-genres">
                                                {anime.genres?.map(g => g.name).join(', ')}
                                            </p>
                                            <div className="anime-stats">
                                                <span>Year: {anime.year}</span>
                                                <span>Score: {anime.score}</span>
                                                <span>Rank: #{anime.rank}</span>
                                                <span>Popularity: #{anime.popularity}</span>
                                                <span>Members: {anime.members?.toLocaleString()}</span>
                                                <span>Favorites: {anime.favorites?.toLocaleString()}</span>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </div>
    );
};

export default Home;