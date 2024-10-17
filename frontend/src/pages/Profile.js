import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
    const [profileData, setProfileData] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/profile/');
                setProfileData(response.data);
            } catch (error) {
                console.error('Error fetching profile data:', error);
            }
        };
        fetchProfile();
    }, []);
    
    return (
        <div>
            {profileData ? (
                <div>
                    <h2>Profile</h2>
                    <p>Username: {profileData.username}</p>
                    <p>Email: {profileData.email}</p>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Profile;