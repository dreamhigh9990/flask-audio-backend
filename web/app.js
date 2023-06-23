$(function() {

  // Add User Submission
  var $addUserForm = $("#add-user-form"),
      $addUserSuccess = $("#add-user-success");
  
  $addUserForm.on("submit", function(e) {
    
    var data = {
      first_name: $addUserForm.find("#first_name").val(),
      last_name: $addUserForm.find("#last_name").val(),
      email: $addUserForm.find("#email").val(),
      password: $addUserForm.find("#password").val(),
    };

    console.log(data);

    $.ajax({
      url: "http://127.0.0.1:5000/user/",
      type: "POST",
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data),
      success: function(resp) {
        console.log(resp);
        $addUserForm.hide();
        $addUserSuccess.show();
      },
      error: function(error) {
        console.error(error);
        alert(error.responseJSON.message)
      }
    });
    
    e.preventDefault();
  });

  // User Login Submission
  var $loginForm = $("#login-form"),
      $loginSuccess = $("#login-success");
  
  $loginForm.on("submit", function(e) {
    
    var data = {
      email: $loginForm.find("#email").val(),
      password: $loginForm.find("#password").val(),
    };

    console.log(data);

    $.ajax({
      url: "http://127.0.0.1:5000/user/login/",
      type: "POST",
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data),
      success: function(resp) {
        window.access_token = resp.access_token
        window.refresh_token = resp.refresh_token
        window.username = resp.first_name
        console.log(resp);
        $loginForm.hide();
        $loginSuccess.show();
      },
      error: function(error) {
        console.error(error);
        alert(error.responseJSON.message)
      }
    });
    
    e.preventDefault();
  });
  
});

// User Upload Submission
var $uploadForm = $("#upload-form"),
  $uploadSuccess = $("#upload-success"),
  $uploadFile = $("#voice_file")

$uploadForm.on("submit", function(e) {
  var formData = new FormData()
  
  formData.append('file', $uploadFile[0].files[0])
  try {
    $.ajax({
      url: "http://127.0.0.1:5000/voice/upload/",
      type: "POST",
      method: "POST",
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      dataType: 'json',
      headers: {
        AccessToken: window.access_token
      },
      success: function(resp) {
        console.log(resp)
        $uploadForm.hide()
        $uploadSuccess.show()
      },
      error: function(error) {
        alert('failed')
      }
    })
    e.preventDefault();
  } catch (e) {
    console.log(e.message)
  }
});

// Dialog Upload Submission
var $uploadDialogForm = $("#upload-dialog-form"),
  $uploadDialogSuccess = $("#upload-dialog-success"),
  $uploadDialogFile = $("#dialog_file")

$uploadDialogForm.on("submit", function(e) {
  var formData = new FormData()
  
  formData.append('file', $uploadDialogFile[0].files[0])
  try {
    $.ajax({
      url: "http://127.0.0.1:5000/voice/upload/dialog/",
      type: "POST",
      method: "POST",
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      dataType: 'json',
      headers: {
        AccessToken: window.access_token
      },
      success: function(resp) {
        console.log(resp)
        if (resp.success) {
          $("#voice_percent").text("Speaker 1: " + (resp.result.voice * 100).toFixed(0) + "%")
          $("#audience_percent").text("Speaker 2: " + (resp.result.audience * 100).toFixed(0) + "%")
          $uploadDialogForm.hide()
          $uploadDialogSuccess.show()
        }
      },
      error: function(error) {
        alert('failed')
      }
    })
    e.preventDefault();
  } catch (e) {
    console.log(e.message)
  }
});
