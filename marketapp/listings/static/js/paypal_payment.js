paypal.Buttons({
  createOrder: function(data, actions) {
    // This function sets up the details of the transaction, including the amount and line item details.
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: JSON.parse(document.getElementById('payment_amount').textContent)
        },
        payee: {
          email_address: JSON.parse(document.getElementById('user_receiving').textContent)
        }
      }]
    });
  },
  onApprove: function(data, actions) {
    // This function captures the funds from the transaction.
    return actions.order.capture().then(function(details) {
      // This function shows a transaction success message to your buyer.
      alert('Transaction Details: ' + details.payer.name.given_name);

      receipt_id = JSON.parse(document.getElementById('receipt_id').textContent)
      var data = {'details': details}
      $.post(URL, data, function(response){
          if(response === 'success'){
            alert('All went well :)');
            location.href = "/listings/receipts/" + receipt_id + "/payment-made"
          } else {
            alert('Something went wrong...');
          }
      });
      //receipt_id = JSON.parse(document.getElementById('receipt_id').textContent)
      //location.href = "/listings/receipts/" + receipt_id + "/payment-made"
    });
  }
}).render(document.getElementById('payment-container'));
