    $(document).ready(function(){

    $("#login").click(function() {
            $('#error_msg').html("").hide()
            var username = $('#username').val();
            var password = $('#password').val();
            if(username=="" || password=="")
            {
                $('#error_msg').html("Please enter username and password").show()
            }
            else {
            $.ajax({
            url: '/admin/ajax/login',
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
                    window.location.href = "/admin/dashboard";
                }
                else{
                    $('#error_msg').html("Invalid username or password").show()
                }

            }
            });
            }
        });


    $("#register").click(function() {
      var username = $('#username').val();
      var password = $('#password').val();
      var first_name = $('#first_name').val();
      var last_name = $('#last_name').val();
      var mobile = $('#mobile').val();
      var email = $('#email').val();
      var user_type_id = $('#user_type_id').val();
      if (username != "" && password != "" && first_name != "" && last_name != "" && mobile != "" && email != "") {
      $.ajax({
        url: '/admin/ajax/register',
        data: {
          'username': username,
          'password':password,
          'first_name':first_name,
          'last_name':last_name,
          'mobile':mobile,
          'email':email,
          'user_type' : user_type_id
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
    });

    $('#registerId').click(function(){
        $('#RegisterBox').css("display", "block")
    })

    $('.close').click(function(){
        $('#RegisterBox').css("display", "none")
    })

    $("#addCoupon").click(function() {
      $("#error_msg").css("display","block")
      var coupon_name = $('#coupon_name').val();
      var coupon_code = $('#coupon_code').val();
      var coupon_value = $('#coupon_value').val();
      var coupon_description = $('#coupon_description').val();
      if (coupon_name == "" || coupon_code == "" || coupon_value == ""){
        $("#error_msg").html("Please enter mandatory (*) field(s).").css("display","block")
      }
      else {
      $.ajax({
        url: '/admin/ajax/add-coupon',
        data: {
          'coupon_name': coupon_name,
          'coupon_code':coupon_code,
          'coupon_value':coupon_value,
          'coupon_description':coupon_description,
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
    })


    $('#couponId').click(function(){
        $('#CouponBox').css("display","block")
        })

    $('.close').click(function(){
        $('#CouponBox').css("display", "none")
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


function confirmAndActivate(coupon_id) {
    if (confirm('Are you sure you want to deactivate this coupon?')) {
        coupon_act(coupon_id, 1);
    }
}

function confirmAndDeactivate(coupon_id) {
    if (confirm('Are you sure you want to Activate this coupon?')) {
        coupon_act(coupon_id, 0);
    }
}

function coupon_act(id, val) {
    $.ajax({
        url: '/admin/ajax/update-coupon',
        data: {
            'coupon_id': id,
            'is_active': val,
        },
        dataType: 'json',
        method: 'post',
        success: function (data) {
            console.log(data);
            if (data.resp === 'redirect') {
                window.location.href = "";
            }
        }
    });
}