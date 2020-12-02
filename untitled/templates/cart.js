function addtocart(){
var addcartbuttons = document.getElementsByClassName('btn-success')
for(var i =0; i<addcartbuttons.length; i++){
	var button = addcartbuttons[i];
	document.getElementsByClassName('btn-success').innerHTML=button;
	}
}