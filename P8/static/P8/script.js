$(document).ready(function(){

    $(".button_save").click(function(){
        $(this).addClass("disabled");
        $(this).html("<strong> déjà sauvegardé </strong>");

    });

    $("#icône_accueil").mouseover(function(){
        $("#icône_accueil").addClass("mr-3");
    });

    $("#icône_accueil").mouseleave(function(){
        $("#icône_accueil").removeClass("mr-3");
    });

//    Responsive
var width = document.body.clientWidth;
console.log(width)

if (width < 500) {
console.log("plus petit que 1000");
$("#img_icône_accueil").css("width", "50%");
$("#ns").removeClass("w-25");
$("#ns").addClass("w-50");
$("#food_details").removeClass("w-50");
$("#food_details").addClass("w-100");

$(".btn").removeClass("w-25");
$(".btn").addClass("w-50");

}

else {
console.log("plus grand que 1000");
}

//Méthode ajax
var addAjax = $(".add-ajax");

addAjax.click(function(event){
$("#ns").addClass("w-50");
        event.preventDefault();
            console.log("Form is not sending");
            thisForm = $(this)
            var actionEndpoint = thisForm.attr("action");
            var httpMethod = thisForm.attr("method");
            var formData = thisForm.serialize();


            $.ajax({
                url: actionEndpoint,
                method: httpMethod,
                data: formData,

                    success:function(data){
                        console.log("success")
                        console.log(data)
                    },
                    error:function(errorData){
                        console.log("error")
                        console.log(errorData)
                    }
                })
        })
});




