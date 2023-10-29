let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
}
$(document).ready(function (){
    // Add to cart
    $('.add_to_cart').on('click', function (e){
        e.preventDefault();
        // Remove the alert("o") line

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response){
                console.log(response)
                if(response.status === 'login_required'){
                    swal(response.message,'', 'info').then(function (){
                        window.location = '/login';
                    })
                }else if(response.status === 'Failed'){
                    swal(response.message,'', 'error')
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    //Subtotal, tax and grand_total

                    appyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        });
    });

    // Place cart item quantity on load
    $('.item_qty').each(function (){
        var the_id =  $(this).attr('id');
        var qty =  $(this).attr('data-qty');
        $('#'+the_id).html(qty);
    });

    // Decrease cart
    $('.decrease_cart').on('click', function (e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response){
                console.log(response)
                if(response.status === 'login_required'){
                    swal(response.message,'', 'info').then(function (){
                        window.location = '/login';
                    })
                }else if(response.status === 'Failed'){
                    swal(response.message,'', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);


                    appyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )


                    if(window.location.pathname === '/cart/'){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }

                }
            }
        });
    });

    // Delete Cart Item
    $('.delete_cart').on('click', function (e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response){
                console.log(response)
                if(response.status === 'Failed'){
                    swal(response.message,'', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,response.message, 'success')


                    appyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )

                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }
            }
        });
    });
    // delete the  cart element if the quantity is zero
    function removeCartItem(cartItemQty, cart_id){
            if (cartItemQty <=0){
            //remove the element
            document.getElementById("cart-item-"+cart_id).remove()
            }
    }

    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = 'block';
        }
    }


    //apply cart amounts

    function appyCartAmount(subtotal, tax, grand_total){
        if (window.location.pathname==='/cart/'){
            $('#subtotal').html(subtotal)
            $('#tx').html(tax)
            $('#total').html(grand_total)
        }
    }
});