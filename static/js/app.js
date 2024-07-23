var referred_appointment;
var referred_patient;
$(document).ready(function(){


// JavaScript code
function setError($input, errorMsg) {
  $input.removeClass('success');
  $input.addClass('error');
  $input.next('.error-msg').html(errorMsg).show();
  $input.show();
}

function setSuccess($input) {
  $input.removeClass('error');
  $input.addClass('success');
  $input.next('.error-msg').html('').hide();
}


$('#first_name, #last_name, #email_address, #mobile_number, #password, #confirm_password, #user_type').on('input', function () {
  setSuccess($(this)); // Call setSuccess to hide the error message
})

$("#send_otp, #register").click(function () {

  var email_address = $('#email_address').val();
  var first_name = $('#first_name').val();
  var last_name = $('#last_name').val();
  var mobile_number = $('#mobile_number').val();
  var password = $('#password').val();
  var confirm_password = $('#confirm_password').val();
  var user_type = $('#user_type').val();
  var referral_code = $('#referral_code').val();

  // Regular expression to validate email address
  //var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  //r'[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-zA-Z]+'
  var emailRegex =  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:.[a-zA-Z0-9-]+)*$/;

  var firstnameRegex = /^[A-Za-z][A-Za-z0-9_]{2,29}$/;

  var lastnameRegex = /^[A-Za-z][A-Za-z0-9_]{0,29}$/;

  var mobileRegex = /^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$/;

  var passwordRegex =  /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;

 // Function to validate email address
  function validateEmail(email) {
    if (!emailRegex.test(email)) {
      setError($('#email_address'), 'Please enter a valid email address');
      return false;
    } else {
      setSuccess($('#email_address'));
      return true;
    }
  }

  function validateMobileNumber(mobile_number) {
  if (!mobileRegex.test(mobile_number)) {
    setError($('#mobile_number'), 'Please enter a valid mobile number');
    return false;
  } else {
    setSuccess($('#mobile_number'));
    return true;
  }
}

function validateFirstName(first_name) {
  if (!firstnameRegex.test(first_name)) {
    setError($('#first_name'), 'Please enter valid name. It should start with an alphabet and no space in front. All other characters can be alphabets, numbers or an underscore. It should be alreast 3 letters');
    return false;
  } else {
    setSuccess($('#first_name'));
    return true;
  }
}

function validateLastName(last_name) {
  if (!lastnameRegex.test(last_name)) {
    setError($('#last_name'), 'Please enter valid name. It should start with an alphabet and no space in front. All other characters can be alphabets, numbers or an underscore.');
    return false;
  } else {
    setSuccess($('#last_name'));
    return true;
  }
}

function validatePassword(password) {
  if (!passwordRegex.test(password)) {
    setError($('#password'), 'Please enter valid password. It should be minimum 8 characters with at least one uppercase character, one lowercase character and one special character and one digit ');
    return false;
  } else {
    setSuccess($('#password'));
    return true;
  }
}


  var missingRequiredFields = [];

   if (email_address === "") {
      missingRequiredFields.push("Email Address");
      setError($('#email_address'), 'Email address is required');
    } else {
      if (!validateEmail(email_address)) {
        setError($('#email_address'), 'Please enter a valid email address');
        return; // Return immediately if email is invalid
      } else {
        setSuccess($('#email_address'));
      }
    }

    if (first_name === "") {
      missingRequiredFields.push("First Name");
      setError($('#first_name'), 'First name is required');
    } else {
      if (!validateFirstName(first_name)) {
        setError($('#first_name'), 'Please enter valid name. It should start with an alphabet and no space in front. All other characters can be alphabets, numbers or an underscore. It should be alreast 3 letters');
        return;
      } else {
        setSuccess($('#first_name'));
      }
    }

  if (last_name === "") {
    missingRequiredFields.push("Last Name");
    setError($('#last_name'), 'Last name is required');
  } else {
     if (!validateLastName(last_name)) {
        setError($('#last_name'), 'Please enter valid name. It should start with an alphabet and no space in front. All other characters can be alphabets, numbers or an underscore.');
        return;
      } else {
        setSuccess($('#last_name'));
      }
    }

    if (mobile_number === "") {
      missingRequiredFields.push("Mobile Number");
      setError($('#mobile_number'), 'Mobile number is required');
    } else {
      if (!validateMobileNumber(mobile_number)) {
        setError($('#mobile_number'), 'Please enter a valid  mobile number');
        return; // Return immediately if mobile number is invalid
      } else {
        setSuccess($('#mobile_number'));
      }
    }

  if (password === "") {
    missingRequiredFields.push("Password");
    setError($('#password'), 'Password is required');
  } else {
      if (!validatePassword(password)) {
        setError($('#password'), 'Please enter valid password. It should be minimum 8 characters with at least one uppercase character, one lowercase character and one special character and one digit ');
        return; // Return immediately if mobile number is invalid
      } else {
        setSuccess($('#password'));
      }
    }

  if (confirm_password === "") {
    missingRequiredFields.push("Confirm Password");
    setError($('#confirm_password'), 'Confirm password is required');
  } else {
    if (password !== confirm_password) {
      setError($('#confirm_password'), 'Confirm Password do not match with Password');
      return;
    } else {
      setSuccess($('#confirm_password'));
    }
  }

  if (user_type === "") {
    missingRequiredFields.push("User Type");
    setError($('#user_type'), 'User type is required');
  } else {
    setSuccess($('#user_type'));
  }

  if (missingRequiredFields.length > 0) {
    $('#error_msg').html("Please enter the required fields: " + missingRequiredFields.join(', ')).show();
    // Show input boxes that have errors
    $('.error').each(function () {
      $(this).show();
    });
    return;
  } else {
    $('#error_msg').html("").hide();
  }

  this_id = $(this).attr('id');

  if (this_id === 'send_otp') {
    action = 'send_otp';
    otp = '';
  }

  if (this_id === 'register') {
    action = 'validate_otp';
    otp = $('#received_otp').val();
  }

  $.ajax({
    url: '/ajax/registeruser',
    data: {
      'first_name': first_name,
      'last_name': last_name,
      'email_address': email_address,
      'mobile_number': mobile_number,
      'user_type': user_type,
      'action': action,
      'password': password,
      'referral_code': referral_code
    },
    dataType: 'json',
    method: 'post',
    success: function (data) {
      console.log(data);
         if(data.status=="failed")
            {
            setError($('#email_address'), 'User already exist');
            }

      if (data.resp === 'redirect') {
        window.location.href = "/profile/edit";
      }
    },
    error: function (error) {
      console.error('AJAX Error', error);
    }
  });
})


    $("#send_login_otp, #login").click(function () {
      var email = $('#signin_email').val();
      var password = $('#password').val();
      if(email=="" || password=="")
      {
      $('#error_msg').html("Please enter username and password").show()
      }
      else
      {
        $('#error_msg').html("").hide()


      //var user_type = $('#user_type').val();
      var user_type = $("input[name='user_type']:checked").val()

      $.ajax({
        url: '/ajax/loginuser',
        data: {
          'email': email,
          'password':password,
          'user_type': user_type,

        },
        dataType: 'json',
        method: 'post',
        success: function (data) {
          console.log(data)

            //$('#signin_received_otp').val(data.resp);
            if(data.status=="failed")
            {
            $('#error_msg').html("Kindly enter the correct username and password").show()
            }
            else
            {
            $('#error_msg').html("").hide()

            }
            if(data.resp == 'redirect')
            {
                window.location.href = "/profile";
            }

        }
      });
      }
      })

    $("#update_personal_info, #update_profile_info, #update_address_info, #update_professional_info, #update_subscription_info, #update_availability_info").click(function(){
        this_id = $(this).attr('id')
        data = {}

        if (this_id=='update_personal_info')
        {
            first_name = $("#first_name").val()
            last_name = $("#last_name").val()
            gender = $("input[name='gender']:checked").val()
            email =$("#email").val()
            dob = $("#dob").val()
            about_me = $("#about_me").val()
            total_experience = $("#total_experience").val()

            var firstnameRegex = /^[A-Za-z][A-Za-z0-9_]{2,29}$/;



            data = {
                  "first_name": first_name,
                  "last_name":last_name,
                  "gender": gender,
                  "dob": dob,
                  "email":email,
                  "action" : this_id,

                }

                $("#success_message").show().fadeOut(5000);
                }



        if (this_id=='update_profile_info')
        {
            about_me = $("#about_me").val()
            total_experience = $("#total_experience").val()
            consultation_fees = $("#consultation_fees").val()
            data = {
                  "about_me": about_me,
                  "total_experience":total_experience,
                  "consultation_fees":consultation_fees,
                  "action" : this_id,
                }
        }

        if (this_id=='update_professional_info')
        {
//            qualification =$("#qualification").val()
//            specialization = $("#specialization").val()
            specializationArr = new Array()
            $("input[name='specialization']:checked").each(function(){
                 specializationArr.push(this.value)
            })

            qualificationArr = new Array()
            $("input[name='qualification']:checked").each(function(){
                qualificationArr.push(this.value)
            })

            data = {
                  "qualification" : qualificationArr.join(","),
                  "specialization": specializationArr.join(","),
                  "action" : this_id,
                }

        }

        if (this_id=='update_address_info')
        {
            title = $("#title").val()
            address_1 = $("#address_1").val()
            address_2 = $("#address_2").val()
            city = $("#city").val()
            district = $("#district").val()
            state = $("#state").val()
            pincode = $("#pincode").val()
            data = {
                  "title": title,
                  "address_1": address_1,
                  "address_2":address_2,
                  "city": city,
                  "district": district,
                  "state": state,
                  "pincode": pincode,
                  "action" : this_id,

                }

        }

        if (this_id=='update_subscription_info')
        {
            subscription = $("input[name='subscription']:checked").val()

            data = {
                  "subscription_id": subscription,
                  "action" : this_id,

                }

        }

          if (this_id=='update_availability_info')
        {
            var day = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"];
            var dict = {};
            $.each(day, function(key, value) {
            day_start_time = $("#"+value+"_start_time").val()
            day_end_time = $("#"+value+"_end_time").val()
            day_duration = $("#"+value+"_duration").val()
            if( $("#"+value+"_available").is(':checked') ){
                day_available=1
             }
             else{
                day_available=0
             }
            day_val = day_start_time+","+day_end_time+","+day_duration+","+day_available

            dict[value] = day_val
        });
         data = {
                  "avail": JSON.stringify(dict),
                  "action" : this_id,

                }

        }

       $.ajax({
        url: '/ajax/updateuser',
        data: data,
        dataType: 'json',
        method: 'post',
        success: function (data) {
          console.log(data)
        }
      });
    })

     // $(".time-block").click(function(){
    $('#result_form').on('click', '.time-block', function(e) {
        apt_data = $(this).attr('id')

        console.log(apt_data)
        $("#user_apt_data").val(apt_data)
        $("#result_form").submit()

    })

    $(document).on('click', '#coupon_apply', function(e) {
        coupon = $("#coupon").val()
        $("#error-msg").html('').css('display', 'none')
        $.ajax({
            url: '/ajax/apply-coupon',
            data: {'coupon': coupon},
            dataType: 'json',
            method: 'post',
            success: function (data) {
              //console.log(data)
                if(data.status == 'success') {
                    $("#disc_amount").html("-"+data.result.discount_amount)
                    $("#discounted_amount").html(data.result.discounted_amount)
                    $("#gst_amount").html(data.result.gst_amount)
                    $("#total_amount").html(data.result.final_amount)
                    $("#payment_amount").val(data.result.final_amount)
                    options['amount'] = data.result.final_amount
                }
                else{
                    $("#error-msg").html(data.result).css('display', 'block')
                 }


            }
        });
    })

//    $("#proceed_to_payment").on('click','#proceed_to_payment_form')
//    $('#proceed_to_payment').click(function(){
//        $.ajax({
//        url: "/ajax/appointmentSave",
//        method: "POST",
//        data: {
//            patient_id: $('#user_id').val(),
//            appointment_datetime:$('#apt_date_time').val(),
//            csrfmiddlewaretoken:$( "input[name='csrfmiddlewaretoken']" ).val()
//        },
//         headers: {
//              "X-CSRFToken": "{{csrf_token}}"
//            },
//
//        success: function (data) {
//              console.log(data)
//            $("#proceed_to_payment_form").submit();
//            }
//
//     })
//
//    })

    $('#search_doctor').click(function(){
        $("#search_form").submit();
    })


    $(".confirm-apt,.modify-apt, .cancel-apt").click(function(){
        this_id = $(this).attr('id')
        this_list = this_id.split("_")
        action = this_list[0]
        appointment_id = this_list[1]
        data = {}

        data["action"] = action
        data["appointment_id"] = appointment_id

        if(action == "modify-apt"){
            data["modified_datetime"] = $("#cal-apt-datetime_"+appointment_id).val()
        }

        console.log(data)
         $.ajax({
         url: '/ajax/update-appointment',
         data: data,
         dataType: 'json',
         method: 'post',

        success: function (data) {
             window.location=""
          console.log(data)
        }
      });

    })


    $(" .modify-apt-btn,  .close-apt").click(function(){
        this_id = $(this).attr('id')
        this_list = this_id.split("_")
        action = this_list[0]
        appointment_id = this_list[1]

        if(action=="modify-apt-btn"){

            $("#modify-apt-div_"+appointment_id).css("display", "block")
        }

        if(action=="close-apt"){
            $("#modify-apt-div_"+appointment_id).css("display", "none")
        }

 })

    $(".refer-doctor").click(function(){
    this_id = $(this).attr('id')
    this_list = this_id.split("_")
    action = this_list[0]
    referred_appointment = this_list[1]
    referred_patient = this_list[2]
    $("#ReferDrScreen").css("display", "flex")
})

    $(".close").click(function(){
    $("#ReferDrScreen").css("display", "none")
    referred_appointment = ''
    referred_patient = ''
})

    $("#search_doctor_to_refer").click(function(){
        search_city = $("#search_city").val()
        search_keyword = $("#search_keyword").val()
        data = {}
        data['search_city'] = search_city
        data['search_keyword'] = search_keyword

         $.ajax({
         url: '/ajax/search-dr',
         data: data,
         dataType: 'json',
         method: 'post',

        success: function (data) {
          console.log(data)
            $("#dr_search_result").html(data.search_data)
        }
      });
    })

    //    $('.myr__button-primary').css('background', '#232c60')
    $('.radio-inline').click(function(){
        $('#error_msg').html("").hide();

    })


})

    function show_appointment_slots(id){
        $('.myr__slot-calender').html('').hide()
        //alert(id)
        $.ajax({
            url: '/ajax/show_appointment_slots',
            data: {'user_id': id},
            dataType: 'json',
            method: 'post',
            success: function (data) {
              //console.log(data)
              $('#slot-calander-'+id).html(data).show()
            }
        });
    }

    function dr_refer_patient(referred_dr_id){
        data["action"] = 'dr-refer'
        data["appointment_id"] = referred_appointment
        data["patient_id"] = referred_patient
        data["referred_to_dr_id"] = referred_dr_id
        data["refer_notes"] = $('#refer_notes_'+referred_dr_id).val()
        console.log(data)
        $.ajax({
             url: '/ajax/update-appointment',
             data: data,
             dataType: 'json',
             method: 'post',

            success: function (data) {
                 window.location=""
                //console.log(data)
            }
        });
    }

    var user_type;
    var email;


    $("#reset_password_button").click(function () {
        var new_password = $("#new_password").val();
        var confirm_password = $("#confirm_password").val()
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val(); // Get the CSRF token
        $(".error").text("").css("display", 'none');
        $(".success_msg").text("").css("display", 'none');

        if (new_password != '' && confirm_password != '') {
            if (new_password == confirm_password) {
                $.ajax({
                    url: '/reset-password',
                    data: {
                            'csrfToken': csrfToken,
                            'new_password': new_password,
                            'confirm_password': confirm_password,
                        },
                    dataType: 'json',
                    method: 'post',
                    success: function (data) {
                        if (data.success) {
                            $('#new-password-form').remove()
                            $(".success_msg").text("Password has been reset successfully!").css("display", 'block');
                        } else {
                            $(".error").text("Error resetting password.").css("display", 'block');
                        }
                    }
                });
                }
                else {
                $(".error").text("New and confirm password are not same.").css("display", 'block');
                }
            }
            else {
                $(".error").text("Please enter mandatory(*) fields").css("display", 'block');
            }
    });




    $("#forgot_password").click(function () {
        var user_type = $("input[name='user_type']:checked").val();
        var user_email = $('#signin_email').val();
        $(".error").text("").css("display", 'none');
        if(user_type!='' &&  user_email!='')
        {
            $.ajax({
                url: '/forgot-password',
                data: {
                    'user_type': user_type,
                    'user_email': user_email,
                    'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
                },
                dataType: 'json',
                method: 'post',
                success: function (data) {
                if (data.success) {
                    $("#signin_email").attr('disabled', 'disabled')
                    $("input[name='user_type']").attr('disabled', 'disabled')

                    $("#otp_box").show();
                    $("#forgot_password").hide();
                    $("#validate_otp").show();
                } else {
                    $(".error").text("This email is not registered with us!").css("display", 'block');
                }
               }

            });

        }
        else {
            $(".error").text("Please enter mandatory fields!").css("display", 'block');
        }
     })

    $("#validate_otp").click(function () {
            $(".error").text("").css("display", 'none');
            var entered_otp = $("#entered_otp").val();
            $.ajax({
                    url: '/validate-otp',
                    data: {'entered_otp': entered_otp},
                    dataType: 'json',
                    method: 'post',
                    success: function (data) {
            if (data.success) {
                window.location.href = '/reset-password';
            } else {
                $(".error").text("Entered OTP is wrong, please try again!").css("display", 'block');
            }
        }
    });
});