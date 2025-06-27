# Blog-Project
User Authentication

Implemented JWT-based login and registration using Django REST Framework.

Used SimpleJWT for generating access and refresh tokens.

Login/Register available via both frontend and Postman.

Blog Management (CRUD APIs)

Created APIs for:

✅ Listing blog posts (with pagination of 10 per page)

✅ Creating a blog post

✅ Updating and deleting (only by the blog's author)

✅ Getting blog details

Used APIView and GenericAPIView (like ListCreateAPIView, RetrieveUpdateDestroyAPIView).

Pagination

Implemented via DRF settings:

python
Copy
Edit
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
Likes and Comments

Users can like a post once.

Comments are associated with a blog post and user.

All handled via DRF views and displayed on the frontend.

Frontend (index.html)

Designed using Bootstrap.

Shows:

Blog post title, content preview, author, date-

user http://127.0.0.1:8000/
![image](https://github.com/user-attachments/assets/beadca7c-9980-4b25-bf2a-4e1da0e8a0f5)


❤️ Like, 🔗 Share, 💬 Comment box

Logged-in user displayed on top-left corner

🔽 Load More button for pagination (2 posts/page for testing, can change to 10)

📌 API Endpoints Summary
Endpoint	Method	Description
/api/token/	POST	Login to get JWT tokens
http://127.0.0.1:8000/api/token/
![image](https://github.com/user-attachments/assets/0b34cb66-28cb-4a76-aecc-0ae0a9a950d6)


I built a blog platform using Django REST Framework with JWT login. Users can create/manage posts, like,
 comment, and view with pagination and search. Frontend is built using Bootstrap + JS, and permissions are
 enforced to allow only the post creator to modify posts.

 🛠️ Recent Fixes & Updates:
✅ Reintegrated like & comment functionality from the previously working version.

✅ Fixed new user issue: Now, newly registered users can successfully add blogs, and the blogs show up correctly on the main page.

✅ Ensured only authors can update/delete their posts.

✅ Combined search functionality with paginated blog listing.

✅ Improved frontend JavaScript logic for better user experience and cleaner code.

