def side_bar_hide_style():
    return """
        <style>
            [data-testid="stSidebarCollapsedControl"] {
                display: none
            }
            #MainMenu {visibility: hidden;}
            [data-testid="stSidebar"] {display: none;}
            .shared-view-banner {
                background-color: #f0f2f6;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
                font-size: 14px;
            }
            .create-own-btn {
                display: inline-block;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin-left: 10px;
            }
            .create-own-btn:hover {
                background-color: #45a049;
            }
            .custom-title {
                color: #1E88E5;
                font-size: 2.5em;
                margin-bottom: 0.5em;
            }
            .subtitle {
                color: #666;
                font-size: 1.2em;
                margin-bottom: 2em;
            }
            .name-container {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border: 1px solid #e0e0e0;
            }
            .name-label {
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            .input-container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 800px;
                margin: 0 auto;
            }
            .stButton > button {
                width: 100%;
                margin-top: 20px;
                background-color: #1E88E5;
                color: white;
            }
            .stButton > button:hover {
                background-color: #1976D2;
            }
        </style>
    """;

def profile_view_style():
    return """
        <style>
            .profile-container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-top: 20px;
            }
            .profile-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f2f6;
            }
            .company-name {
                color: #1E88E5;
                font-size: 2em;
                margin: 0;
            }
            .profile-content {
                font-size: 1.1em;
                line-height: 1.6;
                color: #333;
            }
            .profile-content h1 {
                color: #1E88E5;
                font-size: 1.8em;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            .profile-content h2 {
                color: #2196F3;
                font-size: 1.5em;
                margin-top: 25px;
                margin-bottom: 12px;
            }
            .profile-content h3 {
                color: #42A5F5;
                font-size: 1.3em;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .profile-content p {
                margin-bottom: 15px;
            }
            .profile-content ul, .profile-content ol {
                margin-bottom: 15px;
                padding-left: 20px;
            }
            .profile-content li {
                margin-bottom: 8px;
            }
            .action-buttons {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 8px;
            }
            .generate-new-btn {
                display: inline-block;
                padding: 8px 16px;
                background-color: #1E88E5;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                text-align: center;
                margin-top: 20px;
            }
            .generate-new-btn:hover {
                background-color: #1976D2;
            }
        </style>
    """;