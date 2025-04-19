📍 Project Overview
This repository hosts the Flask-based web application developed for BFA Company, consisting of a public-facing company website and a secured admin dashboard. The application was designed to streamline the company's online presence while providing administrative control over internal functionalities.

🛠️ Technologies Used
Flask – Lightweight Python web framework

HTML/CSS/JavaScript – Frontend interface

Jinja2 – Templating engine for dynamic rendering

MySQL – Relational database for persistent storage

Bootstrap – For responsive UI design

WTForms – For form handling and validation

Flask-Login – For authentication and session management

🚀 Features
🌍 Company Website
Informative landing pages about BFA’s services

Responsive design with modern UI

Contact and inquiry form

🧑‍💼 Admin Dashboard
Authentication-protected access

User and role management (Admin/Super Admin)

Image uploads and dynamic content display

Formateur management and notification system

Action history tracking with date, actor, and image references

Privilege-based button rendering (add, delete, modify)

Dynamic maps showing countries of formateurs

🔒 Role Management & Privileges
Admin: Can manage formateurs, depending on granted privileges

Super Admin: Has full control, including visibility over all actions

Privileges include: 'aj' (add), 'del' (delete), 'mod' (modify)

📸 Media & File Handling
Round-style profile images for formateurs and admins

Conditional display of formateur images (e.g., hide on deletion)

File upload customization (hiding file input when not needed)

🧠 Smart UI Behavior
Dynamic rendering based on admin privileges

Notifications with formatted messages:
Ex: "Admin John Doe has added this formateur"

Actions ordered from newest to oldest

Form handling supports full date structure (year/month/day)
