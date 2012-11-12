function filterList() {
	$("td:contains('N/A')").parent().hide();
	$("td:contains('Idea')").parent().hide();
}
