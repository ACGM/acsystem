(function (_){
	angular.module('cooperativa.notaConc', ['ngAnimate'])

	.factory('NotasConcServices', ['$http','$q','$filter', 
		function ($http, $q, $filter) {
			var apiUrl='/conciliacion/notas';
			var NostasApiUrl='/conciliacion/notas/rg/';

			function getNotas(){
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

			function setNotas(notas){
				var deferred = $q.defer();

				$http.post(apiUrl, JSON.stringify({'Notas':notas}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};

			function getNotasId(id){
				var deferred = $q.defer();

				getNotas().then(function (data){
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

			function getNotasByType(tipo){
				var deferred = $q.defer();

				getNotas().then(function (data){
					var result= data.filter(function (reg){
						return reg.tipo = tipo; 
					});

					if(result.length > 0){
						deferred.resolve(result);
					}else{
						deferred.reject();
					}

					return deferred.response;
				});
			};
			
			function getNotasByFecha(fechaI, fechaF){
				var deferred = $q.defer();

				$http.get(NostasApiUrl+'?fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});

				return deferred.promise;
			}
	
		return {
			getNotas : getNotas,
			setNotas : setNotas,
			getNotasId : getNotasId,
			getNotasByType : getNotasByType,
			getNotasByFecha, getNotasByFecha


		};
	}])
	
	.controller('NotasConcCtrl', ['$scope','$filter', '$rootScope', 'NotasConcServices','$timeout','appService', '$window', 'ContabilidadService',
		function ($scope, $filter, $rootScope, NotasConcServices, timeout, appService, $window, ContabilidadService ) {
			$scope.CrNota= false;
			$scope.lsView = true;
			$scope.LsNotas = [];
			$scope.Nota = null;
			$scope.fechai = null;
			$scope.fechaf = null;
			$scope.rgNote = {};
		    
		    $scope.desgloseCuentas = [];
		    $scope.posteoG = false;


			//Traer todas las cuentas a javascript
	      	appService.allCuentasContables().then(function (data) {
	        	if(data.length > 0) {
	          		$scope.todasLasCuentas = data;
	        	}
	      	});

			$scope.nueva = function(){
				$scope.CrNota = true;
				$scope.lsView = false;
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

			$scope.getConcNotas = function($event){
				// $event.preventDefault();
				
				NotasConcServices.getNotas().then(function (data){
					$scope.LsNotas = [];
					$scope.LsNotas = data.sort($scope.objectSorteable);
					$scope.lsView = true;
	          		$scope.CrNota = false;
	          		$scope.showPostear  = false;
				});
			};

			$scope.getConNotasF = function($event){
				$scope.LsNotas = [];
				
				
				NotasConcServices.getNotas().then(function (data){
					$scope.LsNotas = data.filter(function(rep){
						var RegFecha = rep.fecha.split('-');
          				var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
          				rep.fecha = FechaFormat;

						return rep.fecha >= $scope.fechai && rep.fecha <= $scope.fechaf; 
					}).sort($scope.objectSorteable);
					$scope.lsView = true;
	          		$scope.CrNota = false;
	          		$scope.showPostear  = false;
				});
			};

			$scope.setConNotas = function($event){
				$event.preventDefault();
				try{
					
					var regFecha = $scope.rgNote.fecha.split('/');
					var FechaFormat = regFecha[2] + '-' + regFecha[1] + '-' + regFecha[0];
					$scope.rgNote.fecha = FechaFormat;
					$scope.rgNote.estatus = 'P';

					if($scope.rgNote.id == undefined){
						$scope.rgNote.id = null;
					}
					$scope.registro = null
					NotasConcServices.setNotas($scope.rgNote).then(function (data){
						$scope.registro = data;
					});
					$scope.iDocumentos = 0;
					$scope.toggleInfo();
					notie.alert(1,"Registro Guardado",3.2);
				}
				catch(e){
					// $rootScope.mostrarError(e);
					notie.alert(3,e,3.2);
				}
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
	          $scope.desgloseCuentas.forEach(function (item) {
	            ContabilidadService.guardarEnDiario(Date.now(), item.cuenta, item.ref, item.debito, item.credito).then(function (data) {
	              console.log('Registros guardados en el diario');
	              console.log(data);
	            });
	          });

	          // InventarioService.postearINV($scope.entradasSeleccionadas, 'EINV').then(function (data) {
	          //   console.log(data);
	          //   $scope.listadoEntradas();
	          // });
			 $scope.getConcNotas();
	          notie.alert(1,'Los registros fueron posteados con exito!',3.2);

	        } catch (e) {
	          notie.alert(3,e,3.2);
	        }
	      } //Linea FIN de posteo Contabilidad.

			

			$scope.getConNota = function($event, id){
				NotasConcServices.getNotasId(id).then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

			$scope.getConNotaType = function($event, tipo){
				NotasConcServices.getNotasByType(tipo).then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

			$scope.getConNotaFecha = function($event, fechaI, fechaF){
				NotasConcServices.getNotasByFecha(fechai, fechaF).then(function (data){
					$scope.LsNotas = []
					$scope.LsNotas = data;
				});
			};

	}]);
})();