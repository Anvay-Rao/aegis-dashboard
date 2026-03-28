const API_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("access_token");
}

function checkAuth() {
    if (!getToken()) {
        console.log("No token found, redirecting to index.html");
        window.location.href = "index.html";
    }
}

function logout() {
    console.log("Logging out.");
    localStorage.removeItem("access_token");
    window.location.href = "index.html";
}

function initAuth() {
    const loginForm = document.getElementById("login-form");
    if (loginForm && !loginForm.dataset.bound) {
        loginForm.dataset.bound = "true";
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            console.log("Login form submitted");
            
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const errorMsg = document.getElementById("error-msg");

            const body = new URLSearchParams({
                "username": username,
                "password": password
            });

            try {
                console.log(`Sending login request to ${API_URL}/login`);
                const response = await fetch(`${API_URL}/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: body
                });

                console.log("Response received:", response.status);

                if (response.ok) {
                    const data = await response.json();
                    console.log("Token received, storing to localStorage.");
                    localStorage.setItem("access_token", data.access_token);
                    console.log("Redirecting to dashboard.html");
                    window.location.href = "dashboard.html";
                } else {
                    console.log("Login failed");
                    if (errorMsg) {
                        errorMsg.innerText = "ACCESS DENIED. Invalid Credentials.";
                        errorMsg.style.display = "block";
                    }
                }
            } catch (error) {
                console.error("Login error:", error);
                if (errorMsg) {
                    errorMsg.innerText = "CONNECTION ERROR. System Offline.";
                    errorMsg.style.display = "block";
                }
            }
        });
    }
}

initAuth();

if (!window.location.pathname.endsWith("index.html") && !window.location.pathname.endsWith("/")) {
    checkAuth();
}
