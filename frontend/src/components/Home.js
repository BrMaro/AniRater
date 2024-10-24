import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import { motion, AnimatePresence } from "framer-motion";
import '../styles/home.css';

const Home = () => {
    const navigate = useNavigate();
    const [levelPreviews, setLevelPreviews] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [visiblePair, setVisiblePair] = useState(0);
    const [isTyping, setIsTyping] = useState(true);
    
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

    useEffect(() => {
        if (!loading) {
            const changeLevel = async () => {
                setIsTyping(false);
                await delay(1000);
                setVisiblePair((prev) => (prev + 1) % 3);
                setIsTyping(true);
            };

            const interval = setInterval(changeLevel, 10000);

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
                    <div className="title-box">
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
                    <div className="title-box">
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
                <div className="title-box">
                    <h1>AnimGuess</h1>
                    <p>Just another anime guessing game? No. Well yea with a unique twist, we test how well do you know an anime's rating!</p>
                    <motion.button
                        className="portal-button"
                        onClick={() => navigate('/game-session')}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                    >
                        Enter the Challenge
                    </motion.button>
                </div>
            </div>
            <div className="main-content">
                <AnimatePresence mode="wait">
                    {visibleLevels.map((level, levelIndex) => (
                        <motion.div
                            key={level}
                            className="level-section"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.5 }}
                        >
                            <motion.h2 
                                className="level-title"
                                animate={{
                                    width: isTyping ? "100%" : "0%",
                                }}
                                transition={{ 
                                    duration: isTyping ? 1 : 0.5,
                                    delay: levelIndex * 0.5,
                                    ease: "easeInOut"
                                }}
                            >
                                {getLevelName(level)}
                            </motion.h2>
                            <div className="anime-cards">
                                {levelPreviews[level]?.map((anime, index) => (
                                    <motion.div 
                                        key={anime.mal_id}
                                        className="anime-card"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ 
                                            duration: 0.5,
                                            delay: levelIndex * 0.5 + index * 0.2 + 1
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