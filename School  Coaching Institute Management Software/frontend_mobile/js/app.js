const API_BASE_URL = 'http://192.168.0.176:5000/api'; // Assuming testing on local network, use PC IP or localhost for emulator

async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

const AppAuth = {
    async login(username, password) {
        const data = await fetchAPI('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        if (data.status === 'success' && data.user.role === 'student') {
            localStorage.setItem('studentUser', JSON.stringify(data.user));
            return data.user;
        } else {
            throw new Error("Invalid student credentials.");
        }
    },
    
    logout() {
        localStorage.removeItem('studentUser');
        window.location.href = 'index.html';
    },
    
    check() {
        const user = localStorage.getItem('studentUser');
        if (!user) {
            window.location.href = 'index.html';
            return null;
        }
        return JSON.parse(user);
    }
};

const StudentData = {
    async getAttendance(student_id) {
        return await fetchAPI(`/attendance/student/${student_id}`);
    },
    async getFees(student_id) {
        return await fetchAPI(`/fees/${student_id}`);
    }
};
