(function(_){
	angular.module('cooperativa.activofijo', ['ngAnimate'])

	.factory('ActivoServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var apiUrl='/activoJson/';
		var apiUrlD = '/depresiacion/';
		
		function getActivos(){
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

		function setActivo(regActivo){
			var deferred = $q.defer();

            $http.post(apiUrl, JSON.stringify({'activo':regActivo}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function setDepresiacion(cuentas, fechaF){
			var deferred = $q.defer();

			$http.post(apiUrlD, JSON.stringify({'cuentas':cuentas,'fechaF': fechaF}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function getActivosById(id){
			var deferred = $q.defer();

			getActivos.then(function (data){
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

		function getSuplidor(){
                var deferred =$q.defer();

                $http.get('/api/suplidor/?format=json')
                .success(function (data){
                    deferred.resolve(data);})
                .error(function (err){
                    deferred.resource(err);
                });
                
                return deferred.promise;
        };

		return {
			getActivos 	    : getActivos,
			setActivo       : setActivo,
			getActivosById  : getActivosById,
			getSuplidor     : getSuplidor,
			setDepresiacion : setDepresiacion
		};
	}])
	
	.controller('ActivoCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout', 
			function ($scope, $filter, $rootScope, ActivoServices, $timeout ){

			$scope.actData = null;
			$scope.lsActivos = [];
			$scope.depList= [];
			$scope.actVs = true;
			$scope.actRg = false;
			$scope.depVs = false;

			$scope.addAct = function($event){
				$scope.actData = null;
				$scope.actVs = false;
				$scope.actRg = true;
			};

			$scope.lstActivos = function($event){
				ActivoServices.getActivos().then(function (data){
					$scope.lsActivos = data;
				})
			};

			$scope.guardarActivo = function($event){
				$event.preventDefault();
				try{
					if($scope.actData.id === undefined){
						$scope.actData.id = null;
					}

					var RgFechaA = $scope.actData.fechaAdq.split('/');
          			var FechaFormat = RgFechaA[2] + '-' + RgFechaA[1] + '-' + RgFechaA[0];
          			$scope.fechaAdq.fechaAdq = FechaFormat;

          			var RgFechaD = $scope.actData.fechaAdq.split('/');
          			var FechaFormatD = RgFechaD[2] + '-' + RgFechaD[1] + '-' + RgFechaD[0];
          			$scope.fechaAdq.fechaDep = FechaFormatD;

					var result = ActivoServices.setActivo($scope.actData);
					//$window.sessionStorage['activoId'] = JSON.stringify($scope.actData);
					$scope.lstActivos();
					$scope.cancelarActivo();
					//$window.open('/impActivo/', target='_blank'); 

				}
				catch(ex){
					$rootScope.mostrarError(ex.message);
				}
            };

            $scope.getDepresiacion = function(id){
				ActivoServices.getActivosById(id).then(function (data){
					$scope.depList = data.depresiacion;
				});
			};

            $scope.cancelarActivo = function(){
	       		$scope.actData = null;
	       		$scope.depList = null;
	       		$scope.actVs = true;
	       		$scope.actRg = false;
	       	};

			
	}])
	
	.controller('DepresiacionCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout',
		function($scope, $filter, $rootScope, $ActivoServices, $timeout){

			$scope.depList= [];
			$scope.cuentas = [];
			$scope.fechaDesp = null;

			$scope.setDepresiacion = function (){
				try{
					if ($scope.cuentas.length > 0){
						ActivoServices.setDepresiacion($scope.cuentas, $scope.fechaDesp);
					}
					else{
						$rootScope.mostrarError("No hay cuentas definidas.");
					}

				}
				catch(ex){
					$rootScope.mostrarError(ex.message);
				}

				
			};
			

		}]);

})();
