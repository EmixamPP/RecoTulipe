const input = document.getElementById("input");
const previewConainer = document.getElementById("view");
const previewImage = previewConainer.querySelector(".input-view")

input.addEventListener("change", function(){
    var image = this.files[0];
    if (image) {
        document.getElementById("res").innerHTML = "Prédiction en cours...";
        
        // mode  
        var complet = document.getElementById("customRadioInline1").checked;
        var mode = complet ? "complet" : "reduit"
        
        // envoie de l'image au serveur
        const form = new FormData(),
              xhr = new XMLHttpRequest();
        form.append('type', "byte");
        form.append('mode', mode);
        form.append('image', image);
        xhr.withCredentials = false;
        xhr.open('post', 'https://www.dirksen.fr:8080', true);
        xhr.onreadystatechange = function(){
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("res").innerHTML = xhr.responseText;
            } else {
              document.getElementById("res").innerHTML = "Le serveur ne répond pas";
            }
        }
        xhr.send(form);

        // affichage de l'image
        const reader = new FileReader();
        reader.addEventListener("load", function(){
            previewImage.setAttribute("src", this.result);
        });
        reader.readAsDataURL(image);

    } else { // aucune image n'a été chargé
        previewImage.setAttribute("src", "");
    }
});