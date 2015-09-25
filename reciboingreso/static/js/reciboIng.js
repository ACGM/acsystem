// reciboIngCtrl


(function(_){
	angular.module('cooperativa.reciboIng',['ngAnimate'])

		.factory('reciboIngServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/reciboIngreso';

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
			}

			function socios() {
                var deferred = $q.defer();

                $http.get('/api/socio/?format=json')
                  .success(function (data) {
                    deferred.resolve(data.filter( function(socio) {
                      return socio.estatus == "E" || socio.estatus == "S";

                    }));
                  });
                  return deferred.promise;
            }

			return {
				getRecibos : getRecibos,
				getReciboBySocio : getReciboBySocio,
				setRecibo : setRecibo,
				socios : socios
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

			$scope.getList = function($event){
				$event.preventDefault();

				$scope.reciboLista =[];

				reciboIngServices.getRecibos().then(function (data) {
					$scope.reciboLista = data;
				});
			}

			$scope.nwRecibo = function($event){
				$scope.reciboLst = false;
				$scope.reciboCr = true;
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
	            $scope.tableSuplidor = false;

	            if($scope.socioNombre !== undefined) {
	              reciboIngServices.socios().then(function (data) {
	                $scope.socios = data.filter(function (registro) {
	                  return $filter('lowercase')(registro.codigo.toString()
	                                      .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
	                });

	                if($scope.socios.length == 0){
	                	$scope.socios = data.filter(function (registro) {
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

	              });
	            } else {
	              reciboIngServices.socios().then(function (data) {
	                $scope.socios = data;
	                $scope.socioCodigo = '';
	              });
	            }
	          };

	        $scope.selPrest = function($event, x){
	       		$event.preventDefault();

	       		$scope.reciboData.prestamo=x.noPrestamo;
	            $scope.montoInicial = x.montoInicial;

	            $scope.tablePrest = false;
	          };

	       	$scope.selSocio = function($event, s) {
	       		$event.preventDefault();

	       		$scope.reciboData.socio=s.codigo;
	            $scope.socioNombre = s.nombreCompleto;

	            $scope.tableSocio = false;
	          };

	        $scope.getPrestamosSocio = function($event){

	        	MaestraPrestamoService.PrestamosbySocio($scope.reciboData.socio).then(function (data){
	        		$scope.prestamosS = data.filter(function (reg){
	        			return reg.estatus != "S"
	        		});
	        	});
	        	$scope.tablePrest = true;
	        	}

	        $rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		    	};

	        $scope.setRecibo = function($event){
	        	$event.preventDefault();

	        	var RegFecha = $scope.reciboData.fecha.split('/');
          			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          			$scope.reciboData.fecha = FechaFormat;

          		try{
          			reciboIngServices($scope.reciboData).then(function (data){
          				console.log(data);
          			});
          		}	
          		catch(ex){
          			$rootScope.mostrarError(ex.message);
          		}
	        	};
}]); 
})(_);