$("#loginScreen").hide();
$("#signupScreen").hide();
let togglaBtn = function () {
    let $eleUl = $(".myr__nav-left").find("ul");
    $(document).on('click', '.myr__nav-humburger', function () {
        $(this).toggleClass("change");
        $eleUl.toggleClass("mobile-menu");
    });
}
let stickyHeader = function(){
    let header = document.getElementById("myr__header");
    let stickyHeader = header.offsetTop;
    console.log(stickyHeader , window.pageYOffset);
    if (window.pageYOffset > stickyHeader) {
        $(header).addClass("myr__sticky");
      } else {
        $(header).removeClass("myr__sticky");
      }
}
let searchModal = function () {
    $(".myr_search").on("click", function () {
        $(".myr__search-modal").show();
    });
    $(".myr__search-close").on("click", function () {
        $(".myr__search-modal").hide();
    });
}
let cardSlider = new Swiper(".myr__card-wrapper", {

    slidesPerView: 4,
    spaceBetween: 30,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    resistanceRatio: 0,
    breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 24,
            // resistanceRatio: 0.85
        },
        480: {
            slidesPerView: 2,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        },
        640: {
            slidesPerView: 4,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        },
        1024: {
            slidesPerView: 5,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        }
    },
    keyboard: {
        enabled: true,
    }
});
let physioSlider = new Swiper(".myr__physio-wrap", {

    slidesPerView: 1,
    spaceBetween: 30,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    resistanceRatio: 0,
    breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 24,
            // resistanceRatio: 0.85
        },
        480: {
            slidesPerView: 1,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        },
        640: {
            slidesPerView: 1,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        }
    },
    keyboard: {
        enabled: true,
    }
});

let testimonialSlider = new Swiper(".myr__testimonials-slider", {

    slidesPerView: 1,
    spaceBetween: 30,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    resistanceRatio: 0,
    breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 24,
            // resistanceRatio: 0.85
        },
        480: {
            slidesPerView: 1,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        },
        640: {
            slidesPerView: 1,
            spaceBetween: 28,
            //resistanceRatio: 0.85
        }
    },
    keyboard: {
        enabled: true,
    }
});

let startupOverlay = function () {
    $(".myr__startup-cta").on("click", function () {
        $(".myr__overlay").show();
        $("body").css("overflow", "hidden");
    });
    $(".myr__close").on("click", function () {
        $(".myr__overlay").hide();
        $("body").css("overflow", "inherit");
    });
}
let loginOverlay = function () {
    $("#loginOverlay, .myr__btn1").on("click", function () {
        $("#loginScreen").show();
    });
    $(".close").on("click", function () {
        $("#loginScreen").hide();
        $("#signupScreen").hide();
    });

    $(".myr__signup-link a").on("click", function () {
        $("#loginScreen").hide();
        $("#signupScreen").show();
    });
    $(".myr__signin-link a").on("click", function () {
        $("#loginScreen").show();
        $("#signupScreen").hide();
    })
}
let rangeSilder = function () {
    if ($(".myr__filter-search").length > 0) {
        let slider = document.getElementById("myRange");
        let output = document.getElementById("rangeValue");
        output.innerHTML = slider.value;
        slider.oninput = function () {
            output.innerHTML = this.value;
        }
    }
}
let toggleFilterSearch = function () {
    $(".myr__filter-wrap").hide();
    $(".myr__filter-by").on("click", function () {

        $(".myr__filter-wrap").slideToggle();
    })
}
let timeSlotCalender = function () {
   $(".myr__slot-calender").hide();
let btnValue = $(".myr__book-appointment").text();
    $(".myr__book-appointment").on("click", function () {
        $(this).parents('.myr__parent').next(".myr__slot-calender").slideToggle();  
    });
}

let slotCalendar = function () {
    let tabwrapWidth = $(".tabs-wrapper").outerWidth();
    let totalWidth = 0;
    $("ul li").each(function () {
        totalWidth += $(this).outerWidth();
    });
    if (totalWidth > tabwrapWidth) {
        
        $(".scroller-btn").removeClass("inactive");
    } else {
        $(".scroller-btn").addClass("inactive");
    }
    if ($("#scroller").scrollLeft() == 0) {
        $(".scroller-btn.left").addClass("inactive");
    } else {
        $(".scroller-btn.left").removeClass("inactive");
    }
    let liWidth = $("#scroller li").outerWidth();
    let liCount = $("#scroller li").length;
    let scrollWidth = liWidth * liCount;
    $(document).on("click", ".right", function (event) {
        $(".nav-tabs").animate({ scrollLeft: "+=260px" }, 300);
    });

    $(document).on("click", ".left", function (event){
        $(".nav-tabs").animate({ scrollLeft: "-=260px" }, 300);
    });
    scrollerHide();

    function scrollerHide() {
        let scrollLeftPrev = 0;
        $("#scroller").scroll(function () {
            let $elem = $("#scroller");
            let newScrollLeft = $elem.scrollLeft(),
                width = $elem.outerWidth(),
                scrollWidth = $elem.get(0).scrollWidth;
            if (scrollWidth - newScrollLeft == width) {
                $(".right.scroller-btn").addClass("inactive");
            } else {
                $(".right.scroller-btn").removeClass("inactive");
            }
            if (newScrollLeft === 0) {
                $(".left.scroller-btn").addClass("inactive");
            } else {
                $(".left.scroller-btn").removeClass("inactive");
            }
            scrollLeftPrev = newScrollLeft;
        });
    }
}
$(function () {
    $( window ).scroll(function() {
        stickyHeader();
    });
    togglaBtn();
    searchModal();
    startupOverlay();
    loginOverlay();
    rangeSilder();
    toggleFilterSearch();
    timeSlotCalender();
    slotCalendar();
});