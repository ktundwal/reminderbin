/**
 * Based on Wookmark's endless scroll.
 */
$(window).ready(function () {
    var apiURL = '/api/patient/?format=json&offset='
    var page = 0;
    var handler = null;
    var isLoading = false;
    
    /**
     * When scrolled all the way to the bottom, add more tiles.
     */
    function onScroll(event) {
      if(!isLoading) {
          var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
          if(closeToBottom) loadData();
      }
    };
    
    function applyLayout() {
      $('#pins').imagesLoaded(function() {
          // Clear our previous layout handler.
          if(handler) handler.wookmarkClear();
          
          // Create a new layout handler.
          handler = $('#pins .pin');
          handler.wookmark({
              autoResize: true,
              offset: 3,
              itemWidth: 242
          });
      });
    };
    
    /**
     * Loads data from the API.
     */
    function loadData() {
        isLoading = true;
        $('#loader').show();
        
        $.ajax({
            url: apiURL+(page*20),
            success: onLoadData
        });
    };
    
    /**
     * Receives data from the API, creates HTML for images and updates the layout
     */
    function onLoadData(data) {
        data = data.objects;
        isLoading = false;
        $('#loader').hide();
        
        page++;
        
        var html = '';
        var i=0, length=data.length, image;
        for(; i<length; i++) {
          image = data[i];
          html += '<div class="pin">';
              html += '<a class="fancybox" rel="pins" href="'+image.image+'">';
                  html += '<img src="'+image.thumbnail+'" width="200" >';
              html += '</a>';
              html += '<p>'+image.description+'</p>';
          html += '</div>';
        }
        
        $('#pins').append(html);
        
        applyLayout();
    };
  
    $(document).ready(new function() {
        $(document).bind('scroll', onScroll);
        loadData();

        $('#user_time').html(getCurrentTime() + " " + getTimezoneName());
    });

    /**
     * On clicking an image show fancybox original.
     */
    $('.fancybox').fancybox({
        openEffect: 'none',
        closeEffect: 'none'
    });
});

function getCurrentTime() {

    var currentDate = new Date()
    var day = currentDate.getDate()
    var month = currentDate.getMonth() + 1
    var year = currentDate.getFullYear()
    current_date = month + "/" + day + "/" + year

    var currentTime = new Date()
    var hours = currentTime.getHours()
    var minutes = currentTime.getMinutes()

    var suffix = "AM";
    if (hours >= 12) {
        suffix = "PM";
        hours = hours - 12;
    }
    if (hours == 0) {
        hours = 12;
    }

    if (minutes < 10)
        minutes = "0" + minutes

    current_time =  hours + ":" + minutes + " " + suffix

    return current_date + " " + current_time
}

