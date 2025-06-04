import React from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL;


export const fetchUsers = async (params = {}, token) => {


    const queryString = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/admin/users?${queryString}`;
    console.log(token)
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
                
            }
        });

        if (!response.ok) {
            const errorData = await response.json(); // Assuming backend sends JSON errors
            throw new Error(errorData.message || 'Failed to fetch users.');
        }

        return response
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error; // Re-throw to be caught by the component
    }
};

export const approveUser = async (userId, token) => {
    console.log(token)
    const url = `${API_BASE_URL}/admin/approve`;
    console.log(token)
    try {

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
                
            },
            body: JSON.stringify({ userId }),
            });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Failed to approve user ${userId}.`);
        }

  
        const data = await response.json(); 
        return data;
    } catch (error) {
        console.error(`Error approving user ${userId}:`, error);
        throw error;
    }
};


export const rejectUser = async (userId, token) => {
    const url = `${API_BASE_URL}/admin/reject`; 
    try {
        console.log('iam here')
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
                
            },
            body: JSON.stringify({ userId }),
            });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Failed to reject user ${userId}.`);
        }

  
        const data = await response.json(); 
        return data;
    } catch (error) {
        console.error(`Error rejecting user ${userId}:`, error);
        throw error;
    }
};

