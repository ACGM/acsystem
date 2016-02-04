(function(_){
	angular.module('cooperativa.chequeConc', ['ngAnimate'])

	.factory('ChequesServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var SolicitudApiUrl='/conciliacion/Solicitudcheque';
		var apiUrl='/conciliacion/Cheques';

		function getCheques(){
			var deferred = $q.defer();

			$http.get(apiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});
			 return deferred.promise;
		};

		function getNoCheque(){
			var deferred = $q.defer();

			$http.get('/conciliacion/Cheques/im?format=json')
				 .success(function (data){
				 	deferred.resolve(data);
				 })
				 .error(function (err){
				 	deferred.resolve(err);
				 });
			return deferred.promise;
		};

		function setCheques(cheque){
			var deferred = $q.defer();

			$http.post(apiUrl, JSON.stringify({'cheque':cheque}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function getChequeById(id){
			var deferred = $q.defer();

			getCheques().then(function (data){
				var result= data.filter(function (reg){
					return reg.id = id; 
				});

				if(result.length > 0){
					deferred.resolve(result);
				}else{
					deferred.reject();
				}

				return deferred.response;
			});
		};

		function getSolicitudes(){
			var deferred = $q.defer();

			$http.get(SolicitudApiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});
			 return deferred.promise;
		};

		function getSolicitudByStatus(estatus){
			var deferred = $q.defer();

			getSolicitudes().then(function (data){
				var result =data.filter(function (reg){
					return reg.estatus == estatus;
				});

				if (result.length > 0){
					deferred.resolve(result);
				}
				else{
					deferred.reject();
				}
			});
			return deferred.promise;

		};

		function getSolicitudesById(id){
			var deferred = $q.defer();

			getSolicitudes().then(function (data){
				var result = data.filter(function (reg){
					return reg.id = id;
					});

				if (result.length > 0){
					deferred.resolve(result);
				}
				else{
					deferred.reject();
				}
			});

			return deferred.promise;
		};

		return {
			getCheques : getCheques,
			setCheques : setCheques,
			getSolicitudes : getSolicitudes,
			getSolicitudByStatus : getSolicitudByStatus,
			getSolicitudesById : getSolicitudesById,
			getChequeById : getChequeById,
			getNoCheque  : getNoCheque,
		};
	}])

	.controller('ChequeCtrl', ['$scope','$filter', '$rootScope', 'ChequesServices','$timeout', '$window','ContabilidadService',
		function ($scope, $filter, $rootScope, ChequesServices, $timeout, $window, ContabilidadService) {
		$scope.LsSolicitud = [];
		
		$scope.Solicitud = {};
		$scope.LsCheques = [];

		$scope.reCheque = {};

		$scope.independiente = null;
		$scope.emitido = false;

		$scope.ToggleCh = false;
		$scope.ToggleSl = false;
		$scope.ToggleNCh = false;
		$scope.fecha = null;

		$scope.listSolicitud = function($event){
			$event.preventDefault();

			$scope.ToggleSl = true;
			$scope.ToggleNCh = false;
			$scope.ToggleCh = false;
			ChequesServices.getSolicitudByStatus('A').then(function (data){
				$scope.LsSolicitud = data;
			});

		};

		$scope.objectSorteable = function(a, b){
			if(a.id < b.id){
				return 1;
			}

			if(a.id > b.id){
				return -1;
			}

			return 0;
		}

		$scope.emitirCheque = function($event){
			$event.preventDefault();
			
			$scope.independiente = 1;
			$scope.emitido = true;
			var el = angular.element('#Beneficiario');
			el.attr('ng-disable','false').removeAttr('disabled');

			ChequesServices.getNoCheque().then(function (data){

				$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
				$scope.reCheque.estatus = "R";
				$scope.reCheque.solicitud = null;
				
				$scope.reCheque.noCheque = data[0].noCheque
				console.log(data);
			});

			$scope.ToggleCh = false;
			$scope.ToggleSl = false;
			$scope.ToggleNCh = true;

		}

		$scope.NewCheque =function($event,s){
			$event.preventDefault();
			console.log(s);
			$scope.reCheque.solicitud = s.id
			var fecha = s.fecha.split('-')

			$scope.reCheque.id = null;

			ChequesServices.getNoCheque().then(function (data){
				$scope.fecha = fecha[2]+"/"+fecha[1]+"/"+fecha[0];
				$scope.reCheque.fecha = fecha[2]+"/"+fecha[1]+"/"+fecha[0];
				$scope.reCheque.estatus = "R";
				if(s.socio != ""){
					$scope.reCheque.beneficiario = s.socio	
				}
				else{
					$scope.reCheque.beneficiario = s.suplidor
				};

				
					$scope.reCheque.noCheque = data[0].noCheque
					console.log(data);
			});

			$scope.ToggleCh = false;
			$scope.ToggleSl = false;
			$scope.ToggleNCh = true;
		}

		$scope.listCheques = function($event){
			$event.preventDefault();

			$scope.ToggleSl = false;
			$scope.ToggleNCh = false;
			$scope.ToggleCh = true;

			ChequesServices.getCheques().then(function (data){
				$scope.LsCheques = data.sort($scope.objectSorteable);
				console.log(data);
			});

		};

		$scope.getSolicitudes = function($event){
			ChequesServices.getSolicitudByStatus('P').then(function (data){
				$scope.LsSolicitud = data.sort($scope.objectSorteable);

			});
		};

		$scope.setConCheque = function($event){
			$event.preventDefault();
			try{
				var RegFecha = $scope.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          		$scope.reCheque.fecha = FechaFormat;

          		if($scope.independiente != null){
          			$scope.toggleInfo();
          		}
          		else{
					ChequesServices.setCheques($scope.reCheque).then(function (data){
						var resp = data;
						if(data == "Ok"){
							
							notie.alert(1,"Cheque generado",3.2)
						}else{
							notie.alert(3,"Ocurrio un error al intentar generar el cheque",3.2);
							console.log(data);
						}
							$scope.cancelRegistro ($event);
							$scope.listCheques($event);
							$scope.getSolicitudes($event);
							
					});
				}
			}
			catch(e){
				$rootScope.mostrarError(e);
			}
			}


		$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
			};


		$scope.getSolicitud = function($event, id){
			$event.preventDefault();

			getSolicitudesById(id).then(function (data){
				$scope.Solicitud = data;
			});
		};

		$scope.getCheque = function($evnet, id){
			$event.preventDefault();
			$scope.reCheque = null;

			ChequesServices.getChequeById(id).then(function (data){
				$scope.reCheque = data;
			});
		};


		$scope.printChk = function($event,ch){
			$window.sessionStorage['chk'] = JSON.stringify(ch);

			$window.open('/conciliacion/Cheques/im', target='_blank'); 
		};

		$scope.cancelRegistro = function($event){
			$scope.ToggleCh = false;
			$scope.ToggleSl = true;
			$scope.ToggleNCh = false;
			$scope.reCheque = {};
			$scope.independiente = null;
			$scope.emitido = false;

		};

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
	        desgloseCuenta.ref = 'TEST-0000';//$scope.desgloseCuentas[$scope.desgloseCuentas.length-1].ref;
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
	          $scope.regCheque.cuentas = $scope.desgloseCuentas
	          
	          ChequesServices.setCheques($scope.reCheque).then(function (data){
						var resp = data;
						if(data == "Ok"){
							
							notie.alert(1,"Cheque generado",3.2)
						}else{
							notie.alert(3,"Ocurrio un error al intentar generar el cheque",3.2);
							console.log(data);
						}
							$scope.cancelRegistro ($event);
							$scope.listCheques($event);
							$scope.getSolicitudes($event);
							
					});
	          
			$scope.independiente = 1;
			$scope.emitido = true;

			var el = angular.element('#Beneficiario');
			el.attr('ng-disabled','true').attr('disabled','disabled');
	

	          
			 $scope.getConcNotas();
	          notie.alert(1,'Los registros fueron posteados con exito!',3.2);

	        } catch (e) {
	          notie.alert(3,e,3.2);
	        }
	      } 

	}])

	.controller('ImpchequeCtrl', ['$scope','$filter', '$rootScope', 'ChequesServices','$timeout', '$window' ,
		function ($scope, $filter, $rootScope, ChequesServices, $timeout, $window) {

			$scope.dia =null;
			$scope.mes =null;
			$scope.agno =null;

			$scope.nombre = null;
			$scope.monto = null;
			$scope.letras =null;
			$scope.fecha = null;
			$scope.concepto = null;
			$scope.cuentas = [];

		$scope.start = function(){
			
			$scope.regData = JSON.parse($window.sessionStorage['chk']);
			$scope.cuentas = $scope.regData.cuenta;
			var formFecha = $scope.regData.fecha.split('-');
			$scope.dia = formFecha[2];
			$scope.mes = formFecha[1];
			$scope.agno = formFecha[0];


			
		}	
			
	}]);
})();