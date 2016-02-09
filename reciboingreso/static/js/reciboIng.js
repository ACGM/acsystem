(function(_){
	angular.module('cooperativa.reciboIng',['ngAnimate'])



	.filter('EstatusRecibo', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('P', 'Posteada')
                .replace('I', 'Nula')
                .replace('R', 'Registrada');
        	return input;
     	 }
  		})

		.factory('reciboIngServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/reciboIngreso';
			var urlNomina ='/reciboNom';

			function getRecibos(){
				var deferred = $q.defer();

				$http.get(apiUrl+"?format=json")
					.success(function (data) {
						deferred.resolve(data);
					})
					.error(function (err){
						deferred.resolve(err);
					})

					return deferred.promise;
			};

			function getReciboBySocio(socio){
				var deferred = $q.defer();

				getRecibos.then(function (data){
					var registro = data.filter(function (reg){
						return reg.socio == socio;
					});

					deferred.resolve(registro);
				});

				return deferred.promise;
			};

			function setRecibo(recibo){
				var deferred = $q.defer();

				$http.post(apiUrl, JSON.stringify({'recibo': recibo}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (err){
						 deferred.resolve(err);
					});

				return deferred.promise;
			};

			function socios() {
                var deferred = $q.defer();

                $http.get('/api/socio/?format=json')
                  .success(function (data) {
                    deferred.resolve(data.filter( function(socio) {
                      return socio.estatus == "E" || socio.estatus == "S";

                    }));
                  });
                  return deferred.promise;
            };

            function postRecibo(recibo, fecha){
            	var deferred = $q.defer();
            	$http.post('/postearRecibo', JSON.stringify({'recibo': recibo,'fecha': fecha}))
            		.success(function (data){
            			deferred.resolve(data);
            		})
            		.error(function (err){
            			deferred.resolve(err);
            		});

            	return deferred.promise;
            };

            function getReciboNomAll(){
            	var deferred = $q.defer();

            	$http.get(urlNomina+"?format=json")
            		.success(function (data){
            			deferred.resolve(data);
            		})
            		.error(function (err){
            			deferred.resolve(err);
            		});

            		return deferred.promise;
            };

            function postReciboNom(recibo){
            	var deferred = $q.defer();

            	$http.post(urlNomina, JSON.stringify({'reciboN': recibo}))
            		.success(function (data){
            			deferred.resolve(data);
            		})
            		.error(function (err){
            			deferred.resolve(err);
            		});

            		return deferred.promise;
            };

			return {
				getRecibos : getRecibos,
				getReciboBySocio : getReciboBySocio,
				setRecibo : setRecibo,
				socios : socios,
				postRecibo : postRecibo,
				getReciboNomAll : getReciboNomAll,
				postReciboNom	: postReciboNom
			};
		}])
		
	  	.controller('reciboIngCtrl', ['$scope', '$filter', '$window', '$rootScope', 'reciboIngServices','$timeout', '$window', 'MaestraPrestamoService',
								function ($scope, $filter, $window , $rootScope, reciboIngServices, $timeout, $window, MaestraPrestamoService){                        	
			
				$scope.reciboData = {}
				$scope.reciboLista = [];
				$scope.prestamosS = [];
				$scope.reciboLst = true;
				$scope.reciboCr = false;
				$scope.tableSocio = false;
				$scope.tablePrest =  false;
				$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			    //Traer todos los socios a javascript
		        reciboIngServices.socios().then(function (data) {
		          $scope.todosLosSocios = data;
		        });

		        $scope.objectSorteable = function(a, b){
					if(a.id < b.id){
						return 1;
					}

					if(a.id > b.id){
						return -1;
					}

					return 0;
				}

		        $scope.cancelarReg = function($event){ 
		        	$scope.reciboData = {}
					$scope.reciboLista = [];
					$scope.prestamosS = [];
					$scope.socioNombre = null;
					$scope.montoInicial = null;
					$scope.reciboLst = true;
					$scope.reciboCr = false;
					$scope.tableSocio = false;
					$scope.tablePrest =  false;
					$scope.totalPrest = null;
					$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
					$scope.getList();
		        }

				$scope.getList = function(){

					$scope.reciboLista =[];
					$scope.reciboData = {};

					reciboIngServices.getRecibos().then(function (data) {
						$scope.reciboLista = data.sort($scope.objectSorteable);
						console.log(data);
					
					});
				}

				$scope.nwRecibo = function($event){
					$scope.reciboLst = false;
					$scope.reciboCr = true;

					// $scope.reciboData.montoAhorro
				}

				$scope.editRecibo = function($event, id){
					$event.preventDefault();

					$scope.reciboLista.filter(function (data){
						var reg = data.filter(function (registro){
							return registro.id == id;
						});
						$scope.reciboData.id = reg[0].id;
						$scope.reciboData.fecha = reg[0].fecha;
						$scope.reciboData.socio =reg[0].socioId;
						$scope.socioNombre = reg[0].socio;
						$scope.reciboData.montoAhorro = reg[0].montoAhorro;
						$scope.reciboData.NoPrestamo = reg[0].prestamo.codigo;
						$scope.montoInicial = reg[0].prestamo.montoInicial;
						$scope.reciboIngreso.montoPrestamo =reg[0].montoPrestamo;

					});
				}

				$scope.getSocio = function($event) {
		            $event.preventDefault();

		            $scope.tableSocio = true;
		            $scope.tablePrest = false;

		            if($scope.socioNombre !== undefined) {
		                $scope.socios = $scope.todosLosSocios.filter(function (registro) {
		                  return $filter('lowercase')(registro.codigo.toString()
		                                      .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
		                });

		                if($scope.socios.length == 0){
		                	$scope.socios = $scope.todosLosSocios.filter(function (registro) {
		                  		return $filter('lowercase')(registro.nombreCompleto
		                  			.substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
		                });
		                }

		                if($scope.socios.length > 0){
		                  $scope.tableSocio = true;
		                  $scope.socioNoExiste = '';
		                } else {
		                  $scope.tableSocio = false;
		                  $scope.socioNoExiste = 'No existe el socio';
		                }

		            } else {
		                $scope.socios = $scope.todosLosSocios;
		                $scope.socioCodigo = '';
		            }
		          };

		        $scope.selPrest = function($event, x){
		       		$event.preventDefault();

		       		$scope.reciboData.NoPrestamo=x.noPrestamo;
		            $scope.montoInicial = x.balance;
		            $scope.totalPrest = x.balance;

		            $scope.tablePrest = false;
		          };

		       	$scope.selSocio = function($event, s) {
		       		$event.preventDefault();

		       		$scope.reciboData.socio=s.codigo;
		            $scope.socioNombre = s.nombreCompleto;

		            $scope.tableSocio = false;
		          };

		        $scope.getPrestamosSocio = function($event){
		        	$scope.tableSocio = false;
					$scope.tablePrest =  true;
		        	
		        	MaestraPrestamoService.PrestamosbySocio($scope.reciboData.socio).then(function (data){
		        		$scope.prestamosS = data.filter(function (reg){
		        			console.log(reg);
			        			return reg.estatus != "S"
			        		});
			        	});
			        	}

		        $rootScope.mostrarError = function(error) {
				      $scope.errorMsg = error;
				      $scope.errorShow = true;
				      $timeout(function(){$scope.errorShow = false;}, 3000);   
			    	};

			    $scope.postRecibo = function($event,id){
			    	$event.preventDefault();

			    	var fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
			    	var RegFecha = $scope.fecha.split('/');
	          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
	          		fecha = FechaFormat;
			    	reciboIngServices.postRecibo(id, fecha).then(function (data){
			    		if(data == "Ok"){
			    			$scope.getList();
			    			alert("Recibo #"+id+" ha sido Posteado")
			    			$scope.reciboLst = true;
							$scope.reciboCr = false;
							$scope.tableSocio = false;
							$scope.tablePrest =  false;
			    			
			    		}else{
			    			$rootScope.mostrarError("Ha Ocurrido un error al intentar postear el recibo #"+id)
			    		}
			    	});
			    };

		        $scope.setRecibo = function($event){
		        	$event.preventDefault();
		        	
	          		try{

		  	        	var RegFecha = $scope.fecha.split('/');
	          			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
	          			$scope.reciboData.fecha = FechaFormat;

	          			if ($scope.reciboData.id == undefined){
	          				$scope.reciboData.id = null;
	          			};

	          			if ($scope.reciboData.estatus == undefined){
	          				$scope.reciboData.estatus = "R";
	          			};

	          			if ($scope.reciboData.NoPrestamo == undefined){
	          				$scope.reciboData.NoPrestamo = null;
	          			}else{
	          				if($scope.reciboData.montoPrestamo != undefined){
	          					if($scope.reciboData.montoPrestamo > $scope.totalPrest){
	          						throw "Monto a pagar es mayor a la deuda del prestamo";
	          					}
	          				}else{
	          					throw "Monto Prestamo no puede estar vacio";
	          				}
	          			};

	          			if($scope.reciboData.montoAhorro == undefined){
	          				$scope.reciboData.montoAhorro = null;
	          			};


	          			reciboIngServices.setRecibo($scope.reciboData).then(function (data){
	          				$scope.cancelarReg($event);
	          			 	$scope.getList();
	          			});
	          			 
	          		}	
	          		catch(ex){
	          			$rootScope.mostrarError(ex.message);
	          		}
		        	};

}])
.controller('ReciboNomCtrl', ['$scope','$filter','$window','reciboIngServices', function ($scope, $filter, $window, reciboIngServices) {
	$scope.reciboList = [];
	$scope.reciboData = {}
	$scope.fechaI = null;
	$scope.fechaF = null;
	$scope.fecha = null;

	$scope.vistaRecibo = true;
	$scope.formRecibo =false;

	$scope.getDate = function(){
		var date = new Date();
		var fechaInicio = new Date(date.getFullYear(), date.getMonth(), 1);
		var fechaFin = new Date(date.getFullYear(), date.getMonth() + 1, 0);
		$scope.fechaI = $filter('date')(fechaInicio, 'dd/MM/yyyy');
		$scope.fechaF = $filter('date')(fechaFin, 'dd/MM/yyyy');

		$scope.getRecibosNomina();
	}

	$scope.getReciboFecha = function($event){
		$event.preventDefault()

		$scope.reciboList = $scope.reciboList.filter(function (data){
			return data.fecha <= $scope.fechaI && data.fecha >= $scope.fechaF;
		});

	};

	$scope.nwRegistro = function($event){
		$event.preventDefault();

		$scope.vistaRecibo = false;
		$scope.formRecibo =true;

	}

	$scope.getRecibosNomina = function(){

		reciboIngServices.getReciboNomAll().then(function (data){
			$scope.reciboList = data;
			console.log(data);
		})
	}

	$scope.cancelarReg = function($event){
		$event.preventDefault();

		$scope.reciboList = [];
		$scope.reciboCuentas = [];
		$scope.reciboData = {}
		$scope.fechaI = null;
		$scope.fechaF = null;
		$scope.fecha = null;

		$scope.vistaRecibo = true;
		$scope.formRecibo =false;

		$scope.getDate();
	}

	$scope.setReciboNom = function($event){
		$event.preventDefault();
		if($scope.reciboData.id === undefined){
			$scope.reciboData.id = null;
		}
		var RegFecha = $scope.fecha.split('/');
		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
		$scope.reciboData.fecha = FechaFormat;

	}

	$scope.editRecibo = function($event, data){
		$event.preventDefault();

		$scope.reciboData = data;
		var RegFecha =  data.fecha.split('-');
		var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
		$scope.fecha = FechaFormat;

		$scope.desgloseCuentas = data.cuentas;
      	$scope.vistaRecibo = false;
		$scope.formRecibo =true;
	}


	// Mostrar/Ocultar posteo Contabilidad
		    $scope.toggleInfo = function() {
		       $scope.showPostear = !$scope.showPostear;
		    }

			 $scope.cuentasBuscar = function($event) {

		        if(!isNaN($scope.Postear.cuentaBuscar)) {
		          //Para cuando es el numero de la cuenta
		          $scope.cuentasContables = $scope.todasLasCuentas.filter(function (item) {
		            return item.codigo.toString().substring(0, $scope.Postear.cuentaBuscar.length) == $scope.Postear.cuentaBuscar;
		          });
		        } else {
		          //Para cuando es la descripcion de la cuenta
		          $scope.cuentasContables = $scope.todasLasCuentas.filter(function (item) {
		            return item.descripcion.toLowerCase().substring(0, $scope.Postear.cuentaBuscar.length) == $scope.Postear.cuentaBuscar.toLowerCase();
		          });
		        }
		        $scope.tableCuenta = true;
		      }

		     // Agregar una cuenta
		      $scope.addCuentaContable = function($event, cuenta) {
		        $event.preventDefault();
		        var desgloseCuenta = new Object();
				
				console.log($scope.desgloseCuentas)
				console.log(cuenta)
		        
		        desgloseCuenta.cuenta = cuenta.codigo;
		        desgloseCuenta.descripcion = cuenta.descripcion;
		        desgloseCuenta.ref = null;//$scope.desgloseCuentas[$scope.desgloseCuentas.length-1].ref;
		        desgloseCuenta.debito = 0;
		        desgloseCuenta.credito = 0;

		        $scope.desgloseCuentas.push(desgloseCuenta);
		        $scope.tableCuenta = false;
		      }

		      $scope.quitarCC = function(desgloseC) {
		        if($scope.desgloseCuentas.length == 2) {
		          $scope.mostrarError("No puede eliminar todas las cuentas. Verifique la configuración de Documentos-Cuentas.")
		        } else {
		          $scope.desgloseCuentas = _.without($scope.desgloseCuentas, _.findWhere($scope.desgloseCuentas, {cuenta: desgloseC.cuenta}));
		          $scope.totalDebitoCredito();
		        }
		      }

		      //Sumarizar el total de CREDITO y total de DEBITO antes de postear (llevar a contabilidad).
		      $scope.totalDebitoCredito = function() {
		        $scope.totalDebito = 0.00;
		        $scope.totalCredito = 0.00;

		        $scope.desgloseCuentas.forEach(function (documento) {
		          console.log(documento)

		          if(documento.debito.length > 0) {
		            $scope.totalDebito += parseFloat(documento.debito);
		          }

		          if(documento.credito.length > 0) {
		            $scope.totalCredito += parseFloat(documento.credito);
		          }
		        });
		      }

		  //Este metodo escribe en el diario general los registros correspondientes al desglose de cuenta
	      //para este modulo de Conciliacion.
	      $scope.postearContabilidad = function() {

	        try {
	        
	          //Validar que el CREDITO cuadre con el DEBITO
	          if($scope.totalDebito != $scope.totalCredito && $scope.totalDebito > 0) {
	            throw "El valor TOTAL del DEBITO es distinto al valor TOTAL del CREDITO.";
	          }

	          $scope.posteoG = true;
	          $scope.desgloseCuentas.forEach(function (item) {
	          	var cuenta = { 
	          		fecha :Date.now(),
	          		cuenta: item.cuenta,
	          		ref: item.ref,
	          		debito: item.debito,
	          		credito: item.credito
	          	};
	         	$scope.reciboCuentas.push(cuenta);
	          });

	          $scope.reciboData.cuentas = $scope.reciboCuentas;

	         reciboIngServices.postReciboNom($scope.reciboData).then(function (data){
			
					if(data == "Ok"){
						notie.alert(1,"Recibo Guardado",1.2);
					}
					
					else{
						notie.alert(3,"Ocurrio un error al intentar guardar el recibo", 3.2);
						console.log(data);
					}

				});
			 $scope.getRecibosNomina();
	          notie.alert(1,'Los registros fueron posteados con exito!',3.2);

	        } catch (e) {
	          notie.alert(3,e,3.2);
	        }
	      } //Linea FIN de posteo Contabilidad.

			

}]); 
})(_);