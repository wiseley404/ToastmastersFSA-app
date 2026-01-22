# 🎤 Toastmasters FSA-ULaval Club Management App

A comprehensive & responsive web application for managing a Toastmasters club at Université Laval. 
This app automates club operations including meeting management, member tracking, evaluations, email campaigns, and performance analytics.
[See the website live here](https://toastmastersfsa-app-production.up.railway.app/)

## 🎯 Features

- **Meeting Management**: Schedule meetings, assign roles, generate PDF agendas
- **Member Profiles**: Track progress, pathways, curriculums, and achievements
- **Speech Evaluations**: Digital evaluation forms with criteria-based feedback
- **Email Automation**: Scheduled emails, reminders, marketing campaigns with template system
- **Statistics Dashboard**: Member activity tracking, club performance metrics with Chart.js visualizations
- **Social Media Integration**: Centralized management of club social media links
- **Document Management**: Upload and organize meeting resources, agendas, and materials
- **Role Assignment**: Automatic role distribution for meetings with conflict detection
- **Responsive Design**: Mobile-first design for access on any device

## 🔐 User Roles

The app features **role-based access control**:

- **Members**: View schedules, manage personal profile, submit evaluations, ...
- **Board Members**: Full administrative access including meeting creation, member management, email campaigns, analytics, and club configuration.

*Screenshots below show the board member interface with complete access.*

## 📸 Screenshots

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/64dcfb99-d5ae-4534-b963-86875186e8e8" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/ea187f6a-bf6c-4c31-98ab-791c118d74d4" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/2d3e8cd6-5b97-42c5-8a17-2f2311221979" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/81adedd3-0d1f-4c88-bebc-fc1e9f9659b7" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/7509deac-74f4-40f7-b3f1-081e8426cbe7" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/e1d79a61-b910-4fbc-b76b-94f047a928cb" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/8868ed88-091c-4180-9ee1-a57ebb194e30" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/7cd95523-95fe-40fb-8329-d743c7c6175c" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/cca6f018-9938-42d5-b4f0-3d30316acec9" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/2701aa12-f111-47e7-9cee-6782bd3ebeb9" />



## 🛠️ Tech Stack

**Backend:**
- Django 5.2 (Python web framework)
- PostgreSQL (database)
- Celery (async task queue)
- Redis (message broker & caching)

**Frontend:**
- HTML5, CSS3 (custom responsive design)
- JavaScript (Vanilla - AJAX, animations, dynamic forms)
- Bootstrap 5 (minimal - grid system & utilities)
- Chart.js (statistics visualizations)
- Font Awesome (icons)

**Deployment:**
- Railway (PostgreSQL + Redis + Web hosting)
- Docker & Docker Compose (containerization)
- Nginx (static files serving)

**Email & Authentication:**
- Django SMTP (email backend)
- Django Allauth (authentication & email verification)

## 📁 Project Structure
```
ToastmastersFSA/
├── accounts/              # User authentication, signup, password reset
├── communications/        # Email campaigns, scheduling, templates
├── core/                  # Core models (Statut, etc.) and utilities
├── forms/                 # Custom form handling
├── meetings/              # Meeting management, roles, agendas, resources
├── members/               # Member profiles, curriculums, progression tracking
├── speechs/               # Speech evaluations, criteria, feedback system
├── templates/             # Global HTML templates
│   └── includes/          # Reusable components (navbar, popup, etc.)
├── static/                # CSS, JavaScript, images
│   ├── css/               # Global css style (base, popup, etc.)
│   ├── js/                # Global JavaScript (popup, forms, etc.)
│   └── images/            # Static images
├── media/                 # User-uploaded files (photos, documents)
├── ToastmastersFSA/       # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   └── celery.py          # Celery configuration
├── docker-compose.yaml    # Docker services configuration
├── Dockerfile             # Docker container definition
├── requirements.txt       # Python dependencies
└── manage.py              # Django management script
```

## 🔑 Key Apps

| App | Description |
|-----|-------------|
| **accounts** | User authentication, registration, password management |
| **communications** | Email system with scheduling, templates, and campaigns |
| **core** | Shared models and utilities (status management) |
| **meetings** | Meeting creation, role assignments, agenda generation |
| **members** | Member profiles, curriculum tracking, statistics |
| **speechs** | Speech evaluations with customizable criteria |

## 🚀 Live Demo

[Lien: https://toastmastersfsa-app-production.up.railway.app]

## 💡 Key Technical Features

- **AJAX-based popups** for seamless CRUD operations without page reloads
- **Celery scheduled tasks** for automated email reminders and campaigns
- **Dynamic form handling** with validation and error display
- **PDF generation** for meeting agendas
- **Responsive CSS** with mobile-first approach
- **Database optimization** with select_related and prefetch_related queries
- **Custom authentication flow** with email verification

## 👨‍💻 Author
Developed by **[Ton Nom]**  
🐙 [GitHub] [https://github.com/wiseley404/]
🌐 [Portfolio/Site Web] [https://github.io/wiseley404/portfolio]   
📧 [Email] [mailto:wppet@ulaval.ca]  
💼 [LinkedIn ][https://www.linkedin.com/in/petitonwiseley]


## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Note**: This project is tailored specifically for Toastmasters FSA-ULaval club operations but the app is not in use currently. 
