# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <title>📚 My Blog</title>
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
#   <style>
#     body { background-color: #f8f9fa; }
#     .card-title { font-weight: 600; }
#     .author-date { font-size: 0.9rem; color: #888; }
#     .comment-box { margin-top: 10px; }
#     .comment-meta { font-size: 0.75rem; color: #666; margin-top: 2px; }
#   </style>
# </head>
# <body>
#
# <div class="container mt-4">
#   <h2 class="text-center mb-4">📖 My Blog</h2>
#
#   <!--  Search Box -->
#   <div class="input-group mb-4">
#     <input type="text" id="search-input" class="form-control" placeholder="Search blog title/content...">
#     <button class="btn btn-outline-secondary" onclick="searchPosts()">Search</button>
#   </div>
#
#   <!--  Blog Posts -->
#   <div id="posts-container"></div>
#
#   <!--  Load More -->
#   <div class="text-center">
#     <button id="load-more-btn" class="btn btn-primary mt-3" onclick="loadPosts()">🔽 Load More</button>
#   </div>
# </div>
#
# <!--  JavaScript -->
# <script>
#   function getAuthHeaders() {
#     const token = localStorage.getItem("access");
#     return {
#       'Content-Type': 'application/json',
#       'Authorization': `Bearer ${token}`
#     };
#   }
#
#   let page = 1;
#   let hasNext = true;
#
#   async function loadPosts(reset = false, search = "") {
#     if (!hasNext && !reset) return;
#
#     const container = document.getElementById("posts-container");
#     if (reset) {
#       container.innerHTML = "";
#       page = 1;
#       hasNext = true;
#     }
#
#     const url = search
#       ? `/api/search/?q=${search}`
#       : `/api/posts/?page=${page}`;
#
#     const response = await fetch(url);
#     const data = await response.json();
#     const posts = data.results || data;
#
#     posts.forEach(post => {
#       const likeUsers = post.likes.length > 0 ? post.likes.join(', ') : 'No one yet';
#       const postHTML = `
#         <div class="card mb-4 shadow">
#           <div class="card-body">
#             <h5 class="card-title">${post.title}</h5>
#             <p class="author-date">👤 ${post.author} |  ${new Date(post.timestamp).toLocaleDateString()}</p>
#             <p class="card-text">${post.content.substring(0, 200)}...</p>
#
#             <!-- ❤️ Like + 🔗 Share -->
#             <div class="d-flex align-items-center mb-2">
#               <button class="btn btn-sm btn-outline-danger me-2" onclick="toggleLike(${post.id}, '${post.author}')">❤️ Like</button>
#               <button class="btn btn-sm btn-outline-success" onclick="sharePost(${post.id})">🔗 Share</button>
#               <small class="ms-3 text-muted" id="like-status-${post.id}">
#                 ❤️ Liked by: ${likeUsers}
#               </small>
#             </div>
#
#             <!--  Comment Box -->
#             <div class="comment-box">
#               <textarea id="comment-${post.id}" rows="1" class="form-control mb-2" placeholder="Add a comment..."></textarea>
#               <button class="btn btn-sm btn-outline-primary mb-2" onclick="submitComment(${post.id})">Post</button>
#               <div id="comments-${post.id}" class="mt-2"></div>
#             </div>
#           </div>
#         </div>`;
#       container.innerHTML += postHTML;
#       fetchComments(post.id);
#     });
#
#     if (!data.next && (!data.results || data.results.length < 2)) {
#       hasNext = false;
#       document.getElementById("load-more-btn").style.display = "none";
#     } else {
#       document.getElementById("load-more-btn").style.display = "inline-block";
#     }
#
#     page += 1;
#   }
#
#   async function toggleLike(postId, postAuthor) {
#     const res = await fetch(`/api/posts/${postId}/like/`, {
#       method: 'POST',
#       headers: getAuthHeaders()
#     });
#
#     if (res.status === 401) {
#       alert("🔒 Please login again.");
#       localStorage.removeItem("access");
#       window.location.href = "/login/";
#       return;
#     }
#
#     const updatedPostRes = await fetch(`/api/posts/${postId}/`, {
#       method: 'GET',
#       headers: getAuthHeaders()
#     });
#
#     const updatedPost = await updatedPostRes.json();
#     const likeUsers = updatedPost.likes.length > 0 ? updatedPost.likes.join(', ') : 'No one yet';
#     document.getElementById(`like-status-${postId}`).innerText = `❤ Liked by: ${likeUsers}`;
#   }
#
#   async function sharePost(postId) {
#     const url = `${window.location.origin}/posts/${postId}/`;
#     navigator.clipboard.writeText(url)
#       .then(() => alert("🔗 Post link copied to clipboard!"))
#       .catch(err => alert(" Failed to copy link"));
#   }
#
# async function submitComment(postId) {
#   const content = document.getElementById(`comment-${postId}`).value;
#   if (!content.trim()) return alert(" Please enter a comment.");
#
#   const res = await fetch(`/api/posts/${postId}/comments/`, {
#     method: 'POST',
#     headers: {
#       'Content-Type': 'application/json',
#       'Authorization': `Bearer ${localStorage.getItem("access")}`
#     },
#     body: JSON.stringify({ content: content })
#   });
#
#   if (res.status === 401) {
#     alert("🔒 Please login to post a comment.");
#     window.location.href = "/login/";
#     return;
#   }
#
#   if (res.ok) {
#     fetchComments(postId);  // refresh comments
#     document.getElementById(`comment-${postId}`).value = "";
#   } else {
#     alert("❌ Failed to post comment.");
#   }
# }
#
#   async function fetchComments(postId) {
#     const res = await fetch(`/api/posts/${postId}/comments/`);
#     const comments = await res.json();
#     const commentDiv = document.getElementById(`comments-${postId}`);
#     commentDiv.innerHTML = comments.map(c => `
#       <div>
#         <strong>${c.user}</strong>: ${c.content}
#         <div class="comment-meta">💬 ${c.user} commented</div>
#         <hr style="margin: 4px 0;">
#       </div>
#     `).join('');
#   }
#
#   function searchPosts() {
#     const query = document.getElementById('search-input').value.trim();
#     if (query) {
#       loadPosts(true, query);
#     }
#   }
#
#   document.addEventListener("DOMContentLoaded", () => {
#     loadPosts();
#   });
# </script>
#
# </body>
# </html>
