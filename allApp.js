/**/
!function(){var a=angular.module("cooperativa",["cooperativa.menu","cooperativa.nomina","cooperativa.facturacion","cooperativa.inventario"]);a.config(function(a,b){a.startSymbol("[[").endSymbol("]]"),b.defaults.xsrfCookieName="csrftoken",b.defaults.xsrfHeaderName="X-CSRFToken"}),a.filter("numberFixedLen",function(){return function(a,b){var c=parseInt(a,10);if(b=parseInt(b,10),isNaN(c)||isNaN(b))return a;for(c=""+c;c.length<b;)c="0"+c;return c}}),a.directive("datepicker",function(){return{restrict:"A",require:"ngModel",link:function(a,b,c,d){$(function(){b.datepicker({dateFormat:"dd/mm/yy",onSelect:function(b){a.$apply(function(){d.$setViewValue(b)})}})})}}})}(),function(){angular.module("cooperativa.menu",[]).controller("MenuController",["$scope",function(a){a.menu="0",a.setMenu=function(b){a.menu=b,$("#menu"+a.menu+" a").addClass("OpcionSeleccionada"),$sib=$("#menu"+a.menu).siblings(),$sib.find(" a").removeClass("OpcionSeleccionada")},a.ShowSubMenuP=function(){a.SubMPrestamo=!a.SubMPrestamo}}])}();