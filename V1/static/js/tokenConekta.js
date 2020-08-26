Conekta.setPublicKey('Llave publica');
// key_DiDc6UeyagcBPqyxrgxkPDg Llave para tokenizar tarjetas en el buscador del cliente.


var conektaSuccessResponseHandler = function(token) {
    // pirmeros 4 digitos
    // número de telefono correo
    var $form = $("#card-form");
    //Inserta el token_id en la forma para que se envíe al servidor
    $("#conektaTokenId").val(token.id);
    // $form.get(0).submit(); //Hace submit
    pagoConekta();
};
var conektaErrorResponseHandler = function(response) {
    var $form = $("#card-form");
    alert(response.message_to_purchaser);
    //$form.find("button").prop("disabled", false);
};


//Genera el token después de dar click en submit
$(function() {
    $("#card-form").submit(function(event) {
        event.preventDefault();
        var $form = $(this);
        // Previene hacer submit más de una vez
        // $form.find("button").prop("disabled", true);
        Conekta.Token.create($form, conektaSuccessResponseHandler, conektaErrorResponseHandler);
        return false;
    });
});

function pagoConekta() {

    //value de cvc y card vacias
    // primeros 4 drigitos
    $("#card").prop("value", "");
    $("#cvc").prop("value", "");

    let params = $("#card-form").serialize();
    let url = "pagoConekta.php";

    // $.post(url, params, function(data) {
    //     if (data == "1") {
    //         alert("Te enviamos un correo de confirmación de tu pago.");
    //         limpiarForm();
    //     } else {
    //         alert(data);
    //     }
    // });
}

// primeros 4 drigitos
// regresar correo a CCC