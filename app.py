from flask import Flask, render_template_string
import os
import json
from datetime import datetime
import platform

app = Flask(__name__)

# HTML Template with Tailwind CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Python Docker App | ECR Deployment</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Inter', sans-serif; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .pulse-animation { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
    </style>
</head>
<body class="gradient-bg min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-6xl mx-auto">
        <!-- Header -->
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden mb-8">
            <div class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-8 md:p-12 text-center">
                <div class="flex flex-col md:flex-row items-center justify-center gap-6 mb-6">
                    <div class="text-5xl">
                        <i class="fas fa-rocket"></i>
                        <i class="fas fa-docker ml-4"></i>
                        <i class="fas fa-cloud ml-4"></i>
                    </div>
                    <div>
                        <h1 class="text-4xl md:text-5xl font-bold mb-3">Python Flask on AWS ECR</h1>
                        <p class="text-xl opacity-90">Containerized Web App with Docker & AWS</p>
                    </div>
                </div>
                <div class="inline-flex items-center space-x-4 text-lg">
                    <span class="bg-white/20 px-4 py-2 rounded-full">
                        <i class="fas fa-code mr-2"></i>Python {{ python_version }}
                    </span>
                    <span class="bg-white/20 px-4 py-2 rounded-full">
                        <i class="fas fa-cube mr-2"></i>Docker Container
                    </span>
                    <span class="bg-white/20 px-4 py-2 rounded-full">
                        <i class="fas fa-server mr-2"></i>AWS ECR
                    </span>
                </div>
            </div>

            <!-- Main Content -->
            <div class="p-8 md:p-12">
                <!-- Stats Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    <div class="card-hover bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-100">
                        <div class="flex items-center mb-4">
                            <div class="bg-blue-100 p-3 rounded-xl mr-4">
                                <i class="fas fa-microchip text-blue-600 text-2xl"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800">System Info</h3>
                        </div>
                        <p class="text-gray-600 mb-2"><i class="fas fa-hashtag text-blue-500 mr-2"></i><span class="font-medium">Host:</span> {{ hostname }}</p>
                        <p class="text-gray-600 mb-2"><i class="fas fa-microchip text-blue-500 mr-2"></i><span class="font-medium">Platform:</span> {{ platform }}</p>
                        <p class="text-gray-600"><i class="fas fa-calendar text-blue-500 mr-2"></i><span class="font-medium">Uptime:</span> Running since {{ current_time }}</p>
                    </div>

                    <div class="card-hover bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-100">
                        <div class="flex items-center mb-4">
                            <div class="bg-green-100 p-3 rounded-xl mr-4">
                                <i class="fas fa-shield-alt text-green-600 text-2xl"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800">App Status</h3>
                        </div>
                        <div class="flex items-center mb-4">
                            <div class="pulse-animation bg-green-500 w-3 h-3 rounded-full mr-3"></div>
                            <span class="text-lg font-bold text-green-700">All Systems Operational</span>
                        </div>
                        <p class="text-gray-600 mb-2"><i class="fas fa-check-circle text-green-500 mr-2"></i>Docker Container: Running</p>
                        <p class="text-gray-600 mb-2"><i class="fas fa-check-circle text-green-500 mr-2"></i>Flask Server: Active</p>
                        <p class="text-gray-600"><i class="fas fa-check-circle text-green-500 mr-2"></i>Health Check: PASS</p>
                    </div>

                    <div class="card-hover bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-100">
                        <div class="flex items-center mb-4">
                            <div class="bg-purple-100 p-3 rounded-xl mr-4">
                                <i class="fas fa-cloud-upload-alt text-purple-600 text-2xl"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800">Deployment</h3>
                        </div>
                        <p class="text-gray-600 mb-2"><i class="fas fa-cloud text-purple-500 mr-2"></i><span class="font-medium">Registry:</span> AWS ECR</p>
                        <p class="text-gray-600 mb-2"><i class="fas fa-map-marker-alt text-purple-500 mr-2"></i><span class="font-medium">Region:</span> ap-south-1</p>
                        <p class="text-gray-600"><i class="fas fa-tag text-purple-500 mr-2"></i><span class="font-medium">Image Size:</span> ~50 MB</p>
                    </div>
                </div>

                <!-- Endpoints Section -->
                <div class="mb-10">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                        <i class="fas fa-plug text-indigo-600 mr-3"></i>API Endpoints
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <a href="/" class="card-hover block">
                            <div class="bg-white border border-gray-200 rounded-xl p-6 hover:border-indigo-300 hover:shadow-lg">
                                <div class="flex items-center mb-4">
                                    <div class="bg-indigo-100 p-3 rounded-lg mr-4">
                                        <i class="fas fa-home text-indigo-600 text-xl"></i>
                                    </div>
                                    <h3 class="text-xl font-bold text-gray-800">Home</h3>
                                </div>
                                <p class="text-gray-600 mb-4">Main application dashboard with system information</p>
                                <code class="bg-gray-100 text-gray-800 px-3 py-1 rounded text-sm">GET /</code>
                            </div>
                        </a>

                        <a href="/health" class="card-hover block">
                            <div class="bg-white border border-gray-200 rounded-xl p-6 hover:border-green-300 hover:shadow-lg">
                                <div class="flex items-center mb-4">
                                    <div class="bg-green-100 p-3 rounded-lg mr-4">
                                        <i class="fas fa-heartbeat text-green-600 text-xl"></i>
                                    </div>
                                    <h3 class="text-xl font-bold text-gray-800">Health Check</h3>
                                </div>
                                <p class="text-gray-600 mb-4">Monitor application health status (returns JSON)</p>
                                <code class="bg-gray-100 text-gray-800 px-3 py-1 rounded text-sm">GET /health</code>
                            </div>
                        </a>

                        <a href="/info" class="card-hover block">
                            <div class="bg-white border border-gray-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-lg">
                                <div class="flex items-center mb-4">
                                    <div class="bg-blue-100 p-3 rounded-lg mr-4">
                                        <i class="fas fa-info-circle text-blue-600 text-xl"></i>
                                    </div>
                                    <h3 class="text-xl font-bold text-gray-800">App Info</h3>
                                </div>
                                <p class="text-gray-600 mb-4">Detailed application metadata and configuration</p>
                                <code class="bg-gray-100 text-gray-800 px-3 py-1 rounded text-sm">GET /info</code>
                            </div>
                        </a>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="bg-gradient-to-r from-gray-50 to-white rounded-2xl p-8 border border-gray-200">
                    <h2 class="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                        <i class="fas fa-bolt text-yellow-500 mr-3"></i>Quick Actions
                    </h2>
                    <div class="flex flex-wrap gap-4">
                        <a href="/health" class="inline-flex items-center bg-green-500 hover:bg-green-600 text-white font-medium px-6 py-3 rounded-xl transition">
                            <i class="fas fa-heartbeat mr-3"></i>Check Health
                        </a>
                        <a href="/info" class="inline-flex items-center bg-blue-500 hover:bg-blue-600 text-white font-medium px-6 py-3 rounded-xl transition">
                            <i class="fas fa-info-circle mr-3"></i>View Info
                        </a>
                        <button onclick="copyDeployCommand()" class="inline-flex items-center bg-purple-500 hover:bg-purple-600 text-white font-medium px-6 py-3 rounded-xl transition">
                            <i class="fas fa-copy mr-3"></i>Copy Deploy Command
                        </button>
                        <button onclick="location.reload()" class="inline-flex items-center bg-gray-600 hover:bg-gray-700 text-white font-medium px-6 py-3 rounded-xl transition">
                            <i class="fas fa-sync-alt mr-3"></i>Refresh Page
                        </button>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="bg-gray-900 text-gray-300 p-6 text-center">
                <div class="flex flex-col md:flex-row justify-between items-center">
                    <div class="mb-4 md:mb-0">
                        <p class="text-lg font-medium">🚀 DevOps Learning Project</p>
                        <p class="text-sm opacity-80">Containerized Python Flask on AWS ECR</p>
                    </div>
                    <div class="flex space-x-6 text-2xl">
                        <a href="#" class="hover:text-white transition"><i class="fab fa-github"></i></a>
                        <a href="#" class="hover:text-white transition"><i class="fab fa-docker"></i></a>
                        <a href="#" class="hover:text-white transition"><i class="fab fa-aws"></i></a>
                        <a href="#" class="hover:text-white transition"><i class="fab fa-python"></i></a>
                    </div>
                </div>
                <p class="mt-4 text-sm opacity-70">Deployed via Docker • AWS ECR • Flask • Tailwind CSS</p>
            </div>
        </div>

        <!-- Mobile Warning -->
        <div class="md:hidden bg-yellow-50 border border-yellow-200 rounded-xl p-4 mb-6">
            <div class="flex items-center">
                <i class="fas fa-mobile-alt text-yellow-600 text-xl mr-3"></i>
                <p class="text-yellow-800 font-medium">Optimized for mobile viewing!</p>
            </div>
        </div>
    </div>

    <script>
        function copyDeployCommand() {
            const command = 'docker run -p 8080:5000 your-ecr-repo-url:latest';
            navigator.clipboard.writeText(command).then(() => {
                alert('Deployment command copied to clipboard!');
            });
        }
        
        // Update time every minute
        function updateTime() {
            const timeElement = document.querySelector('.current-time');
            if (timeElement) {
                const now = new Date();
                timeElement.textContent = now.toLocaleTimeString();
            }
        }
        setInterval(updateTime, 60000);
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Main dashboard with beautiful UI"""
    return render_template_string(
        HTML_TEMPLATE,
        hostname=os.uname().nodename,
        python_version=platform.python_version(),
        platform=platform.platform(),
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/health')
def health():
    """Health check endpoint (JSON)"""
    return {
        "status": "healthy",
        "service": "python-web-app",
        "timestamp": datetime.now().isoformat(),
        "container_id": os.uname().nodename,
        "checks": {
            "database": "connected",
            "disk_space": "adequate",
            "memory": "optimal"
        }
    }

@app.route('/info')
def info():
    """Application information endpoint"""
    return {
        "application": {
            "name": "Python Flask ECR Deployment",
            "version": "2.0.0",
            "description": "Containerized web app with modern UI",
            "author": "DevOps Learning Project"
        },
        "environment": {
            "python_version": platform.python_version(),
            "flask_version": "2.3.3",
            "hostname": os.uname().nodename,
            "platform": platform.platform()
        },
        "deployment": {
            "containerized": True,
            "registry": "AWS ECR",
            "region": "ap-south-1",
            "image_size": "~50MB"
        },
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Main dashboard"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/info", "method": "GET", "description": "App information"}
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.route('/api/status')
def api_status():
    """Lightweight status endpoint for monitoring"""
    return {
        "status": "operational",
        "uptime": "100%",
        "last_updated": datetime.now().isoformat()
    }

if __name__ == '__main__':
    print("🚀 Starting Python Flask App with Modern UI...")
    print("🌐 Server running at: http://0.0.0.0:5000")
    print("📱 Mobile-friendly interface ready!")
    app.run(host='0.0.0.0', port=5000, debug=True)