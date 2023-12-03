function fnameValidation(inputTxt){
    
    var regx = /^[a-zA-Z\s/,()'-]+$/;
    var textField = document.getElementById("name");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 3){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";
                    
            }else{
                textField.textContent = '**Only characters are allowed"';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = '**your product name must include more chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = '**Please enter your product name';
        textField.style.color = "red";
    }
}

function addressValidation(inputTxt){
    
    var regx = /^[a-zA-Z\s,()'-]*$/;
    var textField = document.getElementById("addr");
        
    if(inputTxt.value != '' ){
    
        if(inputTxt.value.length >= 2){
        
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "green";
                    
            }else{
                textField.textContent = 'only characters allowded';
                textField.style.color = "red";
            }  
        }else{
            textField.textContent = 'your input must me more chracters';
            textField.style.color = "red";
        }   
    }else{
        textField.textContent = 'your input is empty';
        textField.style.color = "red";
    }
}


function pincodeValidation(inputTxt){
    
    var regx = /^[0-9]$/;
    var textField = document.getElementById("pin");
        
    if(inputTxt.value != '' ){
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";
                    
            }else{
                textField.textContent = '**enter a valid price';
                textField.style.color = "red";
            }  
    }else{
        textField.textContent = '**Please enter the pincode';
        textField.style.color = "red";
    }
}

function pinValidation(inputTxt){
    
    var regx = /^[0-9]$/;
    var textField = document.getElementById("pin");
        
    if(inputTxt.value != '' ){
            if(inputTxt.value.match(regx)){
                textField.textContent = '';
                textField.style.color = "";
                    
            }else{
                textField.textContent = '**enter a valid price';
                textField.style.color = "red";
            }  
    }else{
        textField.textContent = '**Please enter the pincode';
        textField.style.color = "red";
    }
}

function fileValidation(inputTxt) {
    var fileInput =
        document.getElementById('file');
     
    var filePath = fileInput.value;
    // Allowing file type
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
    if (!inputTxt.value.match(allowedExtensions)) {
        alert('Invalid file type');
        fileInput.value = '';
        return false;
        }
            
}