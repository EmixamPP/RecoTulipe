const choice = document.querySelectorAll(".select_img");
const collapse = document.getElementById("modal_button")

choice.forEach(function(elem) {
    elem.addEventListener("click", function() {
        collapse.click();
        var image = this.src;
        document.getElementById("res").innerHTML = "Prédiction en cours...";

        // mode 
        var complet = document.getElementById("customRadioInline1").checked;
        var mode = complet ? "complet" : "reduit"

        // envoie de l'image au serveur
        const form = new FormData(),
              xhr = new XMLHttpRequest();
        form.append('type', "local");
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
        previewImage.setAttribute("src", image);
    });
});