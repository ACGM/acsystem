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
	
	.controller('NotasConcCtrl', ['$scope','$filter', '$rootScope', 'NotasConcServices','$timeout','appService', '$window', 
		function ($scope, $filter, $rootScope, NotasConcServices, timeout, appService, $window ) {
			$scope.CrNota= false;
			$scope.lsView = true;
			$scope.LsNotas = [];
			$scope.Nota = null;
			$scope.fechai = null;
			$scope.fechaf = null;
			$scope.rgNote = {};


			$scope.nueva = function(){
				$scope.CrNota = true;
				$scope.lsView = false;
			};

			$scope.getConcNotas = function($event){
				// $event.preventDefault();
				NotasConcServices.getNotas().then(function (data){
					$scope.LsNotas = [];
					$scope.LsNotas = data;
				});
			};

			$scope.getConNotasF = function($event){
				$scope.LsNotas = null;
				console.log($scope.fechai);

				NotasConcServices.getNotas().then(function (data){
					$scope.LsNotas = data.filter(function(rep){
						var RegFecha = rep.fecha.split('-');
          				var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
          				rep.fecha = FechaFormat;

						return rep.fecha >= $scope.fechai && rep.fecha <= $scope.fechaf; 
					});
				});
			};

			$scope.setConNotas = function($event){
				$event.preventDefault();
				try{
					
					// var regFecha = $scope.rgNote.fecha.split('/');
					// var FechaFormat = regFecha[2] + '-' + regFecha[1] + '-' + regFecha[0];
					// $scope.rgNote.fecha = FechaFormat;
					// $scope.rgNote.estatus = 'R';

					// if($scope.rgNote.id == undefined){
					// 	$scope.rgNote.id = null;
					// }
					// $scope.registro = null
					// NotasConcServices.setNotas($scope.rgNote).then(function (data){
					// 	$scope.registro = data;
					// });
					$scope.posteo();
				}
				catch(e){
					$rootScope.mostrarError(e);
				}
			}

			$scope.posteo = function(){
				 var idoc = 0;
			      $scope.iDocumentos = 0;
			      $scope.totalDebito = 0.00;
			      $scope.totalCredito = 0.00;

			      $scope.showPostear = true;
			      $scope.desgloseCuentas = [];

			      $scope.registro = '1';

			      appService.getDocumentoCuentas('NCC').then(function (data) {
			        var documentoCuentas = data[0];
			        console.log(documentoCuentas);

			        //Prepara cada linea de posteo

			        var desgloseCuenta = new Object();
			        if($scope.rgNote.tipo =='D'){
			        	$scope.totalDebito += parseFloat($scope.rgNote.monto);
			        }else{
			        	$scope.totalCredito += parseFloat($scope.rgNote.monto);
			        }
			        desgloseCuenta.cuenta = documentoCuentas.getCuentaCodigo;
		            desgloseCuenta.descripcion = documentoCuentas.getCuentaDescrp;
		            desgloseCuenta.ref = documentoCuentas.getCodigo + $scope.registro;
		            desgloseCuenta.debito = $scope.rgNote.tipo == 'D'? $scope.rgNote.monto: $filter('number')(0.00, 2);
		            desgloseCuenta.credito = $scope.rgNote.tipo == 'C'? $scope.rgNote.monto: $filter('number')(0.00, 2);
		            desgloseCuenta.nota = $scope.registro;

			        $scope.desgloseCuentas.push(desgloseCuenta);
			        console.log(desgloseCuenta);

			     });

			}

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