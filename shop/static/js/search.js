//$(document).ready(function(){
//	$("#search-box").keyup(function(){
//		$.ajax({
//		type: "POST",
//		url: "search",
//		data:'keyword='+$(this).val(),
//		beforeSend: function(){
//			$("#search-box").css("background","#FFF url(LoaderIcon.gif) no-repeat 165px");
//		},
//		success: function(data){
//			$("#suggesstion-box").show();
//			$("#suggesstion-box").html(data);
//			$("#search-box").css("background","#FFF");
//		}
//		});
//	});
//});
////To select country name
//function selectCountry(val) {
//$("#search-box").val(val);
//$("#suggesstion-box").hide();
//}
//
//$('#search').autocomplete({
//
//    source: function(request, response){
//        $.ajax({
//
//            type: 'GET',
//			cache   : false,
//            dataType: 'json',
//            serviceUrl : '/search/',
//            data:{
//                //maxRows: 12, // �������� ������ 12 �����������
//                query: $(this).val() // ��������� �����
//
//            },
//
//            //success: function(data){
//            //    response($.map(data, function(item){
//            //        return {
//            //            plink: item.plink, // ������ �� �������� ������
//            //            label: item.title_ru // ������������ ������
//            //        }
//            //    }));
//            //}
//        });
//    },
//    //select: function( event, ui ) {
//    //    // �� ������ - ������� �� �������� ������
//    //    // �� ������ ������ ����� ���������� �� �����
//    //    location.href = ui.item.plink;
//    //    return false;
//    //}
//    //minLength: 3 // �������� ����� � ���� ��������
//});
$(function() {
  $("#autocomplete").autocomplete({
     source: function(request, response) {
        $.get('/search/', { query: request.term },
			function(data) {
           response($.map(JSON.parse(data.split('\n')), function (value, key) {

           return {
                    label: value['title'],
                    value: key,
                    url: value['url'],
                    price: value['price']
                };

      }));
        }) },
      select: function( event, ui ) {
        // �� ������ - ������� �� �������� ������
        // �� ������ ������ ����� ���������� �� �����
          console.log(event)
          console.log(ui.item.url)
        location.href = ui.item.url
        return false;
    },
    minLength: 2,
  });
});