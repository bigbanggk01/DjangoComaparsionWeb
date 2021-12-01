$(document).ready(function () {
   $('#login-button').mouseup(function (e) { 
        e.preventDefault();
        $(this).parent().find(".login-field").toggle();
        $(".login-modal").toggle();
   });
});
