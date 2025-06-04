
const API_BASE_URL = import.meta.env.VITE_API_URL;

export const userLogin = async (username,password) => {
    const url = `${API_BASE_URL}/login`;

    try {
        const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        });

        return response
    } catch (error) {
        console.error('Error failed to login:', error);
        throw error;
    }

}


export const userRegistration = async (username,email,password,userType) => {
    try{
        const body = { 
            username,
            email, 
            password, 
            userType,
        };
        const response = await fetch(`${API_BASE_URL}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        return response

    }catch (error) {
            console.error('Error failed to register:', error);
            throw error;
        }
}
