jQuery(document).ready(function ($) {
    $('.view').click(changeView);
    function changeView() {
        $.ajax({
            type: "GET",
            url: "/products/change_view/",
            data:{
                'view':$(this).attr('data-v'),
            },
            dataType: "html",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
            }
       });
    }
});

jQuery(document).ready(function ($) {
    $('.sort').click(sortView);
    function sortView() {
        $.ajax({
            type: "GET",
            url: "/products/sort_view/",
            data:{
                'sort_view':$(this).attr('data-v'),
            },
            dataType: "html",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
            }
       });
    }
});


 $(document).ready(function () {
     $(".cart-spinner").hide();
var lnk = $("a.in-cart");
$(lnk).click(function(event) {


    var spinner = $(this);

function hideshopcart() {spinner.find('i').filter('.fa-shopping-cart').hide(0);}
function showcartspinner() {spinner.find('i').filter('.cart-spinner').removeClass('hide').show(0);}
function hidecartspinner() {spinner.find('i').filter('.cart-spinner').addClass('hide').hide(0);}
function showshopcart() {spinner.find('i').filter('.fa-shopping-cart').show(0);}

    setTimeout(hideshopcart, 50)
    setTimeout(showcartspinner, 50)
    setTimeout(hidecartspinner, 1000)
    setTimeout(showshopcart, 1000)

$.get($(this).attr('href')).done(

    function( json ) {

    $("#items_in_cart").text(json.items_in_cart)
//function shopcart() {spinner.find('i').filter('.cart-spinner').addClass('hide').hide(0);}
//function shopcart() {spinner.find('i').filter('.fa-shopping-cart').show(0);}
            setTimeout(hideshopcart, 50)
    setTimeout(showcartspinner, 50)
    setTimeout(hidecartspinner, 800)
    setTimeout(showshopcart, 800)
});

return false
});

    });

$(document).ready(function () {
    $('.navbar-brand').hover(function() {
  var back = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","Darkorange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"];
  var rand = back[Math.floor(Math.random() * back.length)];
  $('.navbar-brand').css('color',rand);
})
    });

if ($(document).height() <= $(window).height())
  $("footer.footer").addClass("navbar-fixed-bottom");