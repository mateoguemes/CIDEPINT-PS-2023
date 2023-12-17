// Función para validar el formulario de inicio de sesión
function validateLoginForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    
    if (email === "" || password === "") {
        alert("Por favor, complete todos los campos.");
        return false;
    }
    
    return true; // Envía el formulario si todas las validaciones son exitosas.
}

// Función para validar el formulario de registro
function validateRegisterForm() {
    var name = document.getElementById("name").value;
    var lastName = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    
    if (name === "" || lastName === "" || email === "") {
        alert("Por favor, complete todos los campos.");
        return false;
    }

    // Verificar que el nombre y el apellido no contengan números ni símbolos
    var namePattern = /^[A-Za-z\s]+$/; // Solo letras y espacios permitidos
    if (!namePattern.test(name) || !namePattern.test(lastName)) {
        alert("El nombre y el apellido no deben contener números ni símbolos.");
        return false;
    }

    
    return true; // Envía el formulario si todas las validaciones son exitosas.
}

function validatePassword(password) {
    // Requisitos para la contraseña
    const minLength = 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumberOrSymbol = /[0-9!@#\$%\^&\*]/.test(password); // Puedes personalizar los símbolos permitidos aquí

    return (
        password.length >= minLength &&
        hasUppercase &&
        hasLowercase &&
        hasNumberOrSymbol
    );
}

function passwordValidation() {
    const passwordInput = document.getElementById('password');
    const passwordMessage = document.getElementById('password-message');

    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value;
        const isValid = validatePassword(password);

        if (isValid) {
            passwordMessage.textContent = 'Contraseña válida';
            passwordMessage.style.color = 'green';
        } else {
            passwordMessage.textContent = 'La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número o símbolo.';
            passwordMessage.style.color = 'red';
        }
    });
}


//VALIDACIONES DE FORMULARIO DE ACTUALIZAR INSTITUCION
function validateForm() {
    var name = document.getElementById("name").value;
    var information = document.getElementById("information").value;
    var address = document.getElementById("address").value;
    var location = document.getElementById("location").value;
    var website = document.getElementById("website").value;
    var opening_hours = document.getElementById("opening_hours").value;
    var contact = document.getElementById("contact").value;
    var nameRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
    var keywords = document.getElementById("keywords").value;
    var patron = /^[\p{L}\s]+$/u; // Se admiten letras y espacios, incluyendo letras con acentos
    if (!name.match(nameRegex)) {
        alert("El nombre sólo puede contener letras y no debe estar en blanco.");
        return false;
    }

    if (information.trim() === "" || address.trim() === "" || location.trim() === "" || 
        website.trim() === "" || opening_hours.trim() === "" || contact.trim() === "") {
        alert("Por favor, no deje campos en blanco.");
        return false;
    }
    if (!patron.test(keywords)) {
        alert("Las palabras claves deben separarse por espacios en blanco. Solo se admiten letras y espacios");
        return false;
    }

    var words = keywords.split(' ');
    var word_count = words.length;
    var index = 0;
    var correct_length = true;
    
    while (correct_length && index < word_count) {
        if (words[index].length > 50) {
            correct_length = false;
        }
        index++;
    }
    
    if (!correct_length) {
        alert("Una palabra de búsqueda es demasiado larga. La longitud máxima son 50 letras");
    }
    
    return correct_length;
}
