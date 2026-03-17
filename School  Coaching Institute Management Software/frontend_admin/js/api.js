const API_BASE_URL = 'http://127.0.0.1:5000/api';

// Utility to handle API responses
async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Default headers
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

// Auth API
const Auth = {
    async login(username, password) {
        const data = await fetchAPI('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        if (data.status === 'success' && data.user.role === 'admin') {
            localStorage.setItem('adminUser', JSON.stringify(data.user));
            return data.user;
        } else {
            throw new Error("Unauthorized or not an admin account.");
        }
    },
    
    logout() {
        localStorage.removeItem('adminUser');
        window.location.href = 'login.html';
    },
    
    check() {
        const user = localStorage.getItem('adminUser');
        if (!user) {
            window.location.href = 'login.html';
            return null;
        }
        return JSON.parse(user);
    }
};

// Students API
const Students = {
    async getAll() {
        return await fetchAPI('/students');
    },
    async create(studentData) {
        return await fetchAPI('/students', {
            method: 'POST',
            body: JSON.stringify(studentData)
        });
    },
    async delete(id) {
        return await fetchAPI(`/students/${id}`, {
            method: 'DELETE'
        });
    }
};

// Fees API
const Fees = {
    async getAll() {
        return await fetchAPI('/fees');
    },
    async pay(fee_id, amount) {
        return await fetchAPI('/fees/pay', {
            method: 'POST',
            body: JSON.stringify({ fee_id, amount })
        });
    }
};

// Attendance API
const Attendance = {
    async getAll(date = '') {
        const url = date ? `/attendance?date=${date}` : '/attendance';
        return await fetchAPI(url);
    },
    async mark(student_id, date, status) {
        return await fetchAPI('/attendance', {
            method: 'POST',
            body: JSON.stringify({ student_id, date, status })
        });
    }
};
