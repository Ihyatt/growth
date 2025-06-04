const API_BASE_URL = import.meta.env.VITE_API_URL;

const getAuthToken = () => {
    return localStorage.getItem('jwtToken');
};

export const fetchUsers = async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const url = `${API_BASE_URL}/admin/users?${queryString}`;


    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json(); // Assuming backend sends JSON errors
            throw new Error(errorData.message || 'Failed to fetch users.');
        }

        const data = await response.json();
        return data; // Assuming your backend returns { data: [...], pagination: {...} }
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error; // Re-throw to be caught by the component
    }
};

// --- API Call for Approving a User ---
export const approveUser = async (userId) => {
    const url = `${API_BASE_URL}/admin/users/${userId}/approve`; // Example endpoint

    try {
        const response = await fetch(url, {
            method: 'POST', // Method for actions/updates
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            },
            // You might send a body if needed, e.g., { approvedBy: 'adminId' }
            // body: JSON.stringify({})
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


export const rejectUser = async (userId, reason = '') => {
    const url = `${API_BASE_URL}/admin/users/${userId}/reject`; 

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            },
            body: JSON.stringify({ reason }) 
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

