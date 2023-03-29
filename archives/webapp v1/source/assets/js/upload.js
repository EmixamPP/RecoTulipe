function upload(){
   
    var input = document.getElementById("mypic");
    var file = input.files[0];            
    var form = new FormData(),
        xhr = new XMLHttpRequest();
    var reader = new FileReader();

    form.append('image', file);
    xhr.withCredentials = false;
    xhr.open('post', 'http://127.0.0.1:8001', true);
    //xhr.setRequestHeader("Content-Type","text/html")
    xhr.onreadystatechange = function(){
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("res").innerHTML = xhr.responseText;
      }
      else{
          document.getElementById("res").innerHTML = "Not connected to server";
      }
    }
    /*
    var im =form.get("image"),
    console.log(im.getAsText());
    */
    xhr.send(form);
    
    draw(file);
  }


function draw(file){
    var reader = new FileReader();
    reader.onload = function (e) {
        
      var dataURL = e.target.result,
          c = document.getElementById('canvas'), // see Example 4
          ctx = c.getContext('2d'),
          img = new Image();

      ctx.canvas.clientWidth = 
      ctx.canvas.clientHeight = 
      img.onload = function() {
        c.width = ctx.canvas.clientWidth;
        c.height = ctx.canvas.clientHeight;
        ctx.drawImage(img, 0, 0, 300, 300);
      };
      img.src = dataURL;
    };
    reader.readAsDataURL(file);
}
