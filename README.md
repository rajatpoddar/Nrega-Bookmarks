# 🚀 NREGA Bookmarks Dashboard

A powerful, dynamic, and centralized bookmarking dashboard tailored for
NREGA (Mahatma Gandhi National Rural Employment Guarantee Act) workers,
Program Officers (POs), and government officials.

This platform simplifies access to crucial NREGA portals, auto-generates
dynamic links based on selected districts and blocks, and offers a
seamless, modern UI with multi-theme support.

------------------------------------------------------------------------

## ✨ Key Features

-   **🔗 Dynamic URL Generation:** Automatically fills in District
    Codes, Block Codes, and Financial Year variables into URLs, saving
    users from manual entry.
-   **🎨 Multi-Theme Support:** Choose from 7 highly optimized themes
    including Default Slate, NREGA Classic, Midnight Blue, Dark Coffee,
    Sunset Purple, Light Day, and Light Warm.
-   **📱 Fully Responsive & Ad-Ready:** Built with a mobile-first
    approach using Tailwind CSS, featuring dedicated AdSense
    placeholders for desktop and mobile feeds.
-   **🔐 Admin Control Panel:** A secure dashboard to manage categories,
    add/edit/delete links, and broadcast custom promotional messages or
    greetings to all users.
-   **💡 User Suggestions:** A built-in modal for users to suggest new
    useful links, which admins can easily approve or reject.
-   **⚙️ Production Ready:** Containerized using Docker and served
    securely via Gunicorn.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Backend:** Python 3.9, Flask
-   **Database:** SQLite (SQLAlchemy)
-   **Frontend:** HTML5, Tailwind CSS, FontAwesome/MDI Icons
-   **Deployment:** Docker, Docker Compose, Gunicorn

------------------------------------------------------------------------

## 🚀 Quick Setup & Deployment

### Prerequisites

Make sure you have Docker and Docker Compose installed on your server or
NAS.

### 1. Clone the Repository

``` bash
git clone https://github.com/rajatpoddar/Nrega-Bookmarks.git
cd Nrega-Bookmarks
```

### 2. Deploy with Docker

Run the automated update script or use docker-compose directly:

``` bash
chmod +x update.sh
sudo ./update.sh
```

The application will now be running on port **6006** (or the port
specified in your `docker-compose.yml`).

### 3. Seed the Database (First-time setup only)

To populate the database with real districts, blocks, and the default
application links, execute the seed scripts inside your running
container:

``` bash
sudo docker exec -it nrega_bookmarks_app python seed_db.py
sudo docker exec -it nrega_bookmarks_app python seed_bookmarks.py
```

------------------------------------------------------------------------

## 📂 Project Structure

    Nrega-Bookmarks/
    ├── app.py                  # Main Flask application and routing
    ├── seed_db.py              # Web scraper to fetch Districts & Blocks
    ├── seed_bookmarks.py       # Default NREGA categories & links seeder
    ├── requirements.txt        # Python dependencies
    ├── Dockerfile              # Docker image configuration
    ├── docker-compose.yml      # Docker compose configuration
    ├── update.sh               # Auto-pull and rebuild script
    ├── instance/               # Persistent database volume (created on run)
    └── templates/              # HTML Templates
        ├── base.html           # Master layout and theme CSS
        ├── index.html          # Main user dashboard
        ├── admin.html          # Admin control panel
        └── edit_link.html      # Link editor interface

------------------------------------------------------------------------

## 📝 Customization

**Greeting Message:**\
Set a custom global promotional message directly from the Admin Panel.

**Ads:**\
To enable Google AdSense, place your `ca-pub-XXXX` script in the
`<head>` of `templates/base.html` and update the `ads.txt` route in
`app.py`.

------------------------------------------------------------------------

Maintained with ❤️ by **Rajat Poddar**
