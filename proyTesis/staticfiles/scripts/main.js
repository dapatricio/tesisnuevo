$(document).ready(main);
 
var contador = 1;
 
function main(){
	$('.menu_bar').click(function(){
		// $('nav').toggle(); 
 
		if(contador == 1){
			$('nav').animate({
				left: '0'
			});
			contador = 0;
		} else {
			contador = 1;
			$('nav').animate({
				left: '-100%'
			});
		}
 
	});
 
};

$(document).ready(function(){ 
   $('#area1').on('click',function(e){
      $('.cierre').hide();
      $('#rta_area1').toggle('slow');
   });
   $('#area2').on('click',function(e){
      $('.cierre').hide();
      $('#rta_area2').toggle('slow');
   });
   $('#area3').on('click',function(e){
      $('.cierre').hide();
      $('#rta_area3').toggle('slow');
   });
   $('#area4').on('click',function(e){
      $('.cierre').hide();
      $('#rta_area4').toggle('slow');
   });
   $('#area5').on('click',function(e){
      $('.cierre').hide();
      $('#rta_area5').toggle('slow');
   });
   $('#ar1_comp1').on('click',function(e){
      $('.cierre').hide();
      $('#rta_comp1').toggle('slow');
   });
   $('#ar1_comp2').on('click',function(e){
      $('.cierre').hide();
      $('#rta_comp2').toggle('slow');
   });
   $('#ar1_comp3').on('click',function(e){
      $('.cierre').hide();
      $('#rta_comp3').toggle('slow');
   });
}); 
   
$(document).ready(function(){		
	$(".area1").click(function(){
		$(".competencia1").slideToggle();
	});
	$(".area2").click(function(){
		$(".competencia2").slideToggle();
	});
	$(".area3").click(function(){
		$(".competencia3").slideToggle();
	});
	$(".area4").click(function(){
		$(".competencia4").slideToggle();
	});
	$(".area5").click(function(){
		$(".competencia5").slideToggle();
	});
}); 

$("#area1").animate({ scrollBo: $('#rta_area1')[0].scrollHeight}, 1000);