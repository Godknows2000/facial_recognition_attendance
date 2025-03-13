$(document).ready(function () {
  $(".sidebar-item").click(function (e) {
    e.preventDefault();
    $(".sidebar-item").removeClass("active");
    $(this).addClass("active");
  });
});
