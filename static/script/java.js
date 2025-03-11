var btnUpload = $("#upload_file"),
  btnOuter = $(".button_outer");
btnUpload.on("change", function (e) {
  var ext = btnUpload.val().split('.').pop().toLowerCase();
  if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
    $(".error_msg").text("Not an Image...");
  } else {
    $(".error_msg").text("");
    btnOuter.addClass("file_uploading");
    setTimeout(function () {
      btnOuter.addClass("file_uploaded");
    }, 3000);

  }
});
// ````````````````````````````````````````````````

// java.js
document.addEventListener("DOMContentLoaded", function() {
  var modalOverlay = document.getElementById("modalOverlay");  // Overlay with modal
  var cancelBtn = document.getElementById("cancelDelete");     // Cancel button
  var deleteForm = document.getElementById("deleteForm");      // Form to handle delete

  // Select all delete buttons and add click event listener to each
  document.querySelectorAll('.delete-btn').forEach(button => {
      button.addEventListener('click', function(event) {
          event.preventDefault();  // Prevent default link behavior

          // Get the post ID from the data-id attribute of the clicked button
          var postId = this.getAttribute('data-id');
          deleteForm.action = `/post/${postId}/delete/`;  // Update form action with post ID

          modalOverlay.style.display = "flex";  // Show overlay and center modal
      });
  });

  // When the cancel button is clicked, hide the modal
  cancelBtn.addEventListener('click', function() {
      modalOverlay.style.display = "none";  // Hide the overlay and modal
  });
});


// ``````````````````````messages````````````````````````````````````````````
window.onload = function() {
  // Select the message box
  const messageBox = document.getElementById('message-box');
  if (messageBox) {
      // Set timeout to hide the message after 3 seconds
      setTimeout(function() {
          messageBox.style.display = 'none';
      }, 3000); // 3000ms = 3 seconds
  }
};
// `````````````````````````````````````````
function goToContactPage() {
  window.location.href = "/contact-us/"; // Replace with your contact page route
}

function goToHomePage() {
  window.location.href = "/"; // Replace with your homepage route
}
// ````````````````````like and comment implementation``````````````````````
// Function to retrieve CSRF token from cookies (needed for AJAX POST requests)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function(){
    // Like button event
    $('#like-btn').click(function(){
        const postId = $(this).data('post');
        $.ajax({
            type: "POST",
            url: `/post/${postId}/like-dislike/`,
            data: {
                'like': '1',  // '1' indicates a like action
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response){
                // Update like/dislike counts in the template
                $('#like-count').text(response.likes);
                $('#dislike-count').text(response.dislikes);
            },
            error: function(){
                alert("Error processing like.");
            }
        });
    });

    // Dislike button event
    $('#dislike-btn').click(function(){
        const postId = $(this).data('post');
        $.ajax({
            type: "POST",
            url: `/post/${postId}/like-dislike/`,
            data: {
                'like': '0',  // '0' indicates a dislike action
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response){
                $('#like-count').text(response.likes);
                $('#dislike-count').text(response.dislikes);
            },
            error: function(){
                alert("Error processing dislike.");
            }
        });
    });

    // Comment form submission event
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    $('#comment-form').submit(function (e) {
        e.preventDefault();
    
        let postId = $('#like-btn').data('post');  // Get post ID from like button
        let commentText = $('#comment-input').val();
        let csrfToken = getCSRFToken();
    
        console.log("Submitting comment to: /post/" + postId + "/add-comment/");
    
        $.ajax({
            type: "POST",
            url: `/post/${postId}/add-comment/`,  // Use dynamic post ID
            data: {
                'comment': commentText,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (response) {
                console.log("Comment added successfully:", response);
                const profileImageUrl = response.profile_image ? response.profile_image : "/static/img/defaultimage.png";
                $('#comments-container').prepend(`
                    <div class="comment">
                        <img src="${profileImageUrl}" alt="User Profile" class="user-img">
                        <div class="comment-content">
                            <h4>${response.username} <span class="timestamp">${response.created_at}</span></h4>
                            <p>${response.comment}</p>
                        </div>
                    </div>`);
                $('#comment-input').val('');
            },
            error: function (xhr) {
                console.log("Error response:", xhr.responseText);
                alert("Error adding comment😪.");
            }
        });
    });
    
    // Share button functionality: Copy current URL to clipboard
    $('#share-btn').click(function(){
        // Create a temporary input element to copy the URL
        const dummy = $("<input>").val(window.location.href).appendTo("body").select();
        document.execCommand("copy");
        dummy.remove();
        alert("Link copied to clipboard!");
    });
});



 