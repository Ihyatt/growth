
const API_BASE_URL = import.meta.env.VITE_API_URL;

export const userLogin = async (username, password) => {
    const url = `${API_BASE_URL}/login`;
    console.log(username, password)
    try {
        const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        });
        if (!response.ok) {
        throw new Error(data?.message || 'Login failed.');
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error('Error failed to login:', error);
        throw error;
    }

}