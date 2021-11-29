$(document).ready(function () {
   $('#user-icon').click(function (e) { 
       e.preventDefault();
       $('#myModal').appendTo("body").modal('show');
   });
});
