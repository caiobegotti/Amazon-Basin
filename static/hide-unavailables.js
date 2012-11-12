$("#unavailable").click(function() {
    alert("Test...");
    $("td:contains('N/A')").parent().hide();
});
