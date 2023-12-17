function validateKeywords() {
    var keywords = document.getElementById("keywords").value;
    var patron = /^[\p{L}\s]+$/u; // Se admiten letras y espacios

    if (!patron.test(keywords)) {
        alert("Las palabras claves deben separarse por espacios en blanco. Solo se admiten letras y espacios");
        return false; // Prevent form submission
    } else {
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
        
        if(!correct_length){
            alert("Una palabra de búsqueda es demasiado larga. La longitud máxima son 50 letras");
        }
        return correct_length;
    }
}
