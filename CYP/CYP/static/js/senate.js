// var main = function() {
//   $('.circle').hover(function() {
//     $('.picture_name').css("display", "block");
//     }, function(){
//       $('.picture_name').css("display", "none");
//     });
// };
//
// $(document).ready(main);


$(document).ready(function() {

    // if the function argument is given to overlay,
    // it is assumed to be the onBeforeLoad event listener
    $("a[rel]").overlay({

        top: '0px',
        left: '0px',
        fixed: false,
        position: 'inherit',


        onBeforeLoad: function() {

            // grab wrapper element inside content
            var wrap = this.getOverlay().find(".stuff");

            // load the page specified in the trigger
            wrap.load(this.getTrigger().attr("href"));
        }

    });
});
//
// $(document).ready( function() {
//   onBeforeLoad: function() {
//     $("a[rel]").on("click", function() {
//         $(".article_overlay").load(this.getTrigger().attr("href"));
//     });
// });
