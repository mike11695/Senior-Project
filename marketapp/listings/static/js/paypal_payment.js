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
      receipt_id = JSON.parse(document.getElementById('receipt_id').textContent)
      amount = JSON.parse(document.getElementById('payment_amount').textContent)
      var data = {'receipt_id': receipt_id, 'order_id': details.id,
        'status': details.status,
        'amount': amount,
      }
      $.ajax({
        type: "POST",
        url: '/listings/receipts/create-payment-receipt',
        data: data,
        success: function(response) {
          if (response === 'success') {
            alert("Transaction Completed by: " + details.payer.name.given_name
              + "\nReceipt has been updated!");
            location.href = "/listings/receipts/" + receipt_id + "/payment-made"
          } else {
            alert("Transaction Completed by: " + details.payer.name.given_name
              + "\nReceipt could not be updated though.");
            location.href = "/listings/receipts/" + receipt_id + "/payment-made"
          }
        }
      })
    });
  }
}).render(document.getElementById('payment-container'));