function getTimezoneName() {
    tmSummer = new Date(Date.UTC(2005, 6, 30, 0, 0, 0, 0));
    so = -1 * tmSummer.getTimezoneOffset();
    tmWinter = new Date(Date.UTC(2005, 12, 30, 0, 0, 0, 0));
    wo = -1 * tmWinter.getTimezoneOffset();

    if (-660 == so && -660 == wo) return 'Pacific/Midway';
    if (-600 == so && -600 == wo) return 'Pacific/Tahiti';
    if (-570 == so && -570 == wo) return 'Pacific/Marquesas';
    if (-540 == so && -600 == wo) return 'America/Adak';
    if (-540 == so && -540 == wo) return 'Pacific/Gambier';
    if (-480 == so && -540 == wo) return 'US/Alaska';
    if (-480 == so && -480 == wo) return 'Pacific/Pitcairn';
    if (-420 == so && -480 == wo) return 'US/Pacific';
    if (-420 == so && -420 == wo) return 'US/Arizona';
    if (-360 == so && -420 == wo) return 'US/Mountain';
    if (-360 == so && -360 == wo) return 'America/Guatemala';
    if (-360 == so && -300 == wo) return 'Pacific/Easter';
    if (-300 == so && -360 == wo) return 'US/Central';
    if (-300 == so && -300 == wo) return 'America/Bogota';
    if (-240 == so && -300 == wo) return 'US/Eastern';
    if (-240 == so && -240 == wo) return 'America/Caracas';
    if (-240 == so && -180 == wo) return 'America/Santiago';
    if (-180 == so && -240 == wo) return 'Canada/Atlantic';
    if (-180 == so && -180 == wo) return 'America/Montevideo';
    if (-180 == so && -120 == wo) return 'America/Sao_Paulo';
    if (-150 == so && -210 == wo) return 'America/St_Johns';
    if (-120 == so && -180 == wo) return 'America/Godthab';
    if (-120 == so && -120 == wo) return 'America/Noronha';
    if (-60 == so && -60 == wo) return 'Atlantic/Cape_Verde';
    if (0 == so && -60 == wo) return 'Atlantic/Azores';
    if (0 == so && 0 == wo) return 'Africa/Casablanca';
    if (60 == so && 0 == wo) return 'Europe/London';
    if (60 == so && 60 == wo) return 'Africa/Algiers';
    if (60 == so && 120 == wo) return 'Africa/Windhoek';
    if (120 == so && 60 == wo) return 'Europe/Amsterdam';
    if (120 == so && 120 == wo) return 'Africa/Harare';
    if (180 == so && 120 == wo) return 'Europe/Athens';
    if (180 == so && 180 == wo) return 'Africa/Nairobi';
    if (240 == so && 180 == wo) return 'Europe/Moscow';
    if (240 == so && 240 == wo) return 'Asia/Dubai';
    if (270 == so && 210 == wo) return 'Asia/Tehran';
    if (270 == so && 270 == wo) return 'Asia/Kabul';
    if (300 == so && 240 == wo) return 'Asia/Baku';
    if (300 == so && 300 == wo) return 'Asia/Karachi';
    if (330 == so && 330 == wo) return 'Asia/Calcutta';
    if (345 == so && 345 == wo) return 'Asia/Katmandu';
    if (360 == so && 300 == wo) return 'Asia/Yekaterinburg';
    if (360 == so && 360 == wo) return 'Asia/Colombo';
    if (390 == so && 390 == wo) return 'Asia/Rangoon';
    if (420 == so && 360 == wo) return 'Asia/Almaty';
    if (420 == so && 420 == wo) return 'Asia/Bangkok';
    if (480 == so && 420 == wo) return 'Asia/Krasnoyarsk';
    if (480 == so && 480 == wo) return 'Australia/Perth';
    if (540 == so && 480 == wo) return 'Asia/Irkutsk';
    if (540 == so && 540 == wo) return 'Asia/Tokyo';
    if (570 == so && 570 == wo) return 'Australia/Darwin';
    if (570 == so && 630 == wo) return 'Australia/Adelaide';
    if (600 == so && 540 == wo) return 'Asia/Yakutsk';
    if (600 == so && 600 == wo) return 'Australia/Brisbane';
    if (600 == so && 660 == wo) return 'Australia/Sydney';
    if (630 == so && 660 == wo) return 'Australia/Lord_Howe';
    if (660 == so && 600 == wo) return 'Asia/Vladivostok';
    if (660 == so && 660 == wo) return 'Pacific/Guadalcanal';
    if (690 == so && 690 == wo) return 'Pacific/Norfolk';
    if (720 == so && 660 == wo) return 'Asia/Magadan';
    if (720 == so && 720 == wo) return 'Pacific/Fiji';
    if (720 == so && 780 == wo) return 'Pacific/Auckland';
    if (765 == so && 825 == wo) return 'Pacific/Chatham';
    if (780 == so && 780 == wo) return 'Pacific/Enderbury'
    if (840 == so && 840 == wo) return 'Pacific/Kiritimati';
    return 'US/Pacific';
}

function addTZToForm() {
    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "user_tz");
    input.setAttribute("value", getTimezoneName());

    //append to form element that you want .
    $("#new_reminder_form_id").appendChild(input);
}