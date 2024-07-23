// Add comment here
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


    $("#refer").click(function () {
      var first_name = $('#first_name').val();
      var last_name = $('#last_name').val();
      var mobile_number = $('#mobile_number').val();
      var email = $('#email').val();
      var city = $('#city').val();
      var diagnosis = $('#diagnosis').val();
      var treatment = $('#treatment').val();
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