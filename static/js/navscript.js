$(function(){

  $('input[name="About"]').click(function(){
    alert('Hello...!');
  });

  window.onkeyup = function(e) {
   var key = e.keyCode ? e.keyCode : e.which;

   if (key == 39) {
       document.getElementById('ad_btn').click();
   }else if (key == 37) {
       document.getElementById('notad_btn').click();
   }
 }
  
});