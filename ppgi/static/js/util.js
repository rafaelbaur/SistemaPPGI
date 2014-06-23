function printResultTablePopUp(titulo){
	var htmlTableResults = $("#result_list").clone();
	var popup = window.open();
	popup.document.write("<html><head><link rel='stylesheet' type='text/css' href='/static/admin/css/base.css' /></head><body><h1>" +titulo+ "</h1</body></html>");
	htmlTableResults.appendTo(popup.document.body);
	popup.document.close();
	popup.print();
}
