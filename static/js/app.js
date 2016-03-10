$(".spinner").hide();

$("form").submit(function() {
	$(".spinner").show();
	$(this).hide()
});