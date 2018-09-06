/* OneFile/index.js */

//<!--

function setTitle() {
var a = " $title ";
var b = " Server CMS";
var c = " $sys{script_name}";
 var t = new Date();
 s = t.getSeconds();
 if (s == 10) {
  document.title = a;}
 else if (s == 20) {
 document.title = b;}
 else if (s == 30) {
 document.title = c;}
 else if (s == 40) {
 document.title = a;}
 else if (s == 50) {
 document.title = b;}
 else if (s == 00) {
 document.title = c;}
 setTimeout("setTitle()", 1000);
 }
 
//-->