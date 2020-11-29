(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);


// // script to show post status as Published or Private, if status === 1 => published, else => private
// const tableDesc = document.getElementsByClassName("activity-post-status");
//
// window.onload = () =>{
// 	if(tableDesc.innerText === "1"){
// 	tableDesc.innerText = "published";
// 	}else{
// 		tableDesc.innerText = "private";
// 	}
// }

