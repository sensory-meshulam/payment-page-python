console.log("blabla")

const apiUrl = 'http://localhost:5000';
let resultStatus; //boolean
let resultData;


const data =  {
    sum: 1,
    paymentsNum: 1,
    description: "The destination of the payment",
  }
  
const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Request-Method": "POST",
      "Access-Control-Request-Headers": "Content-Type",
    },
    body: JSON.stringify(data)
}

async function getPaymentLink (){
   const response = await fetch(`/api/payment/getPaymentLink`, options);
   //response in format {isSuccess: boolean, message: string (payment-link or error-message)}
   const data = await response.json();
   console.log(data.message);
   window.open(data.message);
}
