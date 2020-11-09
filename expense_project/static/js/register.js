  
//submit validation
var sub_button=document.querySelector("#submit")
 
 
//email validation code
const emailfield=document.querySelector('#email');
const e_feedback=document.querySelector(".email-invalid")
emailfield.addEventListener('keyup',(e) =>{
    var email=e.target.value;
    e_feedback.style.display="none";
    emailfield.classList.remove('is-invalid')
    if(email.length > 0){

        sub_button.disabled=false;
        fetch('/authentication/validate-email',{
            body:JSON.stringify({ email :email}),
            method:"POST",
        }).then( (res) =>
           res.json())
        .then( (data) =>{
            if(data.email_error)
            {
                
                e_feedback.style.display="block";
                e_feedback.innerHTML=`<h6>${data.email_error}</h6>`
                emailfield.classList.add('is-invalid')
                sub_button.disabled=true;
                
            }
        }) 
  
    }
    
})

//username validation code
var userfield=document.querySelector('#username');
var feedback=document.querySelector(".user-invalid")
userfield.addEventListener('keyup',(e) =>{
    var uname=e.target.value;
    feedback.style.display="none";
    userfield.classList.remove('is-invalid')
    if(uname.length > 0){

        sub_button.disabled=false;
        fetch('/authentication/validate-username',{
            body:JSON.stringify({ username :uname}),
            method:"POST",
        }).then( (res) =>
           res.json())
        .then( (data) =>{
            if(data.username_error)
            {
                
                feedback.style.display="block";
                feedback.innerHTML=`<h6>${data.username_error}</h6>`
                userfield.classList.add('is-invalid')
                sub_button.disabled=true;
            }
        })  
     
  
    }
    
})
//password validation code
var passfield=document.querySelector('#password');
var pass_feedback=document.querySelector(".password-invalid")
passfield.addEventListener('keyup',(e) =>{
    var passwd=e.target.value;
    pass_feedback.style.display="none";
    passfield.classList.remove('is-invalid')
    if(passwd.length > 0){

        sub_button.disabled=false;
        fetch('/authentication/validate-password',{
            body:JSON.stringify({ password :passwd}),
            method:"POST",
        }).then( (res) =>
           res.json())
        .then( (data) =>{
            if(data.password_error)
            {
                
                pass_feedback.style.display="block";
                pass_feedback.innerHTML=`<h6>${data.password_error}</h6>`
                passfield.classList.add('is-invalid')
                sub_button.disabled=true;
            }
        })
      
  
    }
    
})
 
 
 
 
 