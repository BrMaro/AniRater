import React from "react";
import './GameSession.css';


const CardComponent = ({ anime }) => {
    return (
        <div className="card-container">
            <div className="card">
                <img className="card-image" src={anime.image_url} alt={anime.title} />
                <div className="card-content">
                    <h3>{anime.title}</h3>
                    <p>{anime.synopsis}</p>
                </div>
            </div>
        </div>    )
}

export default CardComponent;
