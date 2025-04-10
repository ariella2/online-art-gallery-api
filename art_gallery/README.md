# Online Art Gallery API

A RESTful API for an online art gallery platform built with Django and Django REST Framework. This API allows artists to showcase their artwork, manage their portfolio, and interact with art enthusiasts.

## Project Description

The Online Art Gallery API provides a platform for artists to:
- Create and manage their artwork portfolios
- Categorize their artworks
- Upload multiple images for each artwork
- Control access to their artworks
- Interact with other artists and art enthusiasts

## Main Features

- **User Authentication**: Secure JWT-based authentication system
- **Artwork Management**: Create, read, update, and delete artworks
- **Image Management**: Support for multiple images per artwork with primary image selection
- **Category System**: Organize artworks into categories
- **User Profiles**: Artist profiles with their artwork collections
- **Access Control**: Private and public endpoints with proper authorization

## Users

1. **Artists Users**
   - Can create and manage their artwork
   - Can create categories
   - Can view their own artwork collection
   - Can update and delete their artworks

2. **Client Users**
   - Can browse artworks
   - Can view artwork details
   - Can filter artworks by category

## API Endpoints

### Authentication
- `POST /api/register/` - Register a new artist
- `POST /api/login/` - Login and get JWT tokens

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category (authenticated)

### Artworks
- `GET /api/artworks/` - List all artworks
- `POST /api/artworks/` - Create a new artwork (authenticated)
- `GET /api/artworks/artwork/<int:artwork_id>/` - Get artwork details
- `PUT /api/artworks/artwork/<int:artwork_id>/` - Update artwork (authenticated)
- `DELETE /api/artworks/artwork/<int:artwork_id>/` - Delete artwork (authenticated)
- `GET /api/artworks/category/<int:category_id>/` - List artworks by category
- `GET /api/artworks/user/<int:user_id>/` - List user's artworks (authenticated)
- `GET /api/my-artworks/` - List authenticated user's artworks

## Technologies Used

- **Backend Framework**: Django Framework
- **API Framework**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MySQL

## Installation Prerequisites

1. **Python 3.12.6 or higher**
2. **MySQL Server**
3. **pip** (Python package manager)

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ariella2/online-art-gallery-api.git
   cd online-art-gallery-api
   ```

3. Configure the database:
   - Create a MySQL database named `art_gallery_db`
   - Update database settings in `art_gallery/settings.py` if needed

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API uses JWT for authentication. To access protected endpoints:

1. Register a new user at `/api/register/`
2. Login at `/api/login/` to get your access token
3. Include the token in your requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 