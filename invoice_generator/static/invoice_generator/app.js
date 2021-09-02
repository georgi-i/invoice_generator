
$(document).ready(function(){

    const quantity_field = $("input.quantity[type=number]");
    const unit_price = $("input.unit_price[type=number]");
    const value = $("input.value[type=number]");

    function calcValue(x, y) {
        if (x.val().length != 0 && y.val().length != 0) {
            
            return x.val() * y.val()
        } 
      } 

    quantity_field.keyup(function() {        
        value.val(calcValue(quantity_field, unit_price))            
    });
    unit_price.keyup(function() {        
        value.val(calcValue(quantity_field, unit_price))            
    });
});


