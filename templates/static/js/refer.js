 function IsEmail(email) {
  var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  if(!regex.test(email)) {
    return false;
  }else{
    return true;
  }
}
$(document).ready(function(){

      $("#login").click(function () {
      $('#error_msg').html("").hide()
      var username = $('#username').val();
      var password = $('#password').val();
      if(username=="" || password=="")
        {
            $('#error_msg').html("Please enter username and password").show()
        }
        else {
          $.ajax({
            url: '/refer/ajax/login',
            data: {
              'username': username,
              'password':password
            },
            dataType: 'json',
            method: 'post',
            success: function (data) {
              console.log(data)
                if(data.resp == 'redirect')
                {
                    window.location.href = "/refer/dashboard";
                }
                else{
                    $('#error_msg').html("Invalid username or password").show()
                }

            }
          });
        }
    });

    $('#email').on('input',function() {
        email = $(this).val();
        var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if(regex.test(email)) {
            //alert(email)
            $.ajax({
            url: 'ajax/patient/get',
            data: {
              'email': email
            },
            dataType: 'json',
            method: 'post',
            success: function (data) {
              console.log(data)
              $('#first_name').val(data.resp.first_name)
              $('#last_name').val(data.resp.last_name)
              $('#mobile_number').val(data.resp.mobile)
              $('#city').val(data.resp.city)
            }
          });
        }
       // do something
    });

    $("#refer").click(function () {
      var first_name = $('#first_name').val();
      var last_name = $('#last_name').val();
      var mobile_number = $('#mobile_number').val();
      var email = $('#email').val();
      var city = $('#city').val();
      var diagnosis = $('#diagnosis').val();
      var treatment = $('#treatment').val();
      $('.error').css('display', 'none')
      if (first_name!='' && last_name!='' && email!='' && mobile_number!=''){

      $.ajax({
        url: '/refer/ajax/patient',
        data: {
          'first_name': first_name,
          'last_name': last_name,
          'mobile_number':mobile_number,
          'email':email,
          'city':city,
          'diagnosis':diagnosis,
          'treatment':treatment,
        },
        dataType: 'json',
        method: 'post',
        success: function (data) {
          console.log(data)
            if(data.resp == 'redirect')
            {
                window.location.href = "";
            }

        }
      });
      }
      else{
        $('.error').css('display', 'block')
      }

    });

    $('#registerId').click(function(){
        $('#RegisterBox').css("display", "block")
    })

    $('.close').click(function(){
        $('#RegisterBox').css("display", "none")
    })



    $(".styled-table").fancyTable({
      sortColumn:0, // column number for initial sorting
      sortOrder: 'descending', // 'desc', 'descending', 'asc', 'ascending', -1 (descending) and 1 (ascending)
      sortable: true,
      pagination: true, // default: false
      searchable: true,
      globalSearch: true,
      globalSearchExcludeColumns: [2,5] // exclude column 2 & 5
    });
})

